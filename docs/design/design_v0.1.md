# Design v0.1  
Top10 Mapping Reporter

---

## 1. 목적 및 설계 방향

- 본 프로젝트는 취약점 스캐너가 아니라, **관찰 가능한 근거 기반 리포터**를 목표로 한다.
- 공격 페이로드 기반 탐지는 제외하며, HTTP 응답에서 **확인 가능한 항목**만 다룬다.
- 모든 결과는 **증거(Evidence) 저장**을 전제로 한다.

---

## 2. 시스템 컨텍스트 (System Context)

### Context (Korean)
![context_ko_v0.1](../diagrams/context/v0.1/context_ko_v0.1.png)

### Context (English)
![context_en_v0.1](../diagrams/context/v0.1/context_en_v0.1.png)

---

## 3. 유스케이스 (Use Case)

### Use Case (Korean)
![usecase_ko_v0.1](../diagrams/usecase/v0.1/usecase_ko_v0.1.png)

### Use Case (English)
![usecase_en_v0.1](../diagrams/usecase/v0.1/usecase_en_v0.1.png)

---

## 4. 실행 흐름 (Activity)

### Activity (Korean)
![activity_ko_v0.1](../diagrams/activity/v0.1/activity_ko_v0.1.png)

### Activity (English)
![activity_en_v0.1](../diagrams/activity/v0.1/activity_en_v0.1.png)

---

## 5. 결과 상태 정의 (Result Status)

- 확인됨(PASS): 보안 설정이 정상적으로 확인됨
- 설정 미흡(WEAK): 설정은 있으나 보안상 충분하지 않음
- 미설정(MISSING): 관련 보안 설정이 확인되지 않음
- 식별됨(OBSERVED): 의미가 있을 수 있는 요소가 식별됨(주의 필요)
- 확인불가(NOT_TESTED): 환경/기술적 이유로 판단 불가

---

## 6. 증거 저장 구조 (Evidence)

- 실행 단위로 `runs/<run_id>/` 폴더를 생성한다.
- 리포트 판단에 필요한 원본 근거를 저장한다.
- 민감 정보는 저장 전에 마스킹한다.

(세부 디렉터리 구조는 MVP 구현 후 v0.2에서 확정)

---

## 7. 설계상 제한 및 의도

- 외부 실서비스 무단 점검을 하지 않는다.
- 취약점 확정 문구를 사용하지 않는다.
- 재현 가능한 근거 중심으로만 기록한다.