# HDR-06: Permissions-Policy 헤더 존재 여부

## 목적
브라우저 기능(카메라, 마이크 등)에 대한 접근을 제한하기 위한  
Permissions-Policy 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `Permissions-Policy`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `Permissions-Policy` 항목 존재 여부를 확인한다.

## 판정 기준
- 확인됨(PASS): `Permissions-Policy` 헤더가 존재함
- 미설정(MISSING): 해당 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (브라우저 권한 제어 관련 보안 설정 누락)

## 영향 가능성(Potential Impact)
- 브라우저 기능에 대한 제한이 없는 경우,
  불필요한 기능 접근이 보안 사고의 단서가 될 가능성이 있다.

## 참고/전제(Conditions)
- 실제로 해당 기능을 사용하는 클라이언트 코드가 존재하는 경우

## 증거(Evidence)
- HTTP 응답 헤더 덤프