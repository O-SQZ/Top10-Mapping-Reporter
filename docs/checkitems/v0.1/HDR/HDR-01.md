# HDR-01: Strict-Transport-Security 헤더 존재 여부

## 목적
HTTPS 연결을 강제하여 중간자 공격 및 프로토콜 다운그레이드를 방지하기 위한  
HSTS(Strict-Transport-Security) 설정 여부를 확인한다.

## 점검 대상
- HTTP 응답 헤더 `Strict-Transport-Security`

## 점검 방법
- 대상 URL에 HTTPS 요청을 전송한다.
- 응답 헤더에 `Strict-Transport-Security` 항목이 존재하는지 확인한다.

## 판정 기준
- 확인됨(PASS): `Strict-Transport-Security` 헤더가 존재함
- 설정 미흡(WEAK): 헤더는 존재하나 `max-age` 값이 매우 짧거나 옵션이 제한적임
- 미설정(MISSING): 해당 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): HTTPS 연결 실패 등으로 확인 불가

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (HTTPS 강제 정책은 애플리케이션 보안 설정에 해당)

## 영향 가능성(Potential Impact)
- HTTPS 강제가 적용되지 않은 경우, 네트워크 환경에 따라 중간자 공격이나
  프로토콜 다운그레이드 공격에 노출될 가능성이 증가할 수 있다.

## 참고/전제(Conditions)
- HTTP로 접근 가능한 엔드포인트가 존재하는 경우
- 사용자가 신뢰되지 않은 네트워크 환경에서 접속하는 경우

## 증거(Evidence)
- 전체 HTTP 응답 헤더 덤프