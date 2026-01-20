# EXP-03: robots.txt 존재 여부

## 목적
robots.txt 파일 존재 여부를 확인하여  
검색 엔진 제어 목적의 경로 정보가 노출되는지를 식별한다.

## 점검 대상
- `/robots.txt` 경로

## 점검 방법
- 대상 호스트의 `/robots.txt` 경로로 HTTP GET 요청을 전송한다.
- 응답 상태 코드 및 본문 존재 여부를 확인한다.

## 판정 기준
- 식별됨(OBSERVED): `/robots.txt` 파일이 존재함 (200 OK)
- 미설정(MISSING): 파일이 존재하지 않음 (404 등)
- 확인불가(NOT_TESTED): 요청 실패 또는 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (운영·구성 정보가 외부에 노출될 수 있는 설정 요소)

## 영향 가능성(Potential Impact)
- robots.txt에 특정 경로가 명시된 경우,
  공격자가 사이트 구조를 추측하는 단서로 활용할 수 있다.

## 참고/전제(Conditions)
- robots.txt에 민감하거나 내부 관리용 경로가 포함된 경우

## 증거(Evidence)
- HTTP 상태 코드
- robots.txt 응답 본문