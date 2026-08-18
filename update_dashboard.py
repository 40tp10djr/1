"""
fetch_toss.py / fetch_kb.py 로 받은 결과(toss_output.json, kb_output.json)를
읽어서, 새 대시보드 HTML(dashboard_filled.html)을 만들어줍니다.

사용법:
  python fetch_toss.py
  python fetch_kb.py
  python update_dashboard.py
  → dashboard_filled.html 을 더블클릭해서 열면 최신 숫자가 채워진 상태로 보입니다.

toss_output.json / kb_output.json 중 하나가 없어도 동작합니다(있는 것만 반영).
"""
import json
import re
import os

TEMPLATE_PATH = "dashboard_template.html"
OUTPUT_PATH = "docs/index.html"  # GitHub Pages가 /docs 폴더를 서빙하는 기본 경로


def load_json(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def main():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"에러: {TEMPLATE_PATH} 가 이 폴더에 없습니다. pnl_dashboard.html을 "
              f"{TEMPLATE_PATH} 이름으로 이 폴더에 복사해주세요.")
        return

    toss = load_json("toss_output.json")
    kb = load_json("kb_output.json")

    holdings = []
    if kb:
        holdings.extend(kb.get("holdings", []))
    if toss:
        holdings.extend(toss.get("holdings", []))

    total_eval_pl = sum((h["cur"] - h["buy"]) * h["qty"] for h in holdings) if holdings else None

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        html = f.read()

    if total_eval_pl is not None:
        html = re.sub(
            r'(id="evalPL" value=")[-\d]+(")',
            rf'\g<1>{int(total_eval_pl)}\g<2>',
            html,
        )

    holdings_js = json.dumps(
        [{"broker": h["broker"], "name": h["name"], "qty": h["qty"], "buy": h["buy"], "cur": h["cur"]} for h in holdings],
        ensure_ascii=False,
    )
    html = re.sub(
        r"let holdings = \[[\s\S]*?\];",
        f"let holdings = {holdings_js};",
        html,
        count=1,
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"완료: {OUTPUT_PATH} 생성됨 (보유종목 {len(holdings)}개 반영)")
    if total_eval_pl is not None:
        print(f"자동 계산된 평가손익 합계: {total_eval_pl:,.0f}원")


if __name__ == "__main__":
    main()
