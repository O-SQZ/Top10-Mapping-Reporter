# HDR-02: Content-Security-Policy 헤더 존재 여부

## 목적
브라우저에서 허용되는 리소스 출처를 제한하는  
CSP(Content-Security-Policy) 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `Content-Security-Policy`

## 점검 방법
- 대상 URL에 HTTP/HTTPS 요청을 전송한다.
- 응답 헤더에 CSP 항목이 존재하는지 확인한다.
- 설정된 정책 문자열을 그대로 수집한다.

## 판정 기준
- 확인됨(PASS): CSP 헤더가 존재함
- 설정 미흡(WEAK): CSP는 있으나 `unsafe-inline` 등 보안상 약한 설정이 포함됨
- 미설정(MISSING): CSP 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (브라우저 보안 정책 구성 미흡)

## 영향 가능성(Potential Impact)
- 콘텐츠 출처에 대한 제한이 없을 경우,
  XSS와 같은 클라이언트 측 공격이 발생했을 때
  피해 범위가 확대될 가능성이 있다.

## 참고/전제(Conditions)
- 실제로 XSS 취약점이 존재하는 경우에만 영향이 발생함
- 본 점검은 XSS 존재 여부를 판단하지 않는다

## 증거(Evidence)
- CSP 헤더 원문 문자열