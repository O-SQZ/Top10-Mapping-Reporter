# Demo Web for Top10 Mapping Reporter

이 디렉터리는 **Top10 Mapping Reporter 검증용 데모 웹 애플리케이션**입니다.

실제 서비스를 흉내 내는 것이 아니라,
리포터의 **HDR / EXP / CK 점검 결과가 의도대로 출력되는지**를 확인하기 위한
재현 가능한 테스트 타깃을 제공합니다.

---

## 목적

- 보안 헤더(HDR) 점검 결과 재현
- 정보 노출(EXP) 식별 결과 재현
- 쿠키 속성(CK) 점검 결과 재현
- PASS / WEAK / MISSING / NOT_TESTED 상태 전부 테스트

---

## 실행 방법

```bash
pip install -r requirements.txt
python app.py
```