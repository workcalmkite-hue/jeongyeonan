# app.py
import streamlit as st
from datetime import date, datetime, timedelta
import random
import textwrap

st.set_page_config(page_title="용차니 전용 앱", page_icon="💙", layout="wide")

# -----------------------------
# 초기 상태
# -----------------------------
if "todos" not in st.session_state:
    st.session_state.todos = []

if "notes" not in st.session_state:
    st.session_state.notes = []

if "photos" not in st.session_state:
    st.session_state.photos = []  # list of dicts: {"bytes":..., "caption":...}

if "custom_events" not in st.session_state:
    st.session_state.custom_events = []  # list of dicts: {"name":..., "date":...}

# -----------------------------
# 유틸 함수
# -----------------------------
def days_until(target: date) -> int:
    return (target - date.today()).days

def format_datediff(d: int) -> str:
    if d > 0:
        return f"{d}일 남음"
    elif d == 0:
        return "오늘이에요! 🎉"
    else:
        return f"{abs(d)}일 지남"

def soft_wrap(text: str, width: int = 36) -> str:
    return "\n".join(textwrap.wrap(text, width=width))

def love_msg(name_from: str, name_to: str, vibe: str, context: str) -> str:
    base = {
        "귀여움": [
            "요즘 내 행복 지수? {to}랑 있을 때 100점 만점에 100점💯",
            "오늘도 {to} 생각하다 미소 터졌어☺️ 너는 내 도파민 버튼✨",
            "세상에 이런 조합 또 있을까? {to} + 나 = 완벽 공식🧪💕",
        ],
        "진지": [
            "{to}, 네가 있어서 내 하루가 안정돼. 너는 내 삶의 기준점이야.",
            "함께한 시간들이 나를 더 단단하게 만들었어. 고마워, {to}.",
            "우리가 쌓는 오늘이 내일의 버팀목이 된다는 걸 믿고 있어.",
        ],
        "응원": [
            "{to}, 오늘도 네 페이스대로 가자. 난 항상 네 편이야📣",
            "잘하고 있어! 잠깐의 느림도 결국 도약을 위해 필요한 시간⏳",
            "지치면 내가 어깨 빌려줄게. 같이 가자, 끝까지💪",
        ],
        "사과": [
            "내 감정이 앞섰던 것 같아. 상처 줘서 미안해, {to}.",
            "더 잘 듣고 더 천천히 말할게. 마음 다칠까 걱정돼.",
            "미안해. 우리의 ‘사이’가 무엇보다 소중하다는 걸 다시 느꼈어.",
        ],
    }
    line = random.choice(base.get(v
