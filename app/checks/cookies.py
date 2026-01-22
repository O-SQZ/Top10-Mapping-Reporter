from __future__ import annotations

from http.cookies import SimpleCookie
from typing import Dict, Any, List, Tuple

from app.models import CheckResult, ResultStatus, OwaspMapping
from app.owasp.mapping import OWASP_2025


def _split_set_cookie_header(set_cookie_value: str) -> List[str]:
    """
    결합된 Set-Cookie 헤더를 최대한 안전하게 분리하는 코드

    [원인]
    - 일부 HTTP 클라이언트/프록시/서버 스택에서는 여러 개의 `Set-Cookie` 헤더가 하나의 문자열로 합쳐져(콤마로 구분된 형태) 전달될 수 있음
    - 이때 단순히 `,`로 split 하면 `Expires=Wed, 21 Feb 2026 15:23:00 KST`처럼 날짜 포맷에 포함된 콤마까지 잘못 분리해 파싱이 깨질 수 있음

    [구성]
    - `", "`(콤마+공백)를 만났을 때, 그 뒤의 토큰이 "새 쿠키의 시작처럼 보이는지"를 간단한 규칙으로 추정하여 분리
    (e.g. 보통 새로운 쿠키는 example= 구조를 지님)
    """
    if not set_cookie_value:
        return []

    parts: List[str] = []
    current: List[str] = []
    i = 0
    length = len(set_cookie_value)

    while i < length:
        ch = set_cookie_value[i]
        # 분리 후보 경계: ", "
        if ch == "," and i + 1 < length and set_cookie_value[i + 1] == " ":
            # 이 콤마가 새 쿠키 시작인지 판별하기 위해 미리 살펴봄
            j = i + 2
            # 추가 공백 제거
            while j < length and set_cookie_value[j] == " ":
                j += 1

            # ';' 또는 ',' 전까지 토큰 읽기
            k = j
            while k < length and set_cookie_value[k] not in [";", ","]:
                k += 1

            token = set_cookie_value[j:k]
            # 토큰에 '='이 있고, Expires 날짜 조각처럼 보이지 않으면 새 쿠키 시작으로 추정
            looks_like_cookie_start = ("=" in token) and ("expires=" not in token.lower())

            if looks_like_cookie_start:
                parts.append("".join(current).strip())
                current = []
                i += 2
                continue

        current.append(ch)
        i += 1

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)

    return [p for p in parts if p]


