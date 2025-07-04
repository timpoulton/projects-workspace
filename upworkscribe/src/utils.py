import re
import random
import html2text
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

COVER_LETTERS_FILE = "./data/cover_letter.md"

def extract_provider_and_model(model_string: str):
    """
    Extract the provider and model name from a given model string.

    Args:
        model_string (str): The model string in the format "provider/model".

    Returns:
        tuple: A tuple containing the provider and the model name.
    """
    return model_string.split("/", 1)

def get_llm_by_provider(model_string, temperature=0.1):
    """
    Retrieve the appropriate LLM instance based on the provider and model name.

    Args:
        model_string (str): The model string in the format "provider/model".
        temperature (float): The temperature for controlling output randomness.

    Returns:
        llm: An instance of the specified language model.

    Raises:
        ValueError: If the LLM provider is not supported.
    """
    llm_provider, model = extract_provider_and_model(model_string)
    
    # Match the provider and initialize the corresponding LLM
    if llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(model=model, temperature=temperature)
    elif llm_provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
    elif llm_provider == "groq":
        from langchain_groq import ChatGroq
        llm = ChatGroq(model=model, temperature=temperature)
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    return llm

async def ainvoke_llm(
    system_prompt,
    user_message,
    model="openai/gpt-4o-mini",  # Default to GPT-4o-mini
    response_format=None
):
    """
    Invoke a language model asynchronously with the given prompts.

    Args:
        system_prompt (str): The system-level instruction for the LLM.
        user_message (str): The user's message or query.
        model (str): The model string specifying the provider and model name.
        response_format: An optional format for structuring the output.

    Returns:
        str: The output generated by the LLM.
    """
    # Construct message inputs for the LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]  
    
    # Initialize the LLM based on the model
    llm = get_llm_by_provider(model)
    
    # Apply output parsing based on the response format
    if response_format:
        llm = llm.with_structured_output(response_format)
    else:
        llm = llm | StrOutputParser()
    
    # Execute the LLM invocation asynchronously
    output = await llm.ainvoke(messages)
    return output

async def get_playwright_browser_context(browser):
    """
    Creates a new Playwright browser context with a random user agent.

    Args:
        browser: The Playwright browser instance.

    Returns:
        BrowserContext: A new browser context with a random user agent.
    """
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 11; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0"
    ]

    # Select a random user agent for the browser context
    user_agent = random.choice(USER_AGENTS)
    
    browser_context = await browser.new_context(user_agent=user_agent)

    # Inject session cookies if a `cookies.json` file exists in the project root. This allows
    # authenticated scraping without hard-coding credentials. The file should contain an
    # array of Playwright-style cookie objects (same structure as chrome-devtools copy).
    import json, pathlib, datetime
    cookie_path = pathlib.Path(__file__).resolve().parent.parent / 'cookies.json'
    if cookie_path.exists():
        try:
            with cookie_path.open('r', encoding='utf-8') as f:
                cookies = json.load(f)
            # Playwright expects expires to be an int (Unix timestamp); if provided as string,
            # attempt to coerce ISO date → timestamp.
            for c in cookies:
                if isinstance(c.get('expires'), str):
                    try:
                        # Accept RFC3339/ISO 8601 format
                        dt = datetime.datetime.fromisoformat(c['expires'].replace('Z','+00:00'))
                        c['expires'] = int(dt.timestamp())
                    except Exception:
                        # If parsing fails, set session cookie by removing expires key
                        c.pop('expires', None)
            await browser_context.add_cookies(cookies)
        except Exception as e:
            print(f"[warn] Failed to load cookies.json: {e}")

    return browser_context

def convert_html_to_markdown(html_content):
    """
    Convert HTML content to markdown format.

    Args:
        html_content (str): The HTML content to be converted.

    Returns:
        str: The converted markdown content.
    """
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_tables = False
    markdown_content = h.handle(str(html_content))

    # Remove excessive newlines
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    return markdown_content.strip()

def format_scraped_job_for_scoring(jobs):
    """
    Format a list of scraped jobs for scoring.

    Args:
        jobs (list): The list of scraped job data.

    Returns:
        list: A list of dictionaries representing jobs with their IDs.
    """
    return [{'id': index, **job} for index, job in enumerate(jobs)]

def convert_jobs_matched_to_string_list(jobs_matched):
    """
    Convert a list of matched jobs to a list of formatted strings.

    Args:
        jobs_matched (DataFrame): The DataFrame containing matched job data.

    Returns:
        list: A list of job descriptions as formatted strings.
    """
    jobs = []
    for job in jobs_matched:
        job_str = f"# Title: {job['title']}\n"
        job_str += f"# Experience Level: {job['experience_level']}\n"
        job_str += f"# Description:\n{job['description']}\n\n"
        job_str += f"# Proposal Requirements:\n{job['proposal_requirements']}\n"
        jobs.append(job_str)
    return jobs

def read_text_file(filename):
    """
    Read a text file and return its contents as a single string.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The contents of the file.
    """
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        return "".join(lines)
