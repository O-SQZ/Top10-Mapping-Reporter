# EXP-02: X-Powered-By 헤더 노출 여부

## 목적
웹 애플리케이션의 프레임워크 또는 실행 환경 정보가  
HTTP 헤더를 통해 노출되는지 여부를 식별한다.

## 점검 대상
- HTTP 응답 헤더 `X-Powered-By`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `X-Powered-By` 항목 존재 여부를 확인한다.
- 값이 존재할 경우 그대로 수집한다.

## 판정 기준
- 식별됨(OBSERVED): `X-Powered-By` 헤더가 존재함
- 미설정(MISSING): `X-Powered-By` 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (애플리케이션 구현 정보 노출은 구성 관리 문제로 분류)

## 영향 가능성(Potential Impact)
- 애플리케이션 프레임워크 정보가 노출될 경우,
  공격자의 정찰 단계에서 참고 정보로 활용될 수 있다.

## 참고/전제(Conditions)
- 실제 취약점 존재 여부는 본 점검 범위에 포함되지 않는다

## 증거(Evidence)
- HTTP 응답 헤더 덤프