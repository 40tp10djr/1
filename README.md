# KB증권·토스증권 잔고/손익 자동 조회 스크립트

이 스크립트들은 **반드시 본인 컴퓨터(로컬)에서** 실행해야 합니다. Claude가
작업하는 클라우드 환경에서는 은행/증권사 API 도메인으로 나가는 네트워크가
보안상 막혀 있어서 실행할 수 없습니다.

## 0. 준비

```bash
cd pnl_automation
python -m venv venv
source venv/bin/activate      # Windows는 venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` 파일을 열어 KB증권/토스증권 appKey·appSecret·계좌번호를 채워넣으세요.
**이 파일은 절대 다른 곳에 공유하거나 깃허브에 올리지 마세요.**

## 1. 토스증권 조회

```bash
python fetch_toss.py
```

공식 문서 기준으로 작성했지만 실제 호출 테스트는 못 해봤습니다. 에러가 나면
`https://openapi.tossinvest.com/openapi-docs/latest/openapi.json` 을 브라우저로
열어 정확한 경로를 확인하고 `fetch_toss.py` 안의 `ACCOUNTS_PATH` /
`HOLDINGS_PATH` 를 수정해주세요.

## 2. KB증권 조회

KB증권은 로그인해야 API 목록이 보이는 구조라 Claude가 정확한 경로를
확인하지 못했습니다. `fetch_kb.py` 안 안내대로:

1. https://openapi.kbsec.com/apidoc_b2c 로그인
2. "국내주식" 카테고리에서 잔고/평가손익 API 선택
3. Sample Code Generator → PYTHON 코드 생성
4. 그 코드를 `fetch_kb.py`의 `fetch_balance()` 함수 안에 붙여넣기
5. 응답 필드명에 맞춰 `normalize_holdings()` 수정

이후:
```bash
python fetch_kb.py
```

## 3. 대시보드에 반영

```bash
python update_dashboard.py
```

`dashboard_filled.html`이 생성됩니다. 더블클릭해서 열면 최신 평가손익·보유종목이
채워진 상태로 보입니다.

이 파일 내용(또는 화면 캡처, 혹은 그냥 숫자)을 Claude와의 대화창에 붙여넣어주시면,
데스크톱에 저장해둔 아티팩트 대시보드도 같은 내용으로 갱신해드릴게요.

## 4. 매번 실행이 귀찮다면

- macOS/Linux: `cron`으로 `python fetch_toss.py && python fetch_kb.py && python update_dashboard.py`를
  원하는 주기로 등록
- Windows: 작업 스케줄러(Task Scheduler)에 동일하게 등록

## 나중에 신한/메리츠 추가하기

같은 패턴으로 `fetch_shinhan.py`, `fetch_meritz.py`를 추가하면 됩니다. 각 증권사
Open API 신청 후 알려주시면 그때 스켈레톤을 같이 만들어드릴게요.
