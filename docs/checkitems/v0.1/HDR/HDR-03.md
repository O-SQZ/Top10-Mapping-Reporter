# HDR-03: X-Frame-Options 헤더 존재 여부

## 목적
웹 페이지가 외부 프레임에 포함되는 것을 제한하여  
클릭재킹 공격을 완화하기 위한 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `X-Frame-Options`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `X-Frame-Options` 항목 존재 여부를 확인한다.

## 판정 기준
- 확인됨(PASS): `X-Frame-Options` 헤더가 존재함
- 미설정(MISSING): 해당 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (UI 보호 관련 보안 설정 누락)

## 영향 가능성(Potential Impact)
- 페이지가 외부 프레임에 포함될 수 있는 경우,
  클릭재킹과 같은 UI 기반 공격에 악용될 가능성이 있다.

## 참고/전제(Conditions)
- 공격자가 사용자를 유도할 수 있는 외부 페이지를 구성할 수 있는 경우

## 증거(Evidence)
- HTTP 응답 헤더 덤프