# Top10 Mapping Reporter

**OWASP Top 10 2025 기준으로 관찰 가능한 보안 설정을 점검하고,  
그 근거를 구조화된 결과와 리포트로 정리하는 CLI 기반 Reporter 도구**

이 프로젝트는 취약점을 공격하거나 자동 판정하는 스캐너가 아닙니다.  
HTTP 응답을 기반으로 **명확히 확인 가능한 사실(Evidence)**을 수집하고,  
이를 OWASP Top 10 2025 항목과 **근거 중심으로 매핑**하는 것을 목표로 합니다.

---

## 🔍 Why this project?

OWASP Top 10을 학습하면서 다음과 같은 문제의식을 가졌습니다.

- “OWASP Top 10을 안다”와 “실제로 무엇을 점검하고 어떻게 보고하는가” 사이의 간극

- 자동 스캐너의 결과는 많지만 **왜 문제가 되는지 설명하기 어려운 경우가 많음**

- 포트폴리오 관점에서 **점검 기준 · 판단 흐름 · 결과 구조를 설명할 수 있는 산출물**의 필요성

그래서 이 프로젝트는 **공격 시도 없이도 설명 가능한 보안 점검 결과를 남기는 Reporter**로 설계되었습니다.

---

## 🎯 Project Goal

- HTTP 요청/응답 기반 **재현 가능한 보안 설정 점검**
- 각 점검 항목을 **OWASP Top 10 2025 카테고리와 근거로 매핑**
- 결과를 **JSON + HTML 리포트** 형태로 출력
- 모든 판단에 **Evidence** 포함

---

## ✅ 개발 완료된 기능 

### 1. HTTP Security Headers (HDR)
- Strict-Transport-Security
- Content-Security-Policy (WEAK 판정 포함)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

### 2. Information Exposure (EXP)
- Server 헤더 노출 여부
- X-Powered-By 헤더 노출 여부
- robots.txt 존재 여부
- sitemap.xml 존재 여부

### 3. Cookie Attributes (CK)
- Secure 속성
- HttpOnly 속성
- SameSite 속성
- Path / Domain 명시 여부
- 복수 Set-Cookie 헤더 파싱 지원

### 4. 결과 산출물
- context.json : 요청/응답 컨텍스트 + 부가 정보
- summary.json : 점검 결과 요약
- report.html : 시각화된 HTML 리포트
- 실행 단위별 run 디렉터리 자동 생성

### 5. Demo Web
- config.py 기반 보안 설정 토글
- 각 옵션 조합에 따른 점검 결과 검증용
- **실제 취약한 서비스가 아닌 테스트 목적**

---

## 📊 Result Status 정의

| 상태 | 의미 |
|---|---|
| PASS | 보안 설정이 정상적으로 확인됨 |
| WEAK | 설정은 존재하나 보안상 충분하지 않음 |
| MISSING | 관련 설정이 확인되지 않음 |
| OBSERVED | 보안상 의미를 가질 수 있어 주의가 필요한 요소 |
| NOT_TESTED | 환경적 이유로 판단 불가 |

※ OBSERVED는 취약점 확정이 아님

---

## 🧭 How it works

1. 대상 URL 입력 (CLI)
2. HTTP 요청 및 응답 수집
3. 체크리스트 기반 점검 수행
4. OWASP Top 10 2025 항목 매핑
5. JSON + HTML 리포트 생성

---

## 🚫 Out of Scope (의도적으로 제외)

- SQLi, XSS 등 공격 기반 취약점 탐지
- 인증/세션 공격 시나리오
- 취약점 확정 판정
- 외부 서비스 무단 점검

---

## ⚠️ Disclaimer

이 도구는 **학습 및 포트폴리오 목적**으로 제작되었습니다.  
허가되지 않은 외부 서비스에 사용해서는 안 됩니다.

---