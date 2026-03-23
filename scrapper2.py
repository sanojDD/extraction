import json
from playwright.sync_api import sync_playwright

def scrape_ekantipur_cartoon():
    with sync_playwright() as p:
        # Launching with headless=False so you can verify the navigation
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Navigating to Ekantipur Cartoon Section...")
        page.goto("https://ekantipur.com/cartoon", wait_until="domcontentloaded")
        
        # Wait for the specific wrapper you identified
        try:
            page.wait_for_selector('.cartoon-wrapper', timeout=10000)
            
            # Select the first cartoon card
            card = page.locator('.cartoon-wrapper').first
            
            # 1. Extract Image URL
            # We look inside .cartoon-image img as per your DOM discovery
            img_el = card.locator('.cartoon-image img')
            image_url = img_el.get_attribute('src') or img_el.get_attribute('data-src')

            # 2. Extract and Split Description
            # Found in: .cartoon-description > p
            desc_el = card.locator('.cartoon-description p').first
            full_text = desc_el.inner_text().strip() # Result: "गजब छ बा! - अविन"

            # Logic to split the string at the " - " dash
            if " - " in full_text:
                parts = full_text.split(" - ")
                title = parts[0].strip()
                author = parts[1].strip()
            else:
                title = full_text
                author = "अविन" # Default fallback for the cartoonist

            cartoon_data = {
                "title": title,
                "image_url": image_url,
                "author": author
            }

            # 3. Save to JSON
            with open('cartoon_of_the_day.json', 'w', encoding='utf-8') as f:
                json.dump(cartoon_data, f, ensure_ascii=False, indent=4)

            print(f"Success! Extracted: {title} by {author}")

        except Exception as e:
            print(f"Error: {e}")
            # Take a screenshot if it fails to see what happened
            page.screenshot(path="cartoon_error.png")

        browser.close()

if __name__ == "__main__":
    scrape_ekantipur_cartoon()