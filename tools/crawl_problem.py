import argparse
import json
import traceback
import sys
import asyncio

def crawl_with_cloakbrowser(url):
    print("Trying CloakBrowser...", file=sys.stderr)
    try:
        from cloakbrowser import launch
        browser = launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_selector(".problem-statement", timeout=5000)
        except:
            pass
        title = page.title()
        html = page.content()
        browser.close()
        
        # Check if still blocked
        if "Just a moment" in title or "Cloudflare" in title:
            print("CloakBrowser got blocked by Cloudflare.", file=sys.stderr)
            return None
            
        return {"url": url, "html": html, "markdown": "", "title": title}
    except Exception as e:
        print(f"CloakBrowser failed: {e}", file=sys.stderr)
    return None

def crawl_with_crawl4ai(url):
    print("Trying Crawl4AI...", file=sys.stderr)
    async def run():
        try:
            from crawl4ai import AsyncWebCrawler
            async with AsyncWebCrawler() as crawler:
                res = await crawler.arun(url)
                if res and res.html:
                    return {"url": url, "html": res.html, "markdown": res.markdown, "title": ""}
        except Exception as e:
            print(f"Crawl4AI failed: {e}", file=sys.stderr)
        return None
    return asyncio.run(run())

def crawl_with_playwright(url):
    print("Trying Playwright (headless=False)...", file=sys.stderr)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
            try:
                page.wait_for_selector(".problem-statement", timeout=5000)
            except:
                pass
            html = page.content()
            title = page.title()
            browser.close()
            return {"url": url, "html": html, "markdown": "", "title": title}
    except Exception as e:
        print(f"Playwright failed: {e}", file=sys.stderr)
    return None

def crawl_with_requests(url):
    print("Trying Requests...", file=sys.stderr)
    try:
        import requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return {"url": url, "html": res.text, "markdown": ""}
    except Exception as e:
        print(f"Requests failed: {e}", file=sys.stderr)
    return None

def crawl_problem(url: str) -> dict:
    # Strategy Priority
    res = crawl_with_cloakbrowser(url)
    if res: return res
    
    res = crawl_with_crawl4ai(url)
    if res: return res
    
    res = crawl_with_playwright(url)
    if res: return res
    
    res = crawl_with_requests(url)
    if res: return res
    
    return {"url": url, "html": "Error: All crawling engines failed.", "markdown": ""}

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()
    res = crawl_problem(args.url)
    print(json.dumps(res, ensure_ascii=False))
