import re
import asyncio
import hashlib
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio
from playwright.async_api import async_playwright
from src.utils import ainvoke_llm, get_playwright_browser_context, convert_html_to_markdown
from src.database import job_exists
from src.structured_outputs import JobInformation
from src.prompts import SCRAPER_PROMPT
import requests, urllib.parse, json, pathlib, datetime


class UpworkJobScraper:
    """
    Scrapes Upwork job data based on a search query.
    """

    def __init__(self, batch_size=5):
        """
        Initializes the UpworkJobScraper with a specified batch size for parallel scraping.

        Args:
            batch_size (int): The number of jobs to scrape in parallel. Defaults to 5.
        """
        self.batch_size = batch_size

    async def scrape_upwork_data(self, search_query="AI agent Developer", num_jobs=10):
        """
        Scrapes Upwork job data based on the search query in batches of 5 jobs at a time.
        """
        # 1. Hit Upwork's unofficial JSON search API – no Cloudflare HTML, just data.
        encoded_query = urllib.parse.quote_plus(search_query)
        paging_param = f"0;{num_jobs}"
        api_url = (
            "https://www.upwork.com/jobs/api/search?"
            f"q={encoded_query}&sort=recency&paging={paging_param}&api_params=true"
        )

        # Load cookies.json into a dict the requests library can use
        cookie_path = pathlib.Path(__file__).resolve().parent.parent / "cookies.json"
        cookies_dict = {}
        if cookie_path.exists():
            try:
                with cookie_path.open("r", encoding="utf-8") as f:
                    for c in json.load(f):
                        cookies_dict[c["name"]] = c["value"]
            except Exception as e:
                print(f"[warn] failed to load cookies.json for requests: {e}")

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.upwork.com/",
        }

        try:
            response = requests.get(api_url, headers=headers, cookies=cookies_dict, timeout=20)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
        except Exception as e:
            print(f"[error] Failed to fetch search JSON: {e}")
            results = []

        jobs_links_list = []
        for res in results:
            # The search API returns either 'ciphertext' or 'id' we can use in the apply URL
            job_id = res.get("ciphertext") or res.get("id") or res.get("jobId")
            if not job_id:
                continue
            link = f"https://www.upwork.com/freelance-jobs/apply/{job_id}"
            jobs_links_list.append(link)

        if len(jobs_links_list) == 0:
            print("[debug] Search API returned 0 jobs. Check cookies or query.")

        # 2. Use Playwright only for the individual job pages (HTML → markdown → LLM)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)

            semaphore = asyncio.Semaphore(self.batch_size)  # Limit concurrency to batch size tasks
            jobs_data = []

            async def scrape_job_with_semaphore(link):
                """Wrapper to scrape a job with a semaphore."""
                async with semaphore:
                    return await self.scrape_job_details(browser, link)

            # Scrape job pages in batches
            for i in tqdm_asyncio(range(0, len(jobs_links_list), self.batch_size), desc="Scraping job pages in batches"):
                batch_links = jobs_links_list[i:i+5]
                batch_results = await asyncio.gather(
                    *[scrape_job_with_semaphore(link) for link in batch_links]
                )
                jobs_data.extend(batch_results)

            await browser.close()

            # Filter out None results
            jobs_data = [job for job in jobs_data if job]

            # Process and return the job info data
            jobs_data = self.process_job_info_data(jobs_data)
                
            return jobs_data
    
    def extract_job_id_from_url(self, url):
        """
        Extract job ID from a job URL.
        """
        # Extract the part between 'apply/' and '/?referrer'
        match = re.search(r'apply/([^/]+)/?', url)
        if match:
            return match.group(1)
        return None

    def extract_jobs_urls(self, html):
        """
        Extracts job URLs from the HTML content and filters out already collected jobs.
        """
        soup = BeautifulSoup(html, 'html.parser')
        job_links = []
        skipped_count = 0
        
        # Upwork occasionally changes markup; accept either the legacy <h2.job-tile-title>
        # or the newer <h3.job-title-title ...> variant.
        heading_tags = soup.find_all('h2', class_='job-tile-title')
        heading_tags += soup.find_all('h3', class_=lambda c: c and 'job-title-title' in c)
        # New Upwork markup (July 2025) wraps the link directly with data-test="job-title-link"
        anchor_tags = soup.select('a[data-test="job-title-link"], a[data-test="tile-title-link"]')

        for a in anchor_tags:
            heading_tags.append(a)  # treat anchor as tag for unified processing

        for tag in heading_tags:
            a_tag = tag if tag.name == 'a' else tag.find('a')
            if a_tag:
                job_link = a_tag['href'].replace('/jobs', 'https://www.upwork.com/freelance-jobs/apply', 1)
                job_id = self.extract_job_id_from_url(job_link)
                
                # Skip if job already exists in database
                if job_id and job_exists(job_id):
                    skipped_count += 1
                    continue
                
                # clean the job url
                job_link = job_link.split('?')[0] if '?' in job_link else job_link 
                job_links.append(job_link)
        
        if skipped_count > 0:
            print(f"Skipped {skipped_count} already collected jobs")
            
        return job_links

    async def scrape_job_details(self, browser, url):
        """
        Scrapes and processes a single job page.
        """
        try:
            browser_context = await get_playwright_browser_context(browser)
            page = await browser_context.new_page()
            # Set a custom timeout for navigation
            await page.goto(url, timeout=60000)
            await page.goto(url, timeout=60000)
            try:
                await page.wait_for_selector('main#main', timeout=15000)
            except Exception:
                pass
            html_content = await page.content()

            # Parse the HTML to extract the <main> content of the page
            soup = BeautifulSoup(html_content, "html.parser")
            main_content = soup.find("main", id="main")
            job_page_content_markdown = convert_html_to_markdown(main_content)

            information = await ainvoke_llm(
                system_prompt=SCRAPER_PROMPT,
                user_message=f"Scrape all the relevant job details from the content of this page:\n\n{job_page_content_markdown}",
                model="openai/gpt-4o-mini",
                response_format=JobInformation,
            )
            job_info_dict = information.model_dump()

            # Process the job type from enum
            job_info_dict["job_type"] = information.job_type.value

            # Include job link in the output
            job_info_dict["link"] = url
            
            # Extract and add job_id
            job_id = self.extract_job_id_from_url(url)
            
            # hash the job_id
            job_info_dict["job_id"] = hashlib.sha256(job_id.encode()).hexdigest()

            # Ensure field names match the database schema
            # Map client_information fields to the correct database field names
            client_info = job_info_dict.pop("client_information", None)
            if client_info:
                job_info_dict.update({
                    f"client_{key}": value
                    for key, value in client_info.items()
                })

            return job_info_dict
        except Exception as e:
            print(f"Error processing link {url}: {e}")
            return None
        finally:
            await page.close()  # Ensure the page is closed

    def process_job_info_data(self, jobs_data):
        for job in jobs_data:
            if job.get("payment_rate"):
                job["payment_rate"] = re.sub(
                    r"\$?(\d+\.?\d*)\s*\n*-\n*\$?(\d+\.?\d*)", r"$\1-$\2", job["payment_rate"]
                )
        return jobs_data