"""
Upwork job scraper module
"""

import time
import logging
import re
import uuid
from typing import List, Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

# Import configuration
try:
    from config import config
except ImportError:
    # Use default values if config module not found
    class DefaultConfig:
        UPWORK_USER_NAME = "User"
        UPWORK_USERNAME = "username@example.com"
        UPWORK_PASSWORD = "password"
        CHROME_VERSIONS = [90, 123]
        MAX_ATTEMPTS = 3
        HEADLESS = True
        SCRAPE_DELAY = 2
        MAX_JOBS = 20
        SCROLL_PAUSE_TIME = 1.5
    config = DefaultConfig()

# Set up logger
logger = logging.getLogger(__name__)

class UpworkScraper:
    """
    Scraper for Upwork jobs using Selenium with undetected ChromeDriver
    """
    
    def __init__(self):
        """Initialize the scraper"""
        self.driver = None
        self.logged_in = False
    
    def _initialize_driver(self) -> bool:
        """Initialize Chrome driver with anti-detection measures"""
        for attempt in range(config.MAX_ATTEMPTS):
            for version in config.CHROME_VERSIONS:
                try:
                    logger.info(f"Initializing Chrome driver with version {version}, attempt {attempt + 1}")
                    options = uc.ChromeOptions()
                    
                    # Essential options for server environments
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-features=VizDisplayCompositor")
                    options.add_argument("--window-size=1920,1080")
                    
                    # Stealth options
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    
                    # Additional options for stability
                    options.add_argument("--disable-setuid-sandbox")
                    options.add_argument("--disable-software-rasterizer")
                    options.add_argument("--disable-extensions")
                    options.add_argument("--disable-plugins")
                    options.add_argument("--enable-javascript")
                    
                    # Memory optimization
                    options.add_argument("--memory-pressure-off")
                    
                    # Add user agent
                    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
                    
                    # Headless mode if configured
                    if hasattr(config, 'HEADLESS') and config.HEADLESS:
                        options.add_argument("--headless=new")
                        options.add_argument("--disable-web-security")
                    
                    # Create driver
                    self.driver = uc.Chrome(
                        version_main=version, 
                        options=options,
                        use_subprocess=False
                    )
                    
                    # Set timeouts
                    self.driver.implicitly_wait(10)
                    self.driver.set_page_load_timeout(30)
                    
                    # Execute stealth scripts
                    try:
                        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    except:
                        pass  # Some versions might not support this
                    
                    logger.info("Chrome driver initialized successfully")
                    return True
                except Exception as e:
                    logger.error(f"Failed to initialize Chrome driver with version {version}: {e}")
                    if self.driver:
                        try:
                            self.driver.quit()
                        except:
                            pass
                        self.driver = None
                    continue
        
        logger.error("Failed to initialize Chrome driver after all attempts")
        return False
    
    def login(self) -> bool:
        """Login to Upwork"""
        if not self.driver and not self._initialize_driver():
            return False
        
        try:
            logger.info("Logging in to Upwork")
            self.driver.get("https://www.upwork.com/ab/account-security/login")
            time.sleep(config.SCRAPE_DELAY * 2)  # Give page more time to load
            
            # Check if we're already logged in
            try:
                if self.driver.find_element(By.XPATH, f"//span[contains(text(), '{config.UPWORK_USER_NAME}')]"):
                    logger.info("Already logged in to Upwork")
                    self.logged_in = True
                    return True
            except:
                pass  # Not logged in, continue with login process
            
            # Wait for and enter username
            try:
                username_input = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "login_username"))
                )
                username_input.clear()
                time.sleep(0.5)
                username_input.send_keys(config.UPWORK_USERNAME)
                time.sleep(1)
                
                # Click continue button
                continue_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "login_password_continue"))
                )
                continue_button.click()
                time.sleep(config.SCRAPE_DELAY)
            except TimeoutException:
                logger.error("Could not find username input field. Page structure may have changed.")
                return False
            
            # Wait for and enter password
            try:
                password_input = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "login_password"))
                )
                password_input.clear()
                time.sleep(0.5)
                password_input.send_keys(config.UPWORK_PASSWORD)
                time.sleep(1)
                
                # Click login button
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "login_control_continue"))
                )
                login_button.click()
                time.sleep(config.SCRAPE_DELAY * 2)
            except TimeoutException:
                logger.error("Could not find password input field. Page structure may have changed.")
                return False
            
            # Check for CAPTCHA or other security challenges
            time.sleep(2)
            if "captcha" in self.driver.page_source.lower():
                logger.error("CAPTCHA detected. Manual intervention required.")
                return False
            
            # Check if login was successful
            try:
                # Wait for either the user name or the dashboard to appear
                WebDriverWait(self.driver, 20).until(
                    lambda driver: any([
                        self._check_element_exists(driver, By.XPATH, f"//span[contains(text(), '{config.UPWORK_USER_NAME}')]"),
                        self._check_element_exists(driver, By.XPATH, "//a[contains(@href, '/nx/find-work/')]"),
                        self._check_element_exists(driver, By.XPATH, "//button[contains(@aria-label, 'User menu')]")
                    ])
                )
                logger.info("Successfully logged in to Upwork")
                self.logged_in = True
                return True
            except TimeoutException:
                logger.error("Failed to verify login. Login may have failed or page structure changed.")
                # Log the current URL for debugging
                logger.error(f"Current URL: {self.driver.current_url}")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            logger.error(f"Current URL: {self.driver.current_url if self.driver else 'No driver'}")
            return False
    
    def _check_element_exists(self, driver, by, value):
        """Helper method to check if an element exists"""
        try:
            driver.find_element(by, value)
            return True
        except:
            return False
    
    def search_jobs(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for jobs on Upwork and extract job details
        
        Args:
            query: Search query string
            
        Returns:
            List of job dictionaries
        """
        if not self.logged_in and not self.login():
            logger.error("Not logged in. Cannot search for jobs.")
            return []
        
        jobs = []
        
        try:
            # Navigate to search page
            search_url = f"https://www.upwork.com/search/jobs/?q={query.replace(' ', '%20')}&sort=recency"
            logger.info(f"Navigating to search URL: {search_url}")
            self.driver.get(search_url)
            time.sleep(config.SCRAPE_DELAY * 2)
            
            # Scroll down to load more jobs
            self._scroll_page()
            
            # Extract job cards
            job_cards = self.driver.find_elements(By.XPATH, "//section[contains(@class, 'job-tile')]")
            logger.info(f"Found {len(job_cards)} job cards")
            
            # Process each job card
            for i, card in enumerate(job_cards[:config.MAX_JOBS]):
                try:
                    job = self._extract_job_details(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.error(f"Error extracting job details from card {i}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error during job search: {e}")
            return jobs
    
    def _extract_job_details(self, card) -> Optional[Dict[str, Any]]:
        """
        Extract job details from a job card
        
        Args:
            card: Selenium WebElement representing a job card
            
        Returns:
            Dictionary with job details or None if extraction failed
        """
        try:
            # Extract job title and URL
            title_element = card.find_element(By.XPATH, ".//a[contains(@class, 'job-title')]")
            job_title = title_element.text.strip()
            job_url = title_element.get_attribute("href")
            
            # Extract job ID from URL
            job_id_match = re.search(r"~([a-zA-Z0-9]+)", job_url)
            job_id = job_id_match.group(1) if job_id_match else str(uuid.uuid4())
            
            # Extract client info
            try:
                client_element = card.find_element(By.XPATH, ".//small[contains(@class, 'client-name')]")
                client_name = client_element.text.strip()
            except NoSuchElementException:
                client_name = "Unknown Client"
            
            # Extract budget
            try:
                budget_element = card.find_element(By.XPATH, ".//span[contains(@data-test, 'budget')]")
                budget = budget_element.text.strip()
            except NoSuchElementException:
                budget = "Not specified"
            
            # Extract description
            try:
                description_element = card.find_element(By.XPATH, ".//span[contains(@data-test, 'job-description-text')]")
                description = description_element.text.strip()
            except NoSuchElementException:
                description = "No description available"
            
            # Extract posting time
            try:
                time_element = card.find_element(By.XPATH, ".//span[contains(@data-test, 'posted-on')]")
                posted_time = time_element.text.strip()
            except NoSuchElementException:
                posted_time = "Unknown"
            
            # Calculate a simple score based on job title and description relevance
            # In a real implementation, this would be more sophisticated
            score = self._calculate_job_score(job_title, description)
            
            return {
                "job_id": job_id,
                "job_title": job_title,
                "client_name": client_name,
                "budget": budget,
                "description": description,
                "url": job_url,
                "posted_time": posted_time,
                "score": score,
                "status": "pending",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            logger.error(f"Error extracting job details: {e}")
            return None
    
    def _scroll_page(self):
        """
        Scroll down the page to load more job results
        """
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Number of scrolls (adjust based on how many jobs you want to load)
        max_scrolls = 5
        
        for _ in range(max_scrolls):
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for page to load
            time.sleep(config.SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, it means we've reached the end
                break
            last_height = new_height
    
    def _calculate_job_score(self, title: str, description: str) -> int:
        """
        Calculate a relevance score for the job
        
        Args:
            title: Job title
            description: Job description
            
        Returns:
            Score from 0 to 100
        """
        # This is a simple implementation. In a real system, this would use more
        # sophisticated matching algorithms, possibly with ML.
        
        # Define keywords that indicate a good match
        keywords = getattr(config, 'DEFAULT_SKILLS', [
            "python", "automation", "web scraping", "api", "selenium"
        ])
        
        # Calculate keyword matches
        text = (title + " " + description).lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in text)
        
        # Calculate score (simple version)
        max_matches = len(keywords)
        base_score = int((matches / max_matches) * 70)
        
        # Add bonus for specific high-value indicators
        bonus = 0
        if "automation" in text and "python" in text:
            bonus += 10
        if "web scraping" in text or "data extraction" in text:
            bonus += 10
        if "api" in text and "integration" in text:
            bonus += 5
            
        # Cap score at 100
        return min(base_score + bonus, 100)
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logged_in = False
            logger.info("Closed browser") 