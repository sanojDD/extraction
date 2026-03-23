import json
from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        # headless=False allows you to see the process; set to True for background run
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        results = {
            "entertainment_news": [],
            "cartoon_of_the_day": {}
        }

        # --- Task 1: Entertainment News ---
        print("Opening Ekantipur Entertainment...")
        page.goto("https://ekantipur.com/entertainment", wait_until="domcontentloaded")
        
        # Wait for content and scroll slightly to trigger lazy-loading
        page.wait_for_selector('.category-inner-wrapper')
        page.mouse.wheel(0, 500) 
        page.wait_for_timeout(1000)

        articles = page.locator('.category-inner-wrapper').all()
        for i in range(min(5, len(articles))):
            item = articles[i]
            
            title_node = item.locator('h2').first
            title = title_node.inner_text().strip() if title_node.count() > 0 else "N/A"

            img_node = item.locator('.category-image img').first
            image_url = None
            if img_node.count() > 0:
                # Check data-src first for lazy-loaded images
                image_url = img_node.get_attribute('data-src') or img_node.get_attribute('src')

            author_node = item.locator('.author-name a').first
            author = author_node.inner_text().strip() if author_node.count() > 0 else "N/A"

            results["entertainment_news"].append({
                "title": title,
                "image_url": image_url,
                "category": "मनोरञ्जन",
                "author": author
            })
        print(f"✓ Extracted {len(results['entertainment_news'])} news articles.")

        # --- Task 2: Cartoon of the Day ---
        print("\nNavigating to Ekantipur Cartoon Section...")
        page.goto("https://ekantipur.com/cartoon", wait_until="domcontentloaded")
        
        try:
            page.wait_for_selector('.cartoon-wrapper', timeout=10000)
            card = page.locator('.cartoon-wrapper').first
            
            # Extract Image URL
            img_el = card.locator('.cartoon-image img')
            c_image_url = img_el.get_attribute('src') or img_el.get_attribute('data-src')

            # Extract and Split Description (e.g., "गजब छ बा! - अविन")
            desc_el = card.locator('.cartoon-description p').first
            full_text = desc_el.inner_text().strip()

            if " - " in full_text:
                parts = full_text.split(" - ")
                c_title = parts[0].strip()
                c_author = parts[1].strip()
            else:
                c_title = full_text
                c_author = "अविन"

            results["cartoon_of_the_day"] = {
                "title": c_title,
                "image_url": c_image_url,
                "author": c_author
            }
            print(f"✓ Extracted Cartoon: {c_title} by {c_author}")

        except Exception as e:
            print(f"X Cartoon Error: {e}")
            page.screenshot(path="cartoon_error.png")

        # --- Final Output ---
        with open('ekantipur_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print("\n" + "="*30)
        print("Scraping Complete! Data saved to 'ekantipur_report.json'")
        print("="*30)

        browser.close()

if __name__ == "__main__":
    run_scraper()