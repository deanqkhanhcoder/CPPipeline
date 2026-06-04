import sys
from playwright.sync_api import sync_playwright

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
USER_DATA = r"C:\Users\toanpq\AppData\Local\BraveSoftware\Brave-Browser\User Data"

def test_brave(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA,
                executable_path=BRAVE_PATH,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            # Create a new page instead of using the default one if preferred, 
            # but launch_persistent_context already creates one page by default.
            page = browser.pages[0] 
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            try:
                page.wait_for_selector(".problem-statement", timeout=5000)
            except:
                pass
            html = page.content()
            title = page.title()
            
            blocked = "cdn-cgi/challenge-platform" in html or "Just a moment" in html or "__CF$cv$params" in html
            print(f"Title: {title}")
            print(f"Cloudflare Blocked: {blocked}")
            browser.close()
    except Exception as e:
        print(f"Brave Error: {e}")

if __name__ == "__main__":
    test_brave("https://codeforces.com/contest/1777/problem/C")
