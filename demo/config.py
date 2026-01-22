# demo/config.py
# 
# 이 파일은 데모 웹의 보안 설정/노출 상태를 빠르게 토글하기 위한 설정 파일입니다.
# 리포터 결과(PASS/WEAK/MISSING/OBSERVED/NOT_TESTED)가 의도대로 바뀌는지 확인할 때 사용하세요.
# 
# 사용 방법(권장 흐름)
# 1) 아래 값을 변경한다.
# 2) demo/app.py 재실행(또는 Flask 재시작)한다.
# 3) 리포터를 다시 실행한다: python -m app.main --url http://127.0.0.1:5050 --save
# 
# 참고
# - ENABLE_SERVER_HEADER는 Flask 개발 서버(Werkzeug) 특성상 완전히 제거되지 않을 수 있습니다.

# =========================
# HTTP Security Headers (HDR)
# =========================
# 각 헤더를 True로 켜면 해당 헤더가 응답에 포함됩니다.
# 리포터에서는 보통 다음처럼 판정됩니다.
# - True  -> PASS(또는 CSP는 값에 따라 WEAK 가능)
# - False -> MISSING

# Strict-Transport-Security (HSTS)
# - HTTPS 환경에서 강제 HTTPS 정책을 브라우저에 적용할 때 사용
ENABLE_HSTS = True

# Content-Security-Policy (CSP)
# - 기본은 PASS 목표: "default-src 'self'"
# - WEAK 테스트: unsafe-inline / unsafe-eval / * 등이 포함되면 WEAK로 판정
ENABLE_CSP = True
CSP_VALUE = "default-src 'self' 'unsafe-inline'"  # WEAK 예시: "default-src 'self' 'unsafe-inline'"

# X-Frame-Options
# - 클릭재킹 방어용(보통 DENY 또는 SAMEORIGIN 사용)
ENABLE_XFO = True

# X-Content-Type-Options
# - MIME sniffing 방지용(보통 nosniff)
ENABLE_XCTO = True

# Referrer-Policy
# - Referer 헤더 노출 정책 제어(보통 no-referrer / strict-origin-when-cross-origin 등)
ENABLE_REFERRER_POLICY = True

# Permissions-Policy
# - 브라우저 기능(geolocation 등) 접근 제어
ENABLE_PERMISSIONS_POLICY = True


# =========================
# Information Exposure (EXP)
# =========================
# 응답 헤더/파일 노출을 통한 "식별(OBSERVED)" 시나리오를 만들기 위한 옵션입니다.

# Server 헤더 노출
# - True  -> 보통 EXP-01 OBSERVED
# - False -> (데모 서버에 따라) 제거가 안 될 수 있음 (Werkzeug가 다시 붙일 수 있음)
ENABLE_SERVER_HEADER = False

# X-Powered-By 헤더 노출
# - 기본 Flask는 이 헤더를 자동으로 넣지 않는 경우가 많습니다.
# - True로 켠다고 "자동으로" 나타나진 않을 수 있으며, 필요하면 demo/app.py에서 명시적으로 추가하세요.
ENABLE_X_POWERED_BY = False

# robots.txt / sitemap.xml 존재 여부
# - True  -> 보통 EXP-03/04 OBSERVED(200)
# - False -> 보통 EXP-03/04 MISSING(404)
ENABLE_ROBOTS = True
ENABLE_SITEMAP = True


# =========================
# Cookie Attributes (CK)
# =========================
# 주의: 현재 데모는 /login에서만 쿠키를 발급합니다.
# 리포터가 기본적으로 /만 호출하는 구조라면 CK는 NOT_TESTED로 유지될 수 있습니다.
# CK를 실제로 검증하려면:
# - 데모가 /에서도 쿠키를 발급하게 하거나
# - 리포터가 /login을 추가 요청하도록 확장해야 합니다.

# Secure
# - HTTPS에서만 쿠키 전송(권장)
COOKIE_SECURE = True

# HttpOnly
# - JS에서 document.cookie 접근 제한(권장)
COOKIE_HTTPONLY = True

# SameSite
# - None / "Lax" / "Strict" / "None"
# - None(설정 없음)        -> 보통 MISSING
# - "Lax"/"Strict"       -> 보통 PASS
# - "None"(크로스사이트)  -> v0.1 정책상 WEAK로 판정될 수 있음
COOKIE_SAMESITE = "None"

# Path / Domain
# - None이면 속성 미지정(기본 동작)
# - 테스트 예시:
#   COOKIE_PATH = "/"
#   COOKIE_DOMAIN = "localhost"
COOKIE_PATH = "/"
COOKIE_DOMAIN = "localhost"