# HDR-04: X-Content-Type-Options 헤더 존재 여부

## 목적
브라우저의 MIME 타입 추측(MIME Sniffing)을 방지하기 위한  
`X-Content-Type-Options` 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `X-Content-Type-Options`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `X-Content-Type-Options` 항목 존재 여부를 확인한다.

## 판정 기준
- 확인됨(PASS): `X-Content-Type-Options` 헤더가 존재함
- 미설정(MISSING): 해당 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (콘텐츠 처리 관련 보안 설정 누락)

## 영향 가능성(Potential Impact)
- 브라우저가 MIME 타입을 추측할 수 있는 경우,
  의도하지 않은 스크립트 실행으로 이어질 가능성이 있다.

## 참고/전제(Conditions)
- 콘텐츠 타입이 명확하지 않거나 잘못 설정된 리소스가 존재하는 경우

## 증거(Evidence)
- HTTP 응답 헤더 덤프