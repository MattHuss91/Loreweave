import os, json
from typing import Optional
import requests

LOCAL_VERSION = os.getenv("LOREWEAVE_VERSION", "1.0.0")
DEFAULT_UPDATE_URL = "https://raw.githubusercontent.com/CHANGE_ME_OWNER/CHANGE_ME_REPO/main/latest.json"

def get_latest_info() -> Optional[dict]:
    url = os.getenv("LOREWEAVE_UPDATE_URL", DEFAULT_UPDATE_URL)
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()
        if not isinstance(data, dict) or "version" not in data:
            return None
        return data
    except Exception:
        return None

def is_newer(remote: str, local: str) -> bool:
    def parse(v):
        return [int(p) if p.isdigit() else 0 for p in v.split(".")]
    a, b = parse(remote), parse(local)
    m = max(len(a), len(b))
    a += [0]*(m-len(a)); b += [0]*(m-len(b))
    return a > b
