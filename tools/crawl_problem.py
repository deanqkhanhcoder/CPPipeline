import argparse
import json
import traceback
import sys
import asyncio
import time
import os
from datetime import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stdin.encoding.lower() != 'utf-8':
    sys.stdin.reconfigure(encoding='utf-8')

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
        return True, False, "Empty content"
    if "class=\"problem-statement\"" in html or "class='problem-statement'" in html or "problem-statement" in html:
        return False, False, "" # Valid problem page
    if "404 Not Found" in html or "Page not found" in html or "No such problem" in html:
        return False, True, "404 Not Found (Fatal)"
    if "No problem with such id" in html or "does not exist" in html:
        return False, True, "Problem does not exist (Fatal)"
    if "<title>Just a moment...</title>" in html or "Enable JavaScript and cookies to continue" in html:
        return True, False, "Cloudflare challenge detected"
    if "Access denied" in html or "403 Forbidden" in html:
        return True, False, "Access denied"
    if "Too many requests" in html or "Rate limit" in html:
        return True, False, "Rate limit exceeded"
    if "Login required" in html or "Please login" in html:
        return True, False, "Login required"
    return False, False, ""

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "browser_headless": False,
        "browser_timeout_ms": 20000,
        "max_retries": 2,
        "health_check_every": 25,
        "politeness_delay_min_ms": 1000,
        "politeness_delay_max_ms": 2500
    }

class PersistentBrowserManager:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
        
    def __init__(self):
        self.config = load_config()
        self.playwright = None
        self.browser = None
        self.context = None
        self.jobs_count = 0
        
    def _init_browser(self):
        if self.browser or self.context:
            self.close()
            
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(
            headless=self.config.get("browser_headless", False),
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.jobs_count = 0
        
    def fetch_page(self, url):
        self.jobs_count += 1
        if self.jobs_count > self.config.get("health_check_every", 25):
            print("[Persistent Browser] Health Check: Recycling browser context...", file=sys.stderr)
            self._init_browser()
            
        retries = self.config.get("max_retries", 2)
        for attempt in range(retries):
            print(f"[Persistent Browser] Attempt {attempt+1}/{retries}...", file=sys.stderr)
            try:
                if not self.context:
                    self._init_browser()
                
                page = self.context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=self.config.get("browser_timeout_ms", 20000))
                try:
                    page.wait_for_selector(".problem-statement", timeout=10000)
                except:
                    pass
                html = page.content()
                title = page.title()
                page.close()
                
                is_chal, is_fatal, reason = check_challenge(html)
                if is_fatal:
                    print(f"[Persistent Browser] Fatal: {reason}", file=sys.stderr)
                    return {"url": url, "html": f"Error: {reason}", "markdown": "", "title": title, "fatal": True}
                if is_chal:
                    print(f"[Persistent Browser] Challenge: {reason}", file=sys.stderr)
                    save_debug_snapshot(url, title, html, "PersistentBrowser")
                    time.sleep(2)
                    continue
                    
                import random
                min_delay = self.config.get("politeness_delay_min_ms", 1000) / 1000.0
                max_delay = self.config.get("politeness_delay_max_ms", 2500) / 1000.0
                time.sleep(random.uniform(min_delay, max_delay))
                
                return {"url": url, "html": html, "markdown": "", "title": title, "engine_used": "PersistentBrowser"}
            except Exception as e:
                print(f"[Persistent Browser] Error: {e}", file=sys.stderr)
                if "Target closed" in str(e) or "Connection closed" in str(e):
                    self._init_browser()
                time.sleep(2)
        return None
        
    def close(self):
        try:
            if self.context: self.context.close()
        except: pass
        try:
            if self.browser: self.browser.close()
        except: pass
        try:
            if self.playwright: self.playwright.stop()
        except: pass
        self.context = None
        self.browser = None
        self.playwright = None

def crawl_with_brave(url, retries=2):
    for attempt in range(retries):
        print(f"[Brave] Attempt {attempt+1}/{retries}...", file=sys.stderr)
        try:
            from playwright.sync_api import sync_playwright
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
                        print("\n[CẢNH BÁO] Brave Profile đang bị khóa bởi một phiên làm việc khác!", file=sys.stderr)
                        print("[CẢNH BÁO] Vui lòng ĐÓNG TRÌNH DUYỆT BRAVE trong vòng 60 giây để tiếp tục...", file=sys.stderr)
                        for i in range(60, 0, -5):
                            print(f"... Đang chờ {i} giây", file=sys.stderr)
                            time.sleep(5)
                        print("[Brave] Thử lại sau khi chờ...", file=sys.stderr)
                        continue
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
                
                is_chal, is_fatal, reason = check_challenge(html)
                if is_fatal:
                    print(f"[Brave] Fatal: {reason}", file=sys.stderr)
                    return {"url": url, "html": f"Error: {reason}", "markdown": "", "title": title, "fatal": True}
                if is_chal:
                    print(f"[Brave] Challenge: {reason}", file=sys.stderr)
                    save_debug_snapshot(url, title, html, "Brave")
                    time.sleep(2)
                    continue
                    
                return {"url": url, "html": html, "markdown": "", "title": title, "engine_used": "Brave"}
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
            
            is_chal, is_fatal, reason = check_challenge(html)
            if is_fatal:
                print(f"[CloakBrowser] Fatal: {reason}", file=sys.stderr)
                return {"url": url, "html": f"Error: {reason}", "markdown": "", "title": title, "fatal": True}
            if is_chal:
                print(f"[CloakBrowser] Challenge: {reason}", file=sys.stderr)
                save_debug_snapshot(url, title, html, "CloakBrowser")
                time.sleep(3)
                continue
                
            return {"url": url, "html": html, "markdown": "", "title": title, "engine_used": "CloakBrowser"}
        except Exception as e:
            print(f"[CloakBrowser] Error: {e}", file=sys.stderr)
            time.sleep(3)
    return None

