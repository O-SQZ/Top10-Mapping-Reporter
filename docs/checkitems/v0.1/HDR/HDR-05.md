# HDR-05: Referrer-Policy 헤더 존재 여부

## 목적
요청 시 전송되는 Referer 헤더를 제어하여  
불필요한 정보 노출을 최소화하기 위한 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `Referrer-Policy`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `Referrer-Policy` 항목 존재 여부를 확인한다.

## 판정 기준
- 확인됨(PASS): `Referrer-Policy` 헤더가 존재함
- 미설정(MISSING): 해당 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (요청 정보 노출 제어 설정 누락)

## 영향 가능성(Potential Impact)
- Referer 정보가 과도하게 전송되는 경우,
  URL 경로나 파라미터 정보가 외부로 노출될 가능성이 있다.

## 참고/전제(Conditions)
- 민감한 정보가 URL에 포함되어 있는 경우에만 영향이 커진다

## 증거(Evidence)
- HTTP 응답 헤더 덤프