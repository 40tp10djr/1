"""
토스증권 Open API에서 계좌 평가손익 / 보유종목을 가져오는 스크립트.
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openapi.tossinvest.com"
TOKEN_PATH = "/oauth2/token"
ACCOUNTS_PATH = "/v1/accounts"
HOLDINGS_PATH = "/v1/accounts/holdings"


def get_access_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(
        BASE_URL + TOKEN_PATH,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=10,
    )
    if not resp.ok:
        print(f"토큰 발급 실패: status={resp.status_code}", file=sys.stderr)
        print(f"응답 내용: {resp.text}", file=sys.stderr)
        print(f"보낸 client_id 길이={len(client_id)}, client_secret 길이={len(client_secret)}", file=sys.stderr)
        print(f"client_id 앞3자리/뒤3자리: {client_id[:3]}...{client_id[-3:]}", file=sys.stderr)
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_holdings(access_token: str, account_no: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": account_no,
    }
    resp = requests.get(BASE_URL + HOLDINGS_PATH, headers=headers, timeout=10)
    if not resp.ok:
        print(f"보유종목 조회 실패: status={resp.status_code}", file=sys.stderr)
        print(f"응답 내용: {resp.text}", file=sys.stderr)
    resp.raise_for_status()
    return resp.json()


def main():
    client_id = os.getenv("TOSS_CLIENT_ID")
    client_secret = os.getenv("TOSS_CLIENT_SECRET")
    account_no = os.getenv("TOSS_ACCOUNT_NO")

    if not all([client_id, client_secret, account_no]):
        print("에러: .env 파일에 TOSS_CLIENT_ID / TOSS_CLIENT_SECRET / TOSS_ACCOUNT_NO 를 채워주세요.", file=sys.stderr)
        sys.exit(1)

    print("[토스증권] 토큰 발급 중...", file=sys.stderr)
    token = get_access_token(client_id, client_secret)

    print("[토스증권] 보유종목 조회 중...", file=sys.stderr)
    data = get_holdings(token, account_no)

    holdings = []
    for item in data.get("holdings", data.get("items", [])):
        holdings.append({
            "broker": "토스증권",
            "name": item.get("name") or item.get("productName") or "",
            "qty": item.get("quantity") or item.get("qty") or 0,
            "buy": item.get("averagePrice") or item.get("buyPrice") or 0,
            "cur": item.get("currentPrice") or item.get("curPrice") or 0,
        })

    result = {"broker": "토스증권", "holdings": holdings, "raw": data}
    print(json.dumps(result, ensure_ascii=False, indent=2))

    with open("toss_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n저장됨: toss_output.json", file=sys.stderr)


if __name__ == "__main__":
    main()
