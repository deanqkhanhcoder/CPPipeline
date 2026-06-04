import argparse
import json
import traceback
import sys
import asyncio
import time

def check_cloudflare(html):
    if not html:
        return False
    if "cdn-cgi/challenge-platform" in html or "Just a moment" in html or "__CF$cv$params" in html:
        return True
    return False

def crawl_with_brave(url, retries=2):
    for attempt in range(retries):
        print(f"[Brave] Attempt {attempt+1}/{retries}...", file=sys.stderr)
        try:
            from playwright.sync_api import sync_playwright
            BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            USER_DATA = r"C:\Users\toanpq\AppData\Local\BraveSoftware\Brave-Browser\User Data"
            
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
                        return None # No need to retry if it's locked
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
                
                if check_cloudflare(html):
                    print("[Brave] Cloudflare detected.", file=sys.stderr)
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
                # Wait longer for cloudflare to resolve if it's a challenge page
                page.wait_for_selector(".problem-statement", timeout=10000)
            except:
                pass
            title = page.title()
            html = page.content()
            browser.close()
            
            if check_cloudflare(html):
                print("[CloakBrowser] Cloudflare detected.", file=sys.stderr)
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
                
                if check_cloudflare(html):
                    print("[Playwright Stealth] Cloudflare detected.", file=sys.stderr)
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
                        if check_cloudflare(res.html):
                            print("[Crawl4AI] Cloudflare detected.", file=sys.stderr)
                            await asyncio.sleep(2)
                            continue
                        return {"url": url, "html": res.html, "markdown": res.markdown, "title": ""}
            except Exception as e:
                print(f"[Crawl4AI] Error: {e}", file=sys.stderr)
                await asyncio.sleep(2)
        return None
    return asyncio.run(run())

def crawl_problem(url: str) -> dict:
    res = crawl_with_brave(url)
    if res: return res
    
    res = crawl_with_cloakbrowser(url)
    if res: return res
    
    res = crawl_with_playwright_stealth(url)
    if res: return res
    
    res = crawl_with_crawl4ai(url)
    if res: return res
    
    return {"url": url, "html": "Error: All crawling engines failed. Brave profile locked, and fallbacks hit Cloudflare.", "markdown": ""}

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()
    res = crawl_problem(args.url)
    print(json.dumps(res, ensure_ascii=False))
