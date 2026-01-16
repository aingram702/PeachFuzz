import asyncio
import aiohttp
from typing import List, Callable, Optional
from src.utils.security import is_valid_url, get_domain
from src.engine.payloads import PayloadManager

class Fuzzer:
    def __init__(self, target_url: str, concurrency: int = 10, timeout: int = 5, 
                 proxy: Optional[str] = None, headers: Optional[dict] = None,
                 reporter_callback: Optional[Callable] = None):
        self.target_url = target_url
        self.concurrency = concurrency
        self.timeout = timeout
        self.proxy = proxy
        self.headers = headers or {}
        self.reporter = reporter_callback
        self.payload_manager = PayloadManager()
        self.is_running = False
        self.session = None

    async def _make_request(self, method: str, url: str, data: dict = None) -> dict:
        if not self.session:
            return {"error": "Session not initialized"}
        
        try:
            # Prepare headers (merge default with custom if needed, but here we just use custom)
            headers = self.headers.copy()
            if data and method == 'POST':
               # aiohttp handles content-type for data=dict, strictly speaking
               pass

            async with self.session.request(method, url, data=data, headers=headers, 
                                          proxy=self.proxy, timeout=self.timeout) as response:
                text = await response.text()
                return {
                    "url": url,
                    "method": method,
                    "status": response.status,
                    "length": len(text),
                    "payload": data or "",
                    "response": text
                }
        except Exception as e:
            return {"url": url, "method": method, "error": str(e), "status": 0, "length": 0}

    async def _worker(self, queue: asyncio.Queue):
        while self.is_running and not queue.empty():
            task = await queue.get()
            url = task.get('url')
            method = task.get('method', 'GET')
            payload = task.get('payload')
            
            # If payload is for params, append to URL or body
            target = url
            data = None
            
            if method in ['GET', 'DELETE']:
                if payload:
                    if '?' in target:
                        target += f"&fuzz={payload}"
                    else:
                        target += f"?fuzz={payload}"
            elif method in ['POST', 'PUT', 'PATCH']:
                if payload:
                    data = {'fuzz': payload}
            
            # For HEAD/OPTIONS we might just fuzz URL params or headers, but basic logic here
            
            result = await self._make_request(method, target, data)
            
            if self.reporter:
                self.reporter(result)
            
            queue.task_done()

    async def scan_directory(self, method: str = "GET"):
        """Standard directory brute-force."""
        if not is_valid_url(self.target_url):
            if self.reporter:
                self.reporter({"error": "Invalid URL"})
            return

        self.is_running = True
        queue = asyncio.Queue()
        
        # Load payloads
        dirs = self.payload_manager.get_payloads("directory")
        base_url = self.target_url.rstrip('/')
        
        for d in dirs:
            queue.put_nowait({"url": f"{base_url}/{d}", "method": method})

        async with aiohttp.ClientSession() as session:
            self.session = session
            workers = [asyncio.create_task(self._worker(queue)) for _ in range(self.concurrency)]
            await asyncio.gather(*workers)
        
        self.is_running = False

    async def fuzz_parameters(self, method: str = "GET", vuln_type: str = "sqli"):
        """Fuzz parameters with specific vulnerability payloads."""
        if not is_valid_url(self.target_url):
            return

        self.is_running = True
        queue = asyncio.Queue()
        
        payloads = self.payload_manager.get_payloads(vuln_type)
        
        for p in payloads:
            queue.put_nowait({"url": self.target_url, "method": method, "payload": p})

        async with aiohttp.ClientSession() as session:
            self.session = session
            workers = [asyncio.create_task(self._worker(queue)) for _ in range(self.concurrency)]
            await asyncio.gather(*workers)
        
        self.is_running = False

    def stop(self):
        self.is_running = False