def crawl_with_playwright_stealth(url, retries=2):
    # Use the PersistentBrowserManager for lightning fast crawling and automatic recovery
    manager = PersistentBrowserManager.get_instance()
    return manager.fetch_page(url)

def crawl_with_crawl4ai(url, retries=2):
    async def run():
        for attempt in range(retries):
            print(f"[Crawl4AI] Attempt {attempt+1}/{retries}...", file=sys.stderr)
            try:
                from crawl4ai import AsyncWebCrawler
                async with AsyncWebCrawler() as crawler:
                    res = await crawler.arun(url)
                    if res and res.html:
                        is_chal, is_fatal, reason = check_challenge(res.html)
                        if is_fatal:
                            print(f"[Crawl4AI] Fatal: {reason}", file=sys.stderr)
                            return {"url": url, "html": f"Error: {reason}", "markdown": "", "title": "", "fatal": True}
                        if is_chal:
                            print(f"[Crawl4AI] Challenge: {reason}", file=sys.stderr)
                            save_debug_snapshot(url, "", res.html, "Crawl4AI")
                            await asyncio.sleep(2)
                            continue
                        return {"url": url, "html": res.html, "markdown": res.markdown, "title": "", "engine_used": "Crawl4AI"}
            except Exception as e:
                print(f"[Crawl4AI] Error: {e}", file=sys.stderr)
                await asyncio.sleep(2)
        return None
    return asyncio.run(run())

def is_pdf(url):
    if url.lower().endswith(".pdf"):
        return True
    try:
        import requests
        resp = requests.head(url, timeout=10, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            return True
    except Exception:
        pass
    return False

def crawl_pdf(url):
    import requests
    import fitz  # PyMuPDF
    from cache_manager import get_problem_id
    
    print(f"[PDF Crawler] Downloading PDF from {url}...", file=sys.stderr)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        if resp.status_code != 200:
            print(f"[PDF Crawler] HTTP {resp.status_code} Error", file=sys.stderr)
            return None
            
        pid = get_problem_id(url)
        os.makedirs("cache/pdf", exist_ok=True)
        os.makedirs("cache/pdf_images", exist_ok=True)
        
        pdf_path = f"cache/pdf/{pid}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(resp.content)
            
        print(f"[PDF Crawler] PDF saved to {pdf_path}. Converting to images...", file=sys.stderr)
        
        doc = fitz.open(pdf_path, encoding="utf-8")
        image_paths = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            img_path = f"cache/pdf_images/{pid}_page_{page_num+1:03d}.png"
            pix.save(img_path)
            image_paths.append(img_path)
            
        return {
            "url": url,
            "title": f"PDF Document {pid}",
            "html": f"PDF Document converted to {len(image_paths)} images.",
            "markdown": "",
            "type": "pdf",
            "pdf_path": pdf_path,
            "images": image_paths,
            "engine_used": "PDFCrawler"
        }
    except Exception as e:
        print(f"[PDF Crawler] Error: {e}", file=sys.stderr)
        return None

def crawl_problem(url: str, order_index: int = 0) -> dict:
    from cache_manager import lookup_cache, save_cache
    
    # PHASE 2: CACHE LOOKUP LAYER
    cached_data = lookup_cache(url)
    if cached_data:
        print("[Cache] HIT - Returning cached content", file=sys.stderr)
        cached_data["engine_used"] = "Cache"
        return cached_data
        
    print("[Cache] MISS - Starting Smart Crawler Flow", file=sys.stderr)
    
    res = None
    if is_pdf(url):
        res = crawl_pdf(url)
    
    if not res:
        # PHASE 3: SMART CRAWLER FLOW
        # Prioritize stealth (PersistentBrowserManager) for speed
        for engine in [crawl_with_playwright_stealth, crawl_with_brave, crawl_with_cloakbrowser, crawl_with_crawl4ai]:
            res = engine(url)
            if res:
                if res.get("fatal"):
                    return res
                if not res["html"].startswith("Error:"):
                    break
    
    if res and not res["html"].startswith("Error:"):
        # PHASE 7: AUTO CACHE AFTER SUCCESS
        content_type = res.get("type", "html")
        pdf_path = res.get("pdf_path", None)
        images = res.get("images", [])
        save_cache(
            url=res["url"], 
            title=res["title"], 
            html=res["html"], 
            markdown=res.get("markdown", ""),
            content_type=content_type,
            pdf_path=pdf_path,
            images=images,
            order_index=order_index
        )
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
