import argparse
import json
import traceback
import sys
import asyncio
import time
import os
from datetime import datetime

def save_debug_snapshot(url, title, html, crawler_name):
    try:
        os.makedirs("cache/debug", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = crawler_name.replace(" ", "_").lower()
        filename = f"cache/debug/fail_{safe_name}_{timestamp}.json"
        
        snapshot = {
            "url": url,
            "title": title,
            "timestamp": timestamp,
            "crawler_backend": crawler_name,
            "html_preview": html[:2000] if html else ""
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        print(f"[{crawler_name}] Debug snapshot saved to {filename}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to save debug snapshot: {e}", file=sys.stderr)

def check_challenge(html):
    if not html or len(html.strip()) < 50:
        return True, "Empty content"
    if "class=\"problem-statement\"" in html or "class='problem-statement'" in html or "problem-statement" in html:
        return False, "" # Valid problem page
    if "<title>Just a moment...</title>" in html or "Enable JavaScript and cookies to continue" in html:
        return True, "Cloudflare challenge detected"
    if "Access denied" in html or "403 Forbidden" in html:
        return True, "Access denied"
    if "Too many requests" in html or "Rate limit" in html:
        return True, "Rate limit exceeded"
    if "Login required" in html or "Please login" in html:
        return True, "Login required"
    return False, ""

def crawl_with_brave(url, retries=2):
    for attempt in range(retries):
        print(f"[Brave] Attempt {attempt+1}/{retries}...", file=sys.stderr)
        try:
            from playwright.sync_api import sync_playwright
            # Auto-discovery for Windows, Linux, MacOS
            BRAVE_PATH = os.environ.get("BRAVE_PATH")
            if not BRAVE_PATH:
                if sys.platform == "win32":
                    BRAVE_PATH = os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "BraveSoftware", "Brave-Browser", "Application", "brave.exe")
                elif sys.platform == "darwin":
                    BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
                else:
                    BRAVE_PATH = "/usr/bin/brave-browser"
            
            USER_DATA = os.environ.get("BRAVE_USER_DATA")
            if not USER_DATA:
                if sys.platform == "win32":
                    USER_DATA = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local")), "BraveSoftware", "Brave-Browser", "User Data")
                elif sys.platform == "darwin":
                    USER_DATA = os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser")
                else:
                    USER_DATA = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser")
            
            if not os.path.exists(BRAVE_PATH):
                print(f"[Brave] Executable not found at {BRAVE_PATH}. Disabling Brave backend.", file=sys.stderr)
                return None
            
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch_persistent_context(
                        user_data_dir=USER_DATA,
                        executable_path=BRAVE_PATH,
                        headless=False,
                        args=["--disable-blink-features=AutomationControlled"]
                    )
                except Exception as e:
                    if "Opening in existing browser session" in str(e):
                        print("[Brave] Profile locked by an active session.", file=sys.stderr)
                        return None
                    raise e
                    
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                try:
                    page.wait_for_selector(".problem-statement", timeout=10000)
                except:
                    pass
                html = page.content()
                title = page.title()
                browser.close()
                
                is_chal, reason = check_challenge(html)
                if is_chal:
                    print(f"[Brave] Challenge: {reason}", file=sys.stderr)
                    save_debug_snapshot(url, title, html, "Brave")
                    time.sleep(2)
                    continue
                    
                return {"url": url, "html": html, "markdown": "", "title": title}
        except Exception as e:
            print(f"[Brave] Error: {e}", file=sys.stderr)
            time.sleep(2)
    return None

def crawl_with_cloakbrowser(url, retries=3):
    for attempt in range(retries):
        print(f"[CloakBrowser] Attempt {attempt+1}/{retries}...", file=sys.stderr)
        try:
            from cloakbrowser import launch
            browser = launch()
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            try:
                page.wait_for_selector(".problem-statement", timeout=10000)
            except:
                pass
            title = page.title()
            html = page.content()
            browser.close()
            
            is_chal, reason = check_challenge(html)
            if is_chal:
                print(f"[CloakBrowser] Challenge: {reason}", file=sys.stderr)
                save_debug_snapshot(url, title, html, "CloakBrowser")
                time.sleep(3)
                continue
                
            return {"url": url, "html": html, "markdown": "", "title": title}
        except Exception as e:
            print(f"[CloakBrowser] Error: {e}", file=sys.stderr)
            time.sleep(3)
    return None

def crawl_with_playwright_stealth(url, retries=2):
    for attempt in range(retries):
        print(f"[Playwright Stealth] Attempt {attempt+1}/{retries}...", file=sys.stderr)
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=False,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                try:
                    page.wait_for_selector(".problem-statement", timeout=10000)
                except:
                    pass
                html = page.content()
                title = page.title()
                browser.close()
                
                is_chal, reason = check_challenge(html)
                if is_chal:
                    print(f"[Playwright Stealth] Challenge: {reason}", file=sys.stderr)
                    save_debug_snapshot(url, title, html, "Playwright Stealth")
                    time.sleep(2)
                    continue
                    
                return {"url": url, "html": html, "markdown": "", "title": title}
        except Exception as e:
            print(f"[Playwright Stealth] Error: {e}", file=sys.stderr)
            time.sleep(2)
    return None

def crawl_with_crawl4ai(url, retries=2):
    async def run():
        for attempt in range(retries):
            print(f"[Crawl4AI] Attempt {attempt+1}/{retries}...", file=sys.stderr)
            try:
                from crawl4ai import AsyncWebCrawler
                async with AsyncWebCrawler() as crawler:
                    res = await crawler.arun(url)
                    if res and res.html:
                        is_chal, reason = check_challenge(res.html)
                        if is_chal:
                            print(f"[Crawl4AI] Challenge: {reason}", file=sys.stderr)
                            save_debug_snapshot(url, "", res.html, "Crawl4AI")
                            await asyncio.sleep(2)
                            continue
                        return {"url": url, "html": res.html, "markdown": res.markdown, "title": ""}
            except Exception as e:
                print(f"[Crawl4AI] Error: {e}", file=sys.stderr)
                await asyncio.sleep(2)
        return None
    return asyncio.run(run())

def crawl_problem(url: str) -> dict:
    from cache_manager import lookup_cache, save_cache
    
    # PHASE 2: CACHE LOOKUP LAYER
    cached_data = lookup_cache(url)
    if cached_data:
        print("[Cache] HIT - Returning cached content", file=sys.stderr)
        return cached_data
        
    print("[Cache] MISS - Starting Smart Crawler Flow", file=sys.stderr)
    
    # PHASE 3: SMART CRAWLER FLOW
    res = crawl_with_brave(url)
    if not res: res = crawl_with_cloakbrowser(url)
    if not res: res = crawl_with_playwright_stealth(url)
    if not res: res = crawl_with_crawl4ai(url)
    
    if res and not res["html"].startswith("Error:"):
        # PHASE 7: AUTO CACHE AFTER SUCCESS
        save_cache(res["url"], res["title"], res["html"], res["markdown"])
        res["_cached"] = True
        return res
    
    return {"url": url, "html": "Error: All crawling engines failed. Target is actively blocking requests.", "markdown": ""}

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()
    res = crawl_problem(args.url)
    print(json.dumps(res, ensure_ascii=False))