def _parse_set_cookie_lines(headers: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
    # Set-Cookie 원문 라인과, 파싱된 쿠키 속성(dict) 목록을 반환합니다.
    raw_value = headers.get("set-cookie")
    if not raw_value:
        return [], []

    # 이미 리스트라면 그대로 사용하고, 문자열이라면 '안전 분리' 방식으로 분리합니다.
    if isinstance(raw_value, list):
        raw_lines = [str(x) for x in raw_value if x]
    else:
        raw_lines = _split_set_cookie_header(str(raw_value))

    parsed: List[Dict[str, Any]] = []

    for line in raw_lines:
        cookie = SimpleCookie()
        try:
            cookie.load(line)
        except Exception:
            continue

        for cookie_name, morsel in cookie.items():
            # Morsel 속성 키는 소문자 형태로 저장됩니다.
            parsed.append(
                {
                    "name": cookie_name,
                    "secure": bool(morsel["secure"]),
                    "httponly": bool(morsel["httponly"]),
                    "samesite": (morsel["samesite"] or "").strip() or None,
                    "path": (morsel["path"] or "").strip() or None,
                    "domain": (morsel["domain"] or "").strip() or None,
                    "raw": line,
                }
            )

    return raw_lines, parsed


def run_cookie_checks(ctx: Dict[str, Any]) -> List[CheckResult]:
    headers = {k.lower(): v for k, v in (ctx.get("headers") or {}).items()}
    results: List[CheckResult] = []

    # 공통 OWASP 매핑 (CK 전 항목 공통)
    owasp_mapping = [
        OwaspMapping(
            "A07:2025",
            OWASP_2025["A07:2025"],
            "인증 상태를 유지하는 쿠키 설정은 인증 실패(Authentication Failures)와 연관될 수 있습니다.",
        )
    ]

    raw_set_cookie_lines, parsed_cookies = _parse_set_cookie_lines(headers)

    # 쿠키가 없으면 CK 점검은 수행할 수 없음 
    if not parsed_cookies:
        common_evidence = {
            "detail": "Set-Cookie 헤더가 없거나 파싱 가능한 쿠키가 없어 점검을 수행할 수 없습니다.",
            "raw_set_cookie": raw_set_cookie_lines,
        }

        results.append(
            CheckResult(
                check_id="CK-01",
                check_name="Secure 속성 설정 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence=common_evidence,
                note="점검 가능한 쿠키가 없어 Secure 속성을 확인할 수 없습니다.",
            )
        )
        results.append(
            CheckResult(
                check_id="CK-02",
                check_name="HttpOnly 속성 설정 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence=common_evidence,
                note="점검 가능한 쿠키가 없어 HttpOnly 속성을 확인할 수 없습니다.",
            )
        )
        results.append(
            CheckResult(
                check_id="CK-03",
                check_name="SameSite 속성 설정 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence=common_evidence,
                note="점검 가능한 쿠키가 없어 SameSite 속성을 확인할 수 없습니다.",
            )
        )
        results.append(
            CheckResult(
                check_id="CK-04",
                check_name="Cookie Path/Domain 명시 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence=common_evidence,
                note="점검 가능한 쿠키가 없어 Path/Domain 속성을 확인할 수 없습니다.",
            )
        )

        return results

    cookie_names = [c["name"] for c in parsed_cookies]

    # ------------------------------------------------------------------
    # CK-01: Secure - [ PASS / MISSING / WEAK ]
    # ------------------------------------------------------------------
    secure_missing = [c["name"] for c in parsed_cookies if not c["secure"]]
    if len(secure_missing) == 0:
        status = ResultStatus.PASS
        note = "모든 쿠키에 Secure 속성이 설정되어 있습니다."
    elif len(secure_missing) == len(parsed_cookies):
        status = ResultStatus.MISSING
        note = "모든 쿠키에서 Secure 속성이 확인되지 않습니다."
    else:
        status = ResultStatus.WEAK
        note = "일부 쿠키에서 Secure 속성이 확인되지 않습니다."

    results.append(
        CheckResult(
            check_id="CK-01",
            check_name="Secure 속성 설정 여부",
            status=status,
            owasp=owasp_mapping,
            evidence={
                "cookies": parsed_cookies,
                "summary": {
                    "total": len(parsed_cookies),
                    "cookie_names": cookie_names,
                    "missing_secure": secure_missing,
                },
            },
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # CK-02: HttpOnly - [ PASS / MISSING / WEAK ]
    # ------------------------------------------------------------------
    http_only_missing = [c["name"] for c in parsed_cookies if not c["httponly"]]
    if len(http_only_missing) == 0:
        status = ResultStatus.PASS
        note = "모든 쿠키에 HttpOnly 속성이 설정되어 있습니다."
    elif len(http_only_missing) == len(parsed_cookies):
        status = ResultStatus.MISSING
        note = "모든 쿠키에서 HttpOnly 속성이 확인되지 않습니다."
    else:
        status = ResultStatus.WEAK
        note = "일부 쿠키에서 HttpOnly 속성이 확인되지 않습니다."

    results.append(
        CheckResult(
            check_id="CK-02",
            check_name="HttpOnly 속성 설정 여부",
            status=status,
            owasp=owasp_mapping,
            evidence={
                "cookies": parsed_cookies,
                "summary": {
                    "total": len(parsed_cookies),
                    "cookie_names": cookie_names,
                    "missing_httponly": http_only_missing,
                },
            },
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # CK-03: SameSite - [ PASS / MISSING / WEAK ]
    # ------------------------------------------------------------------
    samesite_missing = [c["name"] for c in parsed_cookies if not c["samesite"]]
    # v0.1: SameSite=None은 '존재'하긴 하지만 주의 필요 -> WEAK로 취급
    samesite_none = [c["name"] for c in parsed_cookies if (c["samesite"] or "").lower() == "none"]

    if len(samesite_missing) == 0 and len(samesite_none) == 0:
        status = ResultStatus.PASS
        note = "모든 쿠키에 SameSite 속성이 설정되어 있습니다."
    elif len(samesite_missing) == len(parsed_cookies):
        status = ResultStatus.MISSING
        note = "모든 쿠키에서 SameSite 속성이 확인되지 않습니다."
    else:
        status = ResultStatus.WEAK
        if len(samesite_none) > 0:
            note = "일부 쿠키에서 SameSite=None이 확인되어 추가 검토가 필요합니다."
        else:
            note = "일부 쿠키에서 SameSite 속성이 확인되지 않습니다."

    results.append(
        CheckResult(
            check_id="CK-03",
            check_name="SameSite 속성 설정 여부",
            status=status,
            owasp=owasp_mapping,
            evidence={
                "cookies": parsed_cookies,
                "summary": {
                    "total": len(parsed_cookies),
                    "cookie_names": cookie_names,
                    "missing_samesite": samesite_missing,
                    "samesite_none": samesite_none,
                },
            },
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # CK-04: Path / Domain - [ PASS / MISSING / WEAK ]
    # ------------------------------------------------------------------
    # v0.1: Path 또는 Domain 둘 중 하나라도 명시되면 '명시됨'으로 처리
    path_or_domain_missing = [
        c["name"]
        for c in parsed_cookies
        if not (c["path"] or c["domain"])
    ]

    if len(path_or_domain_missing) == 0:
        status = ResultStatus.PASS
        note = "모든 쿠키에 Path 또는 Domain 속성이 명시되어 있습니다."
    elif len(path_or_domain_missing) == len(parsed_cookies):
        status = ResultStatus.MISSING
        note = "모든 쿠키에서 Path/Domain 속성이 명시되지 않았습니다."
    else:
        status = ResultStatus.WEAK
        note = "일부 쿠키에서 Path/Domain 속성이 명시되지 않았습니다."

    results.append(
        CheckResult(
            check_id="CK-04",
            check_name="Cookie Path/Domain 명시 여부",
            status=status,
            owasp=owasp_mapping,
            evidence={
                "cookies": parsed_cookies,
                "summary": {
                    "total": len(parsed_cookies),
                    "cookie_names": cookie_names,
                    "missing_path_or_domain": path_or_domain_missing,
                },
            },
            note=note,
        )
    )

    return results