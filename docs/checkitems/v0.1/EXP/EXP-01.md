# EXP-01: Server 헤더 노출 여부

## 목적
HTTP 응답 헤더를 통해 서버 종류 또는 구현 정보가 노출되는지 여부를 식별한다.

## 점검 대상
- HTTP 응답 헤더 `Server`

## 점검 방법
- 대상 URL에 HTTP 요청을 전송한다.
- 응답 헤더에 `Server` 항목 존재 여부를 확인한다.
- 값이 존재할 경우 그대로 수집한다.

## 판정 기준
- 식별됨(OBSERVED): `Server` 헤더가 존재함
- 미설정(MISSING): `Server` 헤더가 존재하지 않음
- 확인불가(NOT_TESTED): 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (불필요한 서버 정보 노출은 보안 설정 관리 문제로 분류)

## 영향 가능성(Potential Impact)
- 서버 종류 또는 구현 정보가 노출될 경우,
  공격자가 기술 스택을 추측하는 데 활용할 수 있다.

## 참고/전제(Conditions)
- 헤더 값에 구체적인 제품명이나 버전 정보가 포함된 경우

## 증거(Evidence)
- HTTP 응답 헤더 덤프