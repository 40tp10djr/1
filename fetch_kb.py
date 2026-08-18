"""
KB증권 Open API에서 계좌 평가손익 / 보유종목을 가져오는 스크립트 (뼈대/스켈레톤).

KB증권은 로그인해야만 API 세부 엔드포인트 목록이 보이는 구조라, Claude가
정확한 경로를 확인하지 못했습니다. 대신 KB증권이 공식으로 제공하는
"샘플 소스 코드 생성기"를 이용하면 가장 정확합니다.

── 하는 방법 ──────────────────────────────────────────
1. https://openapi.kbsec.com/apidoc_b2c 로그인
2. 왼쪽 메뉴 "국내주식" 카테고리에서 계좌 잔고/평가손익 관련 API 선택
   (이름 예상: "주식잔고조회", "계좌평가현황" 등 — 실제 목록은 로그인 후 확인)
3. 우측 "Sample Code Generator"에서 언어를 PYTHON으로 선택 → 코드 생성
4. 생성된 코드를 아래 fetch_balance() 함수 안에 붙여넣고,
   appKey/appSecret/계좌번호 부분만 os.getenv(...)로 바꿔주세요.
5. 응답 데이터에서 종목명/수량/매입단가/현재가에 해당하는 필드명을 찾아
   normalize_holdings() 안의 item.get(...) 부분을 실제 필드명으로 맞춰주세요.
────────────────────────────────────────────────────
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openapi.kbsec.com"  # 실제 API 호출용 도메인은 문서에서 별도 확인 필요할 수 있음


def fetch_balance(app_key: str, app_secret: str, account_no: str):
    """
    TODO: 여기에 KB증권 "Sample Code Generator"가 생성해준 코드를 붙여넣으세요.
    아래는 KB증권을 포함해 국내 증권사 오픈API들이 흔히 쓰는 방식(OAuth 토큰 발급 후
    tr_id 헤더와 함께 조회)을 참고용으로 적어둔 것이며, 실제 경로가 다를 수 있습니다.
    """
    raise NotImplementedError(
        "KB증권 Sample Code Generator에서 받은 코드로 이 함수를 채워주세요. "
        "openapi.kbsec.com/apidoc_b2c 에서 로그인 후 확인 가능합니다."
    )

    # 참고용 예시 형태 (실제 경로/파라미터는 다를 수 있음):
    # token_resp = requests.post(
    #     BASE_URL + "/oauth2/token",
    #     json={"grant_type": "client_credentials", "appkey": app_key, "appsecret": app_secret},
    # )
    # access_token = token_resp.json()["access_token"]
    #
    # balance_resp = requests.get(
    #     BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-balance",
    #     headers={
    #         "Authorization": f"Bearer {access_token}",
    #         "appkey": app_key,
    #         "appsecret": app_secret,
    #         "tr_id": "TTTC8434R",  # 예시 - 실제 tr_id는 문서에서 확인
    #     },
    #     params={"CANO": account_no},
    # )
    # return balance_resp.json()


def normalize_holdings(raw_data):
    holdings = []
    for item in raw_data.get("output1", raw_data.get("holdings", [])):
        holdings.append({
            "broker": "KB증권",
            "name": item.get("prdt_name") or item.get("name") or "",
            "qty": item.get("hldg_qty") or item.get("qty") or 0,
            "buy": item.get("pchs_avg_pric") or item.get("buy_price") or 0,
            "cur": item.get("prpr") or item.get("cur_price") or 0,
        })
    return holdings


def main():
    app_key = os.getenv("KB_APP_KEY")
    app_secret = os.getenv("KB_APP_SECRET")
    account_no = os.getenv("KB_ACCOUNT_NO")

    if not all([app_key, app_secret, account_no]):
        print("에러: .env 파일에 KB_APP_KEY / KB_APP_SECRET / KB_ACCOUNT_NO 를 채워주세요.", file=sys.stderr)
        sys.exit(1)

    print("[KB증권] 조회 중...", file=sys.stderr)
    raw = fetch_balance(app_key, app_secret, account_no)
    holdings = normalize_holdings(raw)

    result = {"broker": "KB증권", "holdings": holdings, "raw": raw}
    print(json.dumps(result, ensure_ascii=False, indent=2))

    with open("kb_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n저장됨: kb_output.json", file=sys.stderr)


if __name__ == "__main__":
    main()
