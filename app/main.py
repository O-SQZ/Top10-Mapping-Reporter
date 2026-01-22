import argparse
import json
import os
from datetime import datetime
from uuid import uuid4

from app.engine.runner import run_checks_with_context

from pathlib import Path
from app.report.render import render_report

def _make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = uuid4().hex[:6]
    return f"{timestamp}_{suffix}"


def _now_kst_iso() -> str:
    # KST 기준
    return datetime.now().isoformat(timespec="seconds")


def _write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--save", action="store_true", help="runs/<run_id>에 결과와 컨텍스트를 저장합니다.")
    args = p.parse_args()

    run_id = _make_run_id()
    created_at = _now_kst_iso()

    ctx, results = run_checks_with_context(args.url)

    # 메타데이터 + 결과물
    summary_payload = {
        "run_id": run_id,
        "created_at": created_at,
        "target_url": args.url,
        "final_url": ctx.get("final_url"),
        "status_code": ctx.get("status_code"),
        "results": [r.to_dict() for r in results],
    }

    # 콘솔 출력도 동일 포맷으로 고정
    print(json.dumps(summary_payload, ensure_ascii=False, indent=2))

    if args.save:
        base_dir = os.path.join("runs", run_id)

        _write_json(os.path.join(base_dir, "summary.json"), summary_payload)

        # 원본에 가까운 컨텍스트 + 추가 요청 결과
        context_payload = {
            "run_id": run_id,
            "created_at": created_at,
            "target_url": args.url,
            "final_url": ctx.get("final_url"),
            "status_code": ctx.get("status_code"),
            "history": ctx.get("history"),
            "headers": ctx.get("headers"),
            # requests CookieJar 등 직렬화 불가 객체는 저장하지 않음
            "context_checks": ctx.get("context_checks", {}),
        }
        _write_json(os.path.join(base_dir, "context.json"), context_payload)

        print(f"\n[Saved] {base_dir}/summary.json")
        print(f"[Saved] {base_dir}/context.json")
        
        #html 문서 생성 + 저장
        run_dir = Path(base_dir)
        report_path = render_report(
            summary=summary_payload,
            results=summary_payload["results"],
            out_dir=run_dir,
        )

        print(f"[Saved] {report_path}")


if __name__ == "__main__":
    main()