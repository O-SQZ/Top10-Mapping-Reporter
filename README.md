# Top10 Mapping Reporter

OWASP Top 10 2025 기준으로  
**“확실히 관찰 가능한 보안 점검 결과”를 수집하고,  
그 근거를 함께 매핑하여 리포트로 정리하는 도구**입니다.

이 프로젝트는 취약점 스캐너가 아니라  
**점검 결과를 근거 중심으로 정리·설명하는 리포터(Reporter)**를 목표로 합니다.

---

## 🔍 Why this project?

OWASP Top 10을 공부하면서 다음과 같은 고민이 있었습니다.

- OWASP Top 10 카테고리는 이해했지만  
  → **실제로 무엇을 점검하고 어떻게 보고해야 하는지**는 잘 연결되지 않았습니다.
- 자동 취약점 스캐너는 결과는 많지만  
  → **왜 이게 문제인지 설명하기 어렵고**, 오탐도 많았습니다.
- 포트폴리오 관점에서도  
  → “스캐너 실행”보다 **점검 근거와 판단 과정**이 더 중요하다고 느꼈습니다.

그래서 이 프로젝트는  
**공격 페이로드 탐지 대신, 관찰 가능한 사실과 근거 수집에 집중**합니다.

---

## 🎯 Project Goal

- HTTP 요청/응답으로 **명확히 확인 가능한 보안 설정을 점검**
- 각 점검 항목을 **OWASP Top 10 2025 카테고리에 근거와 함께 매핑**
- 결과를 **사람이 읽을 수 있는 리포트(HTML / Markdown)** 형태로 출력
- 모든 판단에는 **재현 가능한 증거 파일**을 함께 남김

---

## 📦 What this tool does (MVP scope)

### Included
- HTTP Security Headers 관찰
- Cookie 속성(Secure, HttpOnly, SameSite) 확인
- 서버 정보 노출 여부 관찰
- robots.txt / sitemap.xml 존재 여부 확인
- (선택) 로그인 기반 간단한 세션 시나리오 점검

### Not included
- SQL Injection, XSS, SSRF 등 공격 페이로드 기반 탐지
- 외부 실서비스 무단 점검
- “취약점 확정” 판정

> 모든 결과는  
> **관찰(Observed) / 설정 미흡(Weak) / 미설정(Missing)** 등의 표현을 사용합니다.

---

## 🧭 How it works (High-level)

1. 사용자가 대상 URL을 입력
2. 시스템이 HTTP 요청을 보내 응답을 수집
3. 체크리스트 기반 점검 수행
4. 점검 결과를 OWASP Top 10 2025 항목과 매핑
5. 근거(Evidence)와 함께 리포트 생성

---

## 🗂 Repository Structure (planned)

```
Top10-Mapping-Reporter/
├─ app/            # Flask application
├─ checks/         # Individual check logic
├─ report/         # Report rendering logic
├─ runs/           # Evidence & results (gitignored)
├─ docs/           # Diagrams & design documents
└─ README.md
```

--- 

## ⚠️ Disclaimer

This project is intended for:
- local demo environments
- educational and portfolio purposes
- authorized testing only

It is **not** a replacement for professional security assessments.

---

## 📌 Status

- [x] Repository initialized
- [x] System context diagram drafted
- [ ] Detailed requirements definition
- [ ] Check item specification
- [ ] MVP implementation

This README is a **draft** and will evolve as the project progresses.