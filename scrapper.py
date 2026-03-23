from playwright.sync_api import sync_playwright
import json

def extract_entertainment():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening Ekantipur Entertainment...")
        page.goto("https://ekantipur.com/entertainment", wait_until="domcontentloaded")
        
        # We wait for the inner wrappers which represent individual news items
        page.wait_for_selector('.category-inner-wrapper')
        
        # Locate each individual news block
        articles = page.locator('.category-inner-wrapper').all()
        
        extracted_data = []

        # Loop through the first 5
        for i in range(min(5, len(articles))):
            item = articles[i]
            
            # Using .first to avoid the strict mode error if multiple tags exist
            title_node = item.locator('h2').first
            title = title_node.inner_text().strip() if title_node.count() > 0 else "N/A"

            # Image URL - looking specifically for the image in the thumbnail section
            img_node = item.locator('.category-image img').first
            image_url = None
            if img_node.count() > 0:
                image_url = img_node.get_attribute('data-src') or img_node.get_attribute('src')

            # Author - looking for the link inside the author name div
            author_node = item.locator('.author-name a').first
            author = author_node.inner_text().strip() if author_node.count() > 0 else None

            extracted_data.append({
                "title": title,
                "image_url": image_url,
                "category": "मनोरञ्जन",
                "author": author
            })

        with open('entertainment_news.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)

        print(f"Success! Extracted {len(extracted_data)} articles.")
        browser.close()

if __name__ == "__main__":
    extract_entertainment()