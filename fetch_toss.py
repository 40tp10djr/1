"""
토스증권 Open API에서 계좌 평가손익 / 보유종목을 가져오는 스크립트.

★ 반드시 본인 컴퓨터(로컬)에서 실행하세요. Claude 클라우드 환경에서는
  금융기관 API 도메인으로 나가는 네트워크가 막혀 있어 동작하지 않습니다.

공식 문서 기준(developers.tossinvest.com, openapi.tossinvest.com)으로 작성했지만,
Claude가 실제로 호출 테스트를 해보지 못했습니다. 아래 두 지점은 실행해보고
에러가 나면 openapi.tossinvest.com/openapi-docs/latest/openapi.json (브라우저로 열어서
Ctrl+F로 "accounts", "holdings", "asset" 검색) 를 참고해 경로를 맞춰주세요.
  1) ACCOUNTS_PATH  - 계좌 목록 조회 경로
  2) HOLDINGS_PATH  - 보유종목/평가손익 조회 경로 (계좌번호를 {account} 자리에 대입)
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openapi.tossinvest.com"
TOKEN_PATH = "/oauth2/token"
ACCOUNTS_PATH = "/v1/accounts"                 # 확인 필요 시 openapi.json 참고
HOLDINGS_PATH = "/v1/accounts/holdings"        # 확인 필요 시 openapi.json 참고


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
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_holdings(access_token: str, account_no: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Tossinvest-Account": account_no,
    }
    resp = requests.get(BASE_URL + HOLDINGS_PATH, headers=headers, timeout=10)
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

    # 표준화된 형태로 변환 (update_dashboard.py 가 읽는 포맷)
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
