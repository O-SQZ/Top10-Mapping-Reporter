from typing import Dict, Any, List

from app.models import CheckResult, ResultStatus, OwaspMapping
from app.owasp.mapping import OWASP_2025


def run_header_checks(ctx: Dict[str, Any]) -> List[CheckResult]:
    headers = {k.lower(): v for k, v in (ctx.get("headers") or {}).items()}
    results: List[CheckResult] = []

    # 공통 OWASP 매핑 (HDR 전 항목 공통)
    owasp_mapping = [
        OwaspMapping(
            "A02:2025",
            OWASP_2025["A02:2025"],
            "보안 관련 HTTP 헤더가 누락되었거나 충분히 구성되어 있지 않습니다.",
        )
    ]

    # ------------------------------------------------------------------
    # HDR-01: Strict-Transport-Security - [ PASS / MISSING ]
    # ------------------------------------------------------------------
    strict_transport_security = headers.get("strict-transport-security")
    if strict_transport_security:
        status = ResultStatus.PASS
        evidence = {"Strict-Transport-Security": strict_transport_security}
        note = "Strict-Transport-Security 헤더가 설정되어 있습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 Strict-Transport-Security 헤더를 찾을 수 없습니다."}
        note = "Strict-Transport-Security 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-01",
            check_name="Strict-Transport-Security 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # HDR-02: Content-Security-Policy - [ PASS / WEAK / MISSING ]
    # ------------------------------------------------------------------
    content_security_policy = headers.get("content-security-policy")
    if content_security_policy:
        weak_keywords = ["unsafe-inline", "unsafe-eval", "*"]
        if any(k in content_security_policy for k in weak_keywords):
            status = ResultStatus.WEAK
            note = "Content-Security-Policy 헤더가 존재하지만, 보안상 약한 지시문이 포함되어 있습니다."
        else:
            status = ResultStatus.PASS
            note = "Content-Security-Policy 헤더가 설정되어 있습니다."

        evidence = {"Content-Security-Policy": content_security_policy}
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 Content-Security-Policy 헤더를 찾을 수 없습니다."}
        note = "Content-Security-Policy 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-02",
            check_name="Content-Security-Policy 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # HDR-03: X-Frame-Options - [ PASS / MISSING ]
    # ------------------------------------------------------------------
    x_frame_options = headers.get("x-frame-options")
    if x_frame_options:
        status = ResultStatus.PASS
        evidence = {"X-Frame-Options": x_frame_options}
        note = "X-Frame-Options 헤더가 설정되어 있습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 X-Frame-Options 헤더를 찾을 수 없습니다."}
        note = "X-Frame-Options 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-03",
            check_name="X-Frame-Options 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # HDR-04: X-Content-Type-Options - [ PASS / MISSING ]
    # ------------------------------------------------------------------
    x_content_type_options = headers.get("x-content-type-options")
    if x_content_type_options:
        status = ResultStatus.PASS
        evidence = {"X-Content-Type-Options": x_content_type_options}
        note = "X-Content-Type-Options 헤더가 설정되어 있습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 X-Content-Type-Options 헤더를 찾을 수 없습니다."}
        note = "X-Content-Type-Options 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-04",
            check_name="X-Content-Type-Options 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # HDR-05: Referrer-Policy - [ PASS / MISSING ]
    # ------------------------------------------------------------------
    referrer_policy = headers.get("referrer-policy")
    if referrer_policy:
        status = ResultStatus.PASS
        evidence = {"Referrer-Policy": referrer_policy}
        note = "Referrer-Policy 헤더가 설정되어 있습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 Referrer-Policy 헤더를 찾을 수 없습니다."}
        note = "Referrer-Policy 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-05",
            check_name="Referrer-Policy 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # HDR-06: Permissions-Policy - [ PASS / MISSING ]
    # ------------------------------------------------------------------
    permissions_policy = headers.get("permissions-policy")
    if permissions_policy:
        status = ResultStatus.PASS
        evidence = {"Permissions-Policy": permissions_policy}
        note = "Permissions-Policy 헤더가 설정되어 있습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "설정된 Permissions-Policy 헤더를 찾을 수 없습니다."}
        note = "Permissions-Policy 헤더가 설정되어 있지 않습니다."

    results.append(
        CheckResult(
            check_id="HDR-06",
            check_name="Permissions-Policy 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    return results