import json
import os
from datetime import datetime

class Reporter:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.current_log_file = None

    def start_new_session(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = os.path.join(self.log_dir, f"scan_{timestamp}.jsonl")

    def log_result(self, result: dict):
        if not self.current_log_file:
            self.start_new_session()
        
        # Filter out boring results (optional, maybe configurable)
        # For now, log everything
        with open(self.current_log_file, "a") as f:
            f.write(json.dumps(result) + "\n")

    def format_for_gui(self, result: dict) -> tuple:
        """Returns (status, url, length, info)"""
        status = result.get("status", 0)
        url = result.get("url", "")
        length = result.get("length", 0)
        error = result.get("error")
        
        info = "Error" if error else "OK"
        if 200 <= status < 300:
            info = "Success"
        elif 300 <= status < 400:
            info = "Redirect"
        elif 400 <= status < 500:
            info = "Client Error"
        elif status >= 500:
            info = "Server Error"
            
        return (str(status), url, str(length), info)
