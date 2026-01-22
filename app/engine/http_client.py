import requests
from typing import Dict, Any
from app.config import Settings

def fetch(url: str, settings: Settings) -> Dict[str, Any]:
    r = requests.get(
        url,
        timeout=settings.timeout_sec,
        headers={"User-Agent": settings.user_agent},
        allow_redirects=True,
        verify=settings.verify_tls,
    )
    return {
        "final_url": r.url,
        "status_code": r.status_code,
        "headers": dict(r.headers),
        "cookies": r.cookies,  # requests.cookies.RequestsCookieJar
        "text": r.text,
        "history": [h.status_code for h in r.history],
    }