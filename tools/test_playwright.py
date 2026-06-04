import sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed")
    sys.exit(1)

def test():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://codeforces.com")
            title = page.title()
            print(f"Playwright Test - Title: {title}")
            browser.close()
    except Exception as e:
        print(f"Playwright Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test()
