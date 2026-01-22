from flask import Flask, make_response
import config

app = Flask(__name__)


def apply_security_headers(resp):
    if config.ENABLE_HSTS:
        resp.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"

    if config.ENABLE_CSP:
        resp.headers["Content-Security-Policy"] = config.CSP_VALUE

    if config.ENABLE_XFO:
        resp.headers["X-Frame-Options"] = "DENY"

    if config.ENABLE_XCTO:
        resp.headers["X-Content-Type-Options"] = "nosniff"

    if config.ENABLE_REFERRER_POLICY:
        resp.headers["Referrer-Policy"] = "no-referrer"

    if config.ENABLE_PERMISSIONS_POLICY:
        resp.headers["Permissions-Policy"] = "geolocation=()"

    # 정보 노출 제어
    if not config.ENABLE_SERVER_HEADER:
        resp.headers.pop("Server", None)

    if not config.ENABLE_X_POWERED_BY:
        resp.headers.pop("X-Powered-By", None)

    return resp


@app.route("/")
def index():
    resp = make_response("Top10 Mapping Reporter - Demo Web")
    resp = apply_security_headers(resp)
    return resp


@app.route("/login")
def login():
    resp = make_response("logged in")

    resp.set_cookie(
        key="sessionid",
        value="demo-session",
        secure=config.COOKIE_SECURE,
        httponly=config.COOKIE_HTTPONLY,
        samesite=config.COOKIE_SAMESITE,
        path=config.COOKIE_PATH,
        domain=config.COOKIE_DOMAIN,
    )

    resp = apply_security_headers(resp)
    return resp


@app.route("/logout")
def logout():
    resp = make_response("logged out")
    resp.delete_cookie("sessionid")
    resp = apply_security_headers(resp)
    return resp


@app.route("/robots.txt")
def robots():
    if not config.ENABLE_ROBOTS:
        return "", 404
    return "User-agent: *\nDisallow: /admin", 200


@app.route("/sitemap.xml")
def sitemap():
    if not config.ENABLE_SITEMAP:
        return "", 404
    return "<urlset></urlset>", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)