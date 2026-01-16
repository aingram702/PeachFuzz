import json
import csv
import os
from datetime import datetime

def export_to_json(results: list, filepath: str):
    """Exports list of result dicts to JSON."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False

def export_to_csv(results: list, filepath: str):
    """Exports list of result dicts to CSV."""
    if not results:
        return False
        
    try:
        keys = results[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False
