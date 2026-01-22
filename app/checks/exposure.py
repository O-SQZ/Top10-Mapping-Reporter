from typing import Dict, Any, List

import requests

from app.models import CheckResult, ResultStatus, OwaspMapping
from app.owasp.mapping import OWASP_2025


def run_exposure_checks(ctx: Dict[str, Any]) -> List[CheckResult]:
    headers = {k.lower(): v for k, v in (ctx.get("headers") or {}).items()}
    final_url = ctx.get("final_url")
    # 추가 요청 기반 점검 결과(robots.txt, sitemap.xml 등)를 context.json에 함께 저장하기 위한 공간
    if "context_checks" not in ctx or not isinstance(ctx.get("context_checks"), dict):
        ctx["context_checks"] = {}
    results: List[CheckResult] = []

    # 공통 OWASP 매핑 (EXP 전 항목 공통)
    owasp_mapping = [
        OwaspMapping(
            "A02:2025",
            OWASP_2025["A02:2025"],
            "불필요한 정보 노출은 보안 설정 관리 측면의 문제로 분류될 수 있습니다.",
        )
    ]

    # ------------------------------------------------------------------
    # EXP-01: Server 헤더 노출 여부 - [ OBSERVED / MISSING ]
    # ------------------------------------------------------------------
    server_header = headers.get("server")
    if server_header:
        status = ResultStatus.OBSERVED
        evidence = {"Server": server_header}
        note = "Server 헤더가 식별되었습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "Server 헤더를 찾을 수 없습니다."}
        note = "Server 헤더가 식별되지 않았습니다."

    results.append(
        CheckResult(
            check_id="EXP-01",
            check_name="Server 헤더 노출 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # EXP-02: X-Powered-By 헤더 노출 여부 - [ OBSERVED / MISSING ]
    # ------------------------------------------------------------------
    x_powered_by_header = headers.get("x-powered-by")
    if x_powered_by_header:
        status = ResultStatus.OBSERVED
        evidence = {"X-Powered-By": x_powered_by_header}
        note = "X-Powered-By 헤더가 식별되었습니다."
    else:
        status = ResultStatus.MISSING
        evidence = {"detail": "X-Powered-By 헤더를 찾을 수 없습니다."}
        note = "X-Powered-By 헤더가 식별되지 않았습니다."

    results.append(
        CheckResult(
            check_id="EXP-02",
            check_name="X-Powered-By 헤더 노출 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # robots.txt / sitemap.xml 관련 추후 설정 필요 (데모웹 구현 쪽)
    if not final_url or not isinstance(final_url, str):
        # final_url이 없으면 요청 기반 점검은 진행 불가
        results.append(
            CheckResult(
                check_id="EXP-03",
                check_name="robots.txt 존재 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence={"detail": "final_url 정보가 없어 robots.txt 점검을 수행할 수 없습니다."},
                note="점검에 필요한 URL 정보가 부족합니다.",
            )
        )
        results.append(
            CheckResult(
                check_id="EXP-04",
                check_name="sitemap.xml 존재 여부",
                status=ResultStatus.NOT_TESTED,
                owasp=owasp_mapping,
                evidence={"detail": "final_url 정보가 없어 sitemap.xml 점검을 수행할 수 없습니다."},
                note="점검에 필요한 URL 정보가 부족합니다.",
            )
        )
        return results

    # ------------------------------------------------------------------
    # EXP-03: robots.txt 존재 여부 - [ OBSERVED / MISSING / NOT_TESTED ]
    # ------------------------------------------------------------------
    robots_txt_url = final_url.rstrip("/") + "/robots.txt"
    try:
        robots_response = requests.get(robots_txt_url, timeout=10)
        ctx["context_checks"]["robots_txt"] = {"url": robots_txt_url, "status_code": robots_response.status_code}
        if robots_response.status_code == 200:
            status = ResultStatus.OBSERVED
            evidence = {
                "url": robots_txt_url,
                "status_code": robots_response.status_code,
                "body": robots_response.text,
            }
            note = "robots.txt 파일이 식별되었습니다."
        elif robots_response.status_code == 404:
            status = ResultStatus.MISSING
            evidence = {"url": robots_txt_url, "status_code": robots_response.status_code}
            note = "robots.txt 파일이 식별되지 않았습니다."
        else:
            status = ResultStatus.NOT_TESTED
            evidence = {"url": robots_txt_url, "status_code": robots_response.status_code}
            note = "robots.txt 점검을 완료하지 못했습니다(비정상 상태 코드)."
    except Exception as e:
        ctx["context_checks"]["robots_txt"] = {"url": robots_txt_url, "error": type(e).__name__}
        status = ResultStatus.NOT_TESTED
        evidence = {"url": robots_txt_url, "detail": f"요청 실패: {type(e).__name__}"}
        note = "robots.txt 점검을 완료하지 못했습니다(요청 실패)."

    results.append(
        CheckResult(
            check_id="EXP-03",
            check_name="robots.txt 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    # ------------------------------------------------------------------
    # EXP-04: sitemap.xml 존재 여부 - [ OBSERVED / MISSING / NOT_TESTED ]
    # ------------------------------------------------------------------
    sitemap_xml_url = final_url.rstrip("/") + "/sitemap.xml"
    try:
        sitemap_response = requests.get(sitemap_xml_url, timeout=10)
        ctx["context_checks"]["sitemap_xml"] = {"url": sitemap_xml_url, "status_code": sitemap_response.status_code}
        if sitemap_response.status_code == 200:
            status = ResultStatus.OBSERVED
            evidence = {
                "url": sitemap_xml_url,
                "status_code": sitemap_response.status_code,
                "body": sitemap_response.text,
            }
            note = "sitemap.xml 파일이 식별되었습니다."
        elif sitemap_response.status_code == 404:
            status = ResultStatus.MISSING
            evidence = {"url": sitemap_xml_url, "status_code": sitemap_response.status_code}
            note = "sitemap.xml 파일이 식별되지 않았습니다."
        else:
            status = ResultStatus.NOT_TESTED
            evidence = {"url": sitemap_xml_url, "status_code": sitemap_response.status_code}
            note = "sitemap.xml 점검을 완료하지 못했습니다(비정상 상태 코드)."
    except Exception as e:
        ctx["context_checks"]["sitemap_xml"] = {"url": sitemap_xml_url, "error": type(e).__name__}
        status = ResultStatus.NOT_TESTED
        evidence = {"url": sitemap_xml_url, "detail": f"요청 실패: {type(e).__name__}"}
        note = "sitemap.xml 점검을 완료하지 못했습니다(요청 실패)."

    results.append(
        CheckResult(
            check_id="EXP-04",
            check_name="sitemap.xml 존재 여부",
            status=status,
            owasp=owasp_mapping,
            evidence=evidence,
            note=note,
        )
    )

    return results