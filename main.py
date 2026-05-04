import asyncio
import datetime
import os
import logging
from typing import List
import calendar

from openai import OpenAI
from playwright.async_api import async_playwright, Page

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client from environment variable
def init_openai_client():
    """Initialize OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it before running this script."
        )
    return OpenAI(api_key=api_key)

client = init_openai_client()

def extract_month_from_ai(user_command: str) -> str:
    """
    Use AI to extract target month from user command.
    
    Args:
        user_command: User's natural language command
        
    Returns:
        Month name (e.g., "May")
        
    Raises:
        ValueError: If month cannot be extracted
    """
    current_date = datetime.datetime.now().strftime("%B %Y")
    prompt = (
        f"Current date is {current_date}. User command: '{user_command}'. "
        f"Extract ONLY the month name from the command. "
        f"Return just the month name, nothing else. "
        f"Example: 'May' or 'June'"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        extracted_text = response.choices[0].message.content.strip()
        
        # Validate the response is a valid month
        valid_months = [calendar.month_name[i] for i in range(1, 13)]
        month = next(
            (m for m in valid_months if m.lower() == extracted_text.lower()),
            None
        )
        
        if not month:
            raise ValueError(
                f"AI returned '{extracted_text}' which is not a valid month. "
                f"Valid months: {', '.join(valid_months)}"
            )
        
        return month
        
    except Exception as e:
        logger.error(f"Failed to extract month from AI: {e}")
        raise

def get_chrome_user_data_dir() -> str:
    """
    Get the Chrome user data directory path for the current OS.
    
    Returns:
        Path to Chrome user data directory
    """
    import platform
    system = platform.system()
    
    if system == "Windows":
        return r"C:\Users\YourName\AppData\Local\Google\Chrome\User Data"
    elif system == "Darwin":  # macOS
        return f"/Users/YourName/Library/Application Support/Google/Chrome"
    elif system == "Linux":
        return f"/home/YourName/.config/google-chrome"
    else:
        raise ValueError(f"Unsupported operating system: {system}")

async def extract_youtube_links(page: Page) -> List[str]:
    """
    Extract all YouTube links from the page.
    
    Args:
        page: Playwright page object
        
    Returns:
        List of unique YouTube URLs
    """
    try:
        # Wait for YouTube links to appear (with timeout)
        await page.wait_for_selector(
            "a[href*='youtube.com'], a[href*='youtu.be']",
            timeout=10000
        )
        
        # Get all YouTube links efficiently using locators
        yt_locator = page.locator("a[href*='youtube.com'], a[href*='youtu.be']")
        count = await yt_locator.count()
        
        if count == 0:
            logger.warning("No YouTube links found on page")
            return []
        
        links = []
        for i in range(count):
            href = await yt_locator.nth(i).get_attribute("href")
            if href and href not in links:  # Avoid duplicates
                links.append(href)
                logger.debug(f"Found YouTube link: {href}")
        
        return links
        
    except Exception as e:
        logger.error(f"Failed to extract YouTube links: {e}")
        return []

async def click_month_element(page: Page, target_month: str) -> bool:
    """
    Find and click the month element on the page.
    
    Args:
        page: Playwright page object
        target_month: Month name to search for
        
    Returns:
        True if month was found and clicked, False otherwise
    """
    try:
        logger.info(f"Searching for month: {target_month}")
        
        # Use intelligent locator to find month (works with links, buttons, divs, etc.)
        month_locator = page.get_by_text(target_month, exact=False)
        count = await month_locator.count()
        
        if count == 0:
            logger.error(f"Month '{target_month}' not found on page")
            return False
        
        # Click the first occurrence (most likely the correct one)
        await month_locator.first.click()
        logger.info(f"Clicked on {target_month}")
        
        # Wait for page to update
        await page.wait_for_load_state("networkidle")
        logger.info("Page loaded after month selection")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to click month element: {e}")
        return False

async def verify_page_accessibility(page: Page) -> bool:
    """
    Verify that the page loaded correctly and is accessible.
    
    Args:
        page: Playwright page object
        
    Returns:
        True if page is accessible, False otherwise
    """
    try:
        # Check if page has content
        body_text = await page.text_content("body")
        if not body_text or len(body_text.strip()) < 10:
            logger.error("Page appears to be empty or not loaded properly")
            return False
        
        logger.info("Page accessibility verified")
        return True
        
    except Exception as e:
        logger.error(f"Failed to verify page accessibility: {e}")
        return False

async def absorb_recordings(command: str) -> List[str]:
    """
    Main function to absorb YouTube recordings from ap.lk.
    
    Args:
        command: User command (e.g., "absorb May recordings")
        
    Returns:
        List of YouTube URLs found
    """
    
    # Extract target month from user command using AI
    logger.info(f"Processing command: {command}")
    target_month = extract_month_from_ai(command)
    logger.info(f"Target month extracted: {target_month}")
    
    # Get Chrome user data directory
    user_data_dir = get_chrome_user_data_dir()
    logger.info(f"Using Chrome user data directory: {user_data_dir}")
    
    # Verify directory exists
    if not os.path.exists(user_data_dir):
        logger.error(
            f"Chrome user data directory not found: {user_data_dir}\n"
            f"Please update the path in get_chrome_user_data_dir() function"
        )
        return []
    
    async with async_playwright() as p:
        context = None
        try:
            # Launch browser with your Chrome profile
            logger.info("Launching browser with Chrome profile...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir,
                channel="chrome",
                headless=False,
                args=["--start-maximized"]
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Navigate to ap.lk
            logger.info("Navigating to ap.lk/class...")
            try:
                await page.goto("https://ap.lk/class", wait_until="networkidle", timeout=15000)
            except Exception as e:
                logger.error(f"Failed to navigate to ap.lk: {e}")
                return []
            
            # Verify page loaded
            if not await verify_page_accessibility(page):
                logger.error("Page failed accessibility check")
                return []
            
            # Click the target month
            if not await click_month_element(page, target_month):
                logger.error(f"Could not find or click month: {target_month}")
                return []
            
            # Extract YouTube links
            logger.info("Extracting YouTube links...")
            youtube_links = await extract_youtube_links(page)
            
            if not youtube_links:
                logger.warning("No YouTube links were found")
                return []
            
            logger.info(f"Successfully found {len(youtube_links)} YouTube links")
            for link in youtube_links:
                print(link)
            
            return youtube_links
            
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return []
        
        finally:
            if context:
                await context.close()
                logger.info("Browser context closed")

async def main():
    """Main entry point."""
    try:
        user_command = input("Enter command (e.g., 'absorb May recordings'): ").strip()
        
        if not user_command:
            logger.error("Command cannot be empty")
            return
        
        links = await absorb_recordings(user_command)
        
        if links:
            logger.info(f"\n✅ Successfully absorbed {len(links)} links:")
            for i, link in enumerate(links, 1):
                print(f"{i}. {link}")
        else:
            logger.warning("⚠️  No links were found")
            
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
