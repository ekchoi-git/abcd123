# Streamlit OpenAI 챗봇

`gpt-4o-mini`를 사용하는 간단한 스트리밍 챗봇입니다.

## 로컬 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`.streamlit/secrets.toml` 파일을 만들고 아래처럼 API 키를 입력합니다.

```toml
OPENAI_API_KEY = "sk-..."
```

그 다음 실행합니다.

```powershell
streamlit run app.py
```

## Streamlit Community Cloud 배포

1. 이 폴더를 GitHub 저장소에 push합니다.
2. Streamlit Community Cloud에서 저장소와 `app.py`를 선택합니다.
3. 앱의 **Settings → Secrets**에 아래 내용을 입력합니다.

```toml
OPENAI_API_KEY = "sk-..."
```

API 키는 소스 코드나 GitHub 저장소에 직접 넣지 마세요.
