from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
from datetime import datetime


STATUS_COLOR = {
    "PASS": "#2ecc71",
    "WEAK": "#f39c12",
    "MISSING": "#e74c3c",
    "OBSERVED": "#3498db",
    "NOT_TESTED": "#95a5a6",
}


def render_report(
    summary: Dict[str, Any],
    results: List[Dict[str, Any]],
    out_dir: Path,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "report.html"

    grouped = defaultdict(list)
    for r in results:
        for o in r.get("owasp", []):
            grouped[o["category"]].append((o, r))

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title>Top10 Mapping Reporter</title>
<style>
/* =========================
   Base
========================= */
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  background: #f4f6fa;
  color: #222;
  margin: 0;
  padding: 24px;
}}

h1 {{
  margin: 0 0 6px 0;
}}

h2 {{
  margin: 0 0 6px 0;
}}

small {{
  color: #666;
}}

.container {{
  max-width: 1100px;
  margin: 0 auto;
}}

/* =========================
   Cards
========================= */
.card {{
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
  margin: 12px 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}}

/* =========================
   Summary Table
========================= */
.meta td {{
  padding: 4px 8px;
  vertical-align: top;
  font-size: 14px;
}}

/* =========================
   OWASP Section
========================= */
.section {{
  margin-top: 32px;
  padding-left: 14px;
  border-left: 4px solid #d0d4dc;
}}

.section > p {{
  margin-top: 4px;
  margin-bottom: 12px;
}}

/* =========================
   Check Item
========================= */
.badge {{
  display: inline-block;
  min-width: 86px;
  text-align: center;
  padding: 3px 10px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
  margin-left: 8px;
}}

.note {{
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}}

/* =========================
   Evidence
========================= */
details {{
  margin-top: 10px;
}}

details summary {{
  cursor: pointer;
  font-size: 13px;
  color: #444;
}}

pre {{
  background: #eef0f4;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.4;
}}

/* =========================
   Summary Grid
========================= */
.summary-grid {{
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-top: 12px;
}}

.summary-item {{
  padding: 10px 0;
  border-radius: 6px;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
}}
.summary-link {{
  display: block;
  text-decoration: none;
  color: #ffffff;
  position: relative;
}}

.summary-link:hover {{
  filter: brightness(0.95);
  transform: translateY(-1px);
}}

/* Tooltip */
.summary-link::after {{
  content: attr(data-tooltip);
  position: absolute;
  left: 50%;
  top: -10px;
  transform: translate(-50%, -100%);
  background: rgba(0, 0, 0, 0.85);
  color: #ffffff;
  padding: 6px 8px;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 12px;
  line-height: 1.2;
  opacity: 0;
  pointer-events: none;
  transition: opacity 120ms ease;
}}

.summary-link:hover::after {{
  opacity: 1;
}}

/* Legend */
.legend {{
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 13px;
  color: #444;
}}

.legend-item {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}

.legend-dot {{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  display: inline-block;
}}
</style>
</head>
<body>
<div class="container">
  <h1>Top10 Mapping Reporter</h1>
  <small>
    Run ID: {summary.get("run_id")} |
    Target: {summary.get("target_url")} |
    Created: {summary.get("created_at")}
  </small>

  <div class="card">
    <table class="meta">
      <tr><td><b>URL</b></td><td>{summary.get("target_url")}</td></tr>
      <tr><td><b>Status Code</b></td><td>{summary.get("status_code")}</td></tr>
      <tr><td><b>Total Checks</b></td><td>{summary.get("total_checks")}</td></tr>
    </table>
  </div>
  <div class="card">
    <h3>Check Summary</h3>
    <div class="legend">
      <span class="legend-item"><span class="legend-dot" style="background:{STATUS_COLOR['PASS']}"></span>PASS(확인됨)</span>
      <span class="legend-item"><span class="legend-dot" style="background:{STATUS_COLOR['WEAK']}"></span>WEAK(설정 미흡)</span>
      <span class="legend-item"><span class="legend-dot" style="background:{STATUS_COLOR['MISSING']}"></span>MISSING(미설정)</span>
      <span class="legend-item"><span class="legend-dot" style="background:{STATUS_COLOR['OBSERVED']}"></span>OBSERVED(식별됨)</span>
      <span class="legend-item"><span class="legend-dot" style="background:{STATUS_COLOR['NOT_TESTED']}"></span>NOT_TESTED(확인불가)</span>
    </div>
    <div class="summary-grid">
      {''.join(
        f'<div class="summary-item" style="background:{STATUS_COLOR.get(item["status"], "#999")}">'
        f'<a class="summary-link" href="#{item["check_id"]}" data-tooltip="{item.get("check_name", "")}">{item["check_id"]}</a>'
        f'</div>'
        for item in results
      )}
    </div>
  </div>
"""

    for category, items in grouped.items():
        title = items[0][0].get("title")
        rationale = items[0][0].get("rationale")

        html += f"""
<div class="section">
  <h2>{category} — {title}</h2>
  <p><small>{rationale}</small></p>
"""

        for _, r in items:
            status = r["status"]
            color = STATUS_COLOR.get(status, "#999")
            html += f"""
  <div class="card" id="{r["check_id"]}">
    <b>[{r["check_id"]}] {r["check_name"]}</b>
    <span class="badge" style="background:{color}">{status}</span>
    <div class="note">{r.get("note","")}</div>
    <div class="evidence">
      <pre>{json.dumps(r.get("evidence",{}), ensure_ascii=False, indent=2)}</pre>
    </div>
  </div>
"""
        html += "</div>"

    html += """
</div>
</body>
</html>
"""

    out_path.write_text(html, encoding="utf-8")
    return out_path