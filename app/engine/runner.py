# app/engine/runner.py

from typing import List, Tuple, Dict, Any
from app.config import Settings
from app.models import CheckResult
from app.engine.http_client import fetch
from app.checks.headers import run_header_checks
from app.checks.exposure import run_exposure_checks
from app.checks.cookies import run_cookie_checks

def run_checks_with_context(url: str, settings: Settings | None = None) -> Tuple[Dict[str, Any], List[CheckResult]]:
    settings = settings or Settings()
    ctx = fetch(url, settings)

    results: List[CheckResult] = []
    results.extend(run_header_checks(ctx))
    results.extend(run_exposure_checks(ctx))
    results.extend(run_cookie_checks(ctx))

    return ctx, results