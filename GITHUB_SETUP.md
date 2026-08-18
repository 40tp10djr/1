# 갤럭시탭에서 끝까지 설정하는 방법 (컴퓨터 없이 가능)

GitHub은 웹사이트라서 태블릿 브라우저(크롬)만으로 아래 과정을 전부 할 수 있습니다.
한 번만 설정해두면, 이후엔 GitHub 서버가 알아서 매시간 KB증권·토스증권을 조회해
웹페이지를 갱신하고, 태블릿에서는 그 주소만 열어보면 됩니다.

## 1단계. GitHub 가입 (5분)

1. 태블릿 브라우저에서 https://github.com 접속
2. 오른쪽 위 "Sign up" → 이메일, 비밀번호, 아이디 입력해서 무료 가입

## 2단계. 저장소(repository) 만들기

1. 로그인 후 오른쪽 위 "+" → "New repository"
2. Repository name: `pnl-dashboard` (원하는 이름 아무거나)
3. **Private** 선택 (비공개 — 다른 사람이 못 봄)
4. "Create repository" 클릭

## 3단계. 이 zip 파일 안 내용 업로드

1. 방금 만든 저장소 페이지에서 "uploading an existing file" 클릭
   (또는 "Add file" → "Upload files")
2. 이 zip 파일 압축을 태블릿에서 풀어서(파일 앱의 압축풀기 기능 사용), **pnl_automation 폴더 안의 내용물**을
   전부 선택해서 업로드 화면에 끌어다 놓기
   - `.github` 폴더도 숨김 폴더라 안 보일 수 있어요. 안 보이면 파일 앱에서
     "숨김 파일 표시"를 켜거나, PC가 있는 지인에게 이 폴더만 옮겨달라고 부탁하세요.
     (`.github/workflows/update-dashboard.yml` 파일 하나만 있으면 됩니다)
3. 화면 아래 "Commit changes" 클릭

## 4단계. 비밀키 등록 (Secrets)

절대 코드에 직접 쓰지 않고, GitHub의 암호화된 저장소에 넣습니다.

1. 저장소 상단 "Settings" 탭
2. 왼쪽 메뉴 "Secrets and variables" → "Actions"
3. "New repository secret" 클릭해서 아래 6개를 하나씩 등록 (Name은 정확히 똑같이):

| Name | Value |
|---|---|
| `TOSS_CLIENT_ID` | 토스증권 Client ID |
| `TOSS_CLIENT_SECRET` | 토스증권 Client Secret |
| `TOSS_ACCOUNT_NO` | 토스증권 계좌번호 |
| `KB_APP_KEY` | KB증권 appKey |
| `KB_APP_SECRET` | KB증권 appSecret |
| `KB_ACCOUNT_NO` | KB증권 계좌번호 |

## 5단계. GitHub Pages 켜기 (결과를 볼 웹페이지 주소 만들기)

1. Settings → 왼쪽 메뉴 "Pages"
2. "Build and deployment" → Source: **Deploy from a branch**
3. Branch: `main`, 폴더: `/docs` 선택 → Save
4. 몇 분 기다리면 이 페이지 위쪽에 `https://<아이디>.github.io/pnl-dashboard/` 같은 주소가 뜹니다.
   이 주소를 태블릿 즐겨찾기(홈 화면 추가)에 등록해두세요.

## 6단계. 첫 실행 확인

1. 저장소 상단 "Actions" 탭
2. 왼쪽 "Update PnL Dashboard" 클릭 → 오른쪽 "Run workflow" 버튼으로 수동 실행
3. 초록색 체크가 뜨면 성공. 빨간 X가 뜨면 클릭해서 로그를 확인
   - 지금 상태에서는 KB증권 부분은 `fetch_kb.py`를 아직 완성하지 않았다면 실패가
     "정상"입니다(안내 메시지가 뜸). 토스증권만 우선 확인해보세요.
4. 몇 분 후 5단계에서 만든 주소를 태블릿에서 열어보면 최신 숫자가 채워진 대시보드가 보입니다.

## 이후에는?

- 매시 13분마다 자동으로 갱신됩니다 (workflow 파일에서 주기 조절 가능)
- KB증권 fetch_kb.py를 완성하는 부분만 도움이 필요하면, 완성한 코드를 저에게
  보여주시면 같이 점검해드릴게요 — 이때도 실제 appKey/appSecret 값은 다시 안 주셔도 됩니다.
