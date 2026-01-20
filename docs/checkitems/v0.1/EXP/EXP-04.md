# EXP-04: sitemap.xml 존재 여부

## 목적
사이트 구조 정보가 포함될 수 있는 sitemap.xml 파일의  
존재 여부를 식별한다.

## 점검 대상
- `/sitemap.xml` 경로

## 점검 방법
- 대상 호스트의 `/sitemap.xml` 경로로 HTTP GET 요청을 전송한다.
- 응답 상태 코드 및 본문 존재 여부를 확인한다.

## 판정 기준
- 식별됨(OBSERVED): `/sitemap.xml` 파일이 존재함 (200 OK)
- 미설정(MISSING): 파일이 존재하지 않음 (404 등)
- 확인불가(NOT_TESTED): 요청 실패 또는 응답 수신 실패

## OWASP Top 10 2025 매핑
- A02:2025 – Security Misconfiguration  
  (사이트 구조 정보 노출 가능성은 구성 관리 측면의 문제)

## 영향 가능성(Potential Impact)
- 사이트 전체 구조가 노출될 경우,
  공격자가 탐색 범위를 빠르게 확장할 수 있다.

## 참고/전제(Conditions)
- 관리용 또는 비공개 엔드포인트가 sitemap에 포함된 경우

## 증거(Evidence)
- HTTP 상태 코드
- sitemap.xml 응답 본문