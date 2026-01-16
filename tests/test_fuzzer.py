import pytest
import asyncio
from src.engine.fuzzer import Fuzzer
from src.utils.security import is_valid_url

def test_fuzzer_initialization():
    fuzzer = Fuzzer("http://example.com")
    assert fuzzer.target_url == "http://example.com"
    assert fuzzer.concurrency == 10

def test_invalid_url_validation():
    assert is_valid_url("not_a_url") == False
    assert is_valid_url("http://google.com") == True

def test_fuzzer_scan_directory_invalid_url():
    fuzzer = Fuzzer("invalid_url")
    # This shouldn't raise exception, just log error internally or return
    asyncio.run(fuzzer.scan_directory())
    assert fuzzer.is_running == False

def test_payload_loading():
    from src.engine.payloads import PayloadManager
    pm = PayloadManager()
    assert len(pm.get_payloads("sqli")) > 0
    assert len(pm.get_payloads("xss")) > 0
