import os

import streamlit as st
from openai import OpenAI


MODEL = "gpt-4o-mini"

st.set_page_config(
    page_title="OpenAI 챗봇",
    page_icon="💬",
    layout="centered",
)


def get_api_key() -> str | None:
    """Read the key from Streamlit Community Cloud secrets or local env vars."""
    try:
        if st.secrets.get("OPENAI_API_KEY"):
            return st.secrets["OPENAI_API_KEY"]
    except FileNotFoundError:
        pass
    return os.getenv("OPENAI_API_KEY")


def initialize_chat() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요! 무엇을 도와드릴까요?",
            }
        ]


st.title("💬 OpenAI 챗봇")
st.caption(f"Powered by OpenAI · {MODEL}")

api_key = get_api_key()
if not api_key:
    st.error(
        "OpenAI API 키가 설정되지 않았습니다. Streamlit Community Cloud의 "
        "앱 설정 → Secrets에 OPENAI_API_KEY를 추가해 주세요."
    )
    st.code('OPENAI_API_KEY = "sk-..."', language="toml")
    st.stop()

client = OpenAI(api_key=api_key)
initialize_chat()

with st.sidebar:
    st.subheader("설정")
    st.write(f"모델: `{MODEL}`")
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        answer = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                answer += delta
                response_placeholder.markdown(answer + "▌")
            response_placeholder.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as exc:
            response_placeholder.error(
                "응답을 가져오지 못했습니다. API 키와 OpenAI 사용량/결제 설정을 확인해 주세요."
            )
            st.exception(exc)
