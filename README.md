# Ekantipur Scraper Setup

This project contains the web scraping logic for extracting **Entertainment News** and the **Cartoon of the Day** (व्यंग्यचित्र) from Ekantipur.

## 📋 Requirements
Save the following as `requirements.txt`:

```text
playwright==1.58.0
# pandas          # Uncomment if saving to CSV/Excel
# beautifulsoup4  # Uncomment if using for additional parsing

```

```
🚀 Re-Installation Steps
If you have deleted your venv and browser binaries to save space, follow these steps to get the project running again:

1. Create a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate
------------------------------------------

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

--------------------------------------------
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Install Chromium (Space-Saving)
Since this project primarily uses Chromium, you only need to install that specific browser to save disk space:
------------------------------------------
Bash
playwright install chromium
🛠 Project Scope
Target: ekantipur.com

Selectors: Custom DOM selectors for titles, authors, and lazy-loaded image URLs.

Features: Handles strict mode violations and dynamic content loading.

```
