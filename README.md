# Playwright Automation - APLK Recording Downloader

Automated script to extract YouTube links from ap.lk class recordings using Playwright and OpenAI's GPT.

## Features

✅ **AI-Powered Month Extraction** - Uses GPT-3.5-turbo to understand natural language commands  
✅ **Persistent Chrome Login** - Uses your existing Chrome profile to stay logged in  
✅ **Async/Await Pattern** - Fast, non-blocking browser automation  
✅ **Error Handling** - Comprehensive logging and error recovery  
✅ **Cross-Platform** - Works on Windows, macOS, and Linux  
✅ **YouTube Link Extraction** - Efficiently finds all YouTube links on the page  

## Prerequisites

- Python 3.8+
- Google Chrome installed
- OpenAI API key

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/gavithgethmin01/Playwright_Automation.git
cd Playwright_Automation
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Setup environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### 5. Update Chrome path
Edit `APLK_automation.py` and update the `get_chrome_user_data_dir()` function with your username:

**Windows:**
```python
return r"C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data"
```

**macOS:**
```python
return f"/Users/YOUR_USERNAME/Library/Application Support/Google/Chrome"
```

**Linux:**
```python
return f"/home/YOUR_USERNAME/.config/google-chrome"
```

## Usage

Run the script with a natural language command:

```bash
python APLK_automation.py
```

Then enter a command like:
- `absorb May recordings`
- `get links for June`
- `extract this month's videos`
- `show me April's class links`

The script will:
1. Parse your command with AI to extract the month
2. Open ap.lk in your Chrome browser
3. Navigate to the specified month
4. Extract all YouTube links
5. Display them in the console

## Example Output

```
2026-05-04 10:30:45 - INFO - Processing command: absorb May recordings
2026-05-04 10:30:46 - INFO - Target month extracted: May
2026-05-04 10:30:47 - INFO - Launching browser with Chrome profile...
2026-05-04 10:30:50 - INFO - Navigating to ap.lk/class...
2026-05-04 10:30:52 - INFO - Page accessibility verified
2026-05-04 10:30:53 - INFO - Searching for month: May
2026-05-04 10:30:54 - INFO - Clicked on May
2026-05-04 10:30:56 - INFO - Page loaded after month selection
2026-05-04 10:30:57 - INFO - Extracting YouTube links...
2026-05-04 10:30:58 - INFO - Successfully found 5 YouTube links

✅ Successfully absorbed 5 links:
1. https://www.youtube.com/watch?v=dQw4w9WgXcQ
2. https://www.youtube.com/watch?v=9bZkp7q19f0
3. https://youtu.be/jNQXAC9IVRw
4. https://www.youtube.com/watch?v=tYzMGcUty6s
5. https://www.youtube.com/watch?v=kJQP7kiw9Fk
```

## Architecture

### Key Functions

- **`extract_month_from_ai()`** - Uses OpenAI to parse natural language commands
- **`get_chrome_user_data_dir()`** - Detects OS and returns Chrome user data path
- **`click_month_element()`** - Finds and clicks the target month on the page
- **`extract_youtube_links()`** - Extracts all YouTube links from the page
- **`verify_page_accessibility()`** - Checks if page loaded correctly
- **`absorb_recordings()`** - Main orchestrator function
- **`main()`** - Entry point

### Logging

The script uses Python's built-in logging module. You can adjust the log level in the code:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Troubleshooting

### Issue: "Chrome user data directory not found"
**Solution:** Update the path in `get_chrome_user_data_dir()` with your actual username.

### Issue: "OPENAI_API_KEY environment variable not set"
**Solution:** 
1. Copy `.env.example` to `.env`
2. Add your OpenAI API key to `.env`
3. Ensure `python-dotenv` is installed: `pip install python-dotenv`

### Issue: Month not found on page
**Solution:** 
- Check if the website structure has changed
- Try running with `logging.DEBUG` to see what the page contains
- The month might be in a different format (e.g., number instead of name)

### Issue: "No YouTube links found"
**Solution:**
- The page might not have loaded fully
- Increase the timeout in `page.goto()` or `page.wait_for_selector()`
- Check if YouTube links exist on the page manually

## Security Notes

⚠️ **Never commit `.env` file** - It contains your API key  
⚠️ Add `.env` to `.gitignore` - Already included in generated `.gitignore`  
⚠️ Keep your OpenAI API key secure - Don't share it with anyone  

## Requirements

```
playwright>=1.40.0
openai>=1.3.0
python-dotenv>=1.0.0
```

## License

MIT License - Feel free to use this for personal projects

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify your OpenAI API key is valid
4. Ensure Chrome is properly installed

---

**Created by:** gavithgethmin01  
**Last Updated:** 2026-05-04 12:08:30