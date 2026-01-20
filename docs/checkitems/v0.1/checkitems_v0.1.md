# CheckItems v0.1  
Top10 Mapping Reporter

본 문서는 Top10 Mapping Reporter MVP(v0.1)에서 사용하는  
**점검 항목(CheckItem)의 전체 목록과 OWASP Top 10 2025 매핑 기준**을 정의한다.

각 CheckItem은 공격이나 행위 검증 없이,  
**HTTP 요청/응답을 통해 관찰 가능한 근거**만을 기반으로 한다.

---

## 1. OWASP Top 10 2025 적용 원칙

- 본 프로젝트는 [OWASP Top 10 2025](https://owasp.org/Top10/2025/)를 **취약점 목록이 아닌 리스크 분류 체계**로 활용한다.
- 공격 페이로드, 로그인 시나리오, 내부 로직 분석이 필요한 항목은 v0.1 범위에서 제외한다.
- 모든 점검 결과는 **근거 기반 관찰 결과**이며, 취약점을 확정하지 않는다.

---

## 2. CheckItem 전체 목록 (v0.1)

### A02:2025 – Security Misconfiguration

> 설정 누락, 기본값 사용, 불필요한 정보 노출 등  
> HTTP 응답만으로 관찰 가능한 보안 구성 문제

#### 2.1 HTTP Security Headers

| Check ID | Check Item | 기본 결과 상태 |
|---|---|---|
| HDR-01 | Strict-Transport-Security 헤더 존재 여부 | PASS / WEAK / MISSING |
| HDR-02 | Content-Security-Policy 헤더 존재 여부 | PASS / WEAK / MISSING |
| HDR-03 | X-Frame-Options 헤더 존재 여부 | PASS / MISSING |
| HDR-04 | X-Content-Type-Options 헤더 존재 여부 | PASS / MISSING |
| HDR-05 | Referrer-Policy 헤더 존재 여부 | PASS / MISSING |
| HDR-06 | Permissions-Policy 헤더 존재 여부 | PASS / MISSING |

---

#### 2.2 Information Exposure (관찰 기반)

| Check ID | Check Item | 기본 결과 상태 |
|---|---|---|
| EXP-01 | Server 헤더 노출 여부 | OBSERVED / MISSING |
| EXP-02 | X-Powered-By 헤더 노출 여부 | OBSERVED / MISSING |
| EXP-03 | robots.txt 존재 여부 | OBSERVED / MISSING |
| EXP-04 | sitemap.xml 존재 여부 | OBSERVED / MISSING |

※ 본 그룹은 **취약점 판정(PASS/WEAK)을 사용하지 않으며**,  
존재 여부 자체를 보안상 의미 있는 요소로 **식별**한다.

---

### A07:2025 – Authentication Failures (부분 적용)

> 인증 로직이 아닌, **인증 상태를 보호하는 설정(Configuration)만 관찰**

#### 2.3 Cookie Attributes

| Check ID | Check Item | 기본 결과 상태 |
|---|---|---|
| CK-01 | Secure 속성 설정 여부 | PASS / WEAK / MISSING |
| CK-02 | HttpOnly 속성 설정 여부 | PASS / WEAK / MISSING |
| CK-03 | SameSite 속성 설정 여부 | PASS / WEAK / MISSING |
| CK-04 | Cookie Path / Domain 명시 여부 | PASS / WEAK / MISSING |

※ 쿠키가 존재하지 않는 경우 결과는 **NOT_TESTED**로 처리한다.

---

## 3. 결과 상태 요약

| 상태 | 의미 |
|---|---|
| PASS | 설정이 정상적으로 확인됨 |
| WEAK | 설정은 있으나 보안 관점에서 충분하지 않음 |
| MISSING | 관련 설정이 확인되지 않음 |
| OBSERVED | 보안상 의미를 가질 수 있는 요소가 식별됨 |
| NOT_TESTED | 환경적·기술적 이유로 판단 불가 |

---

## 4. 비적용 OWASP Top 10 항목 (v0.1)

아래 항목은 공격/행위 검증 또는 내부 분석이 필요하므로  
v0.1 CheckItem 범위에서 제외한다.

- A01 – Broken Access Control  
- A03 – Software Supply Chain Failures  
- A04 – Cryptographic Failures  
- A05 – Injection  
- A06 – Insecure Design  
- A08 – Software/Data Integrity Failures  
- A09 – Logging & Alerting Failures  
- A10 – Mishandling of Exceptional Conditions