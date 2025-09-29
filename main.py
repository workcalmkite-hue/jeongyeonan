# app.py
import streamlit as st
from datetime import date, datetime, timedelta
import random
import textwrap

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="용차니 전용 앱", page_icon="💙", layout="wide")

# -----------------------------
# 세션 상태 초기화
# -----------------------------
def init_state():
    ss = st.session_state
    ss.setdefault("todos", [])
    ss.setdefault("notes", [])
    ss.setdefault("photos", [])  # {"bytes":..., "caption":...}
    ss.setdefault("custom_events", [])  # {"name":..., "date":date}
    ss.setdefault("first_date", None)
    ss.setdefault("quiz_records", [])  # 기록 저장
    ss.setdefault("name_to", "용차니")  # 남자친구 이름
    ss.setdefault("name_from", "궁딩이")  # 보낸 사람 기본값(원하면 변경)
    ss.setdefault("vibe", "귀여움")
init_state()

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

def wrap(text: str, width: int = 38) -> str:
    return "\n".join(textwrap.wrap(text, width=width))

def love_msg(name_from: str, name_to: str, vibe: str, context: str) -> str:
    base = {
        "귀여움": [
            "요즘 내 행복 지수? {to} 생각만 해도 100점💯",
            "{to}, 너는 내 도파민 버튼이야☺️ 클릭하면 바로 웃음!",
            "세상 공식 발견: {to} + 나 = 완벽 조합🧪💕",
        ],
        "진지": [
            "{to}, 네가 있어서 하루가 안정돼. 너는 내 기준점.",
            "우리가 쌓는 오늘이 내일의 버팀목이라는 걸 믿어.",
            "같이 성장하는 우리, 그게 내가 바라는 사랑의 모양이야.",
        ],
        "응원": [
            "{to}, 오늘도 네 페이스대로 가자. 난 항상 네 편📣",
            "잠깐의 느림도 도약을 위한 준비⏳ 충분히 잘하고 있어!",
            "지치면 기대. 어깨는 내가 낼게💪 같이 가자.",
        ],
        "사과": [
            "감정이 앞섰던 것 같아. 미안해 {to}. 더 잘 들을게.",
            "우리 사이가 가장 소중해. 마음 다치게 해서 미안해.",
            "조금 천천히, 더 다정하게. 다시 손 꼭 잡자.",
        ],
    }
    line = random.choice(base.get(vibe, base["귀여움"]))
    extra = f"\n\n📝 {wrap(context)}" if context.strip() else ""
    return line.format(to=name_to) + extra

def chip(label: str):
    st.markdown(f"<span style='background:#f1f5f9;padding:4px 10px;border-radius:999px;font-size:12px'>{label}</span>", unsafe_allow_html=True)

def score_badge(score: int, total: int):
    ratio = score / max(total, 1)
    if ratio == 1:
        return "🏆 퍼펙트!"
    elif ratio >= 0.8:
        return "🌟 거의 완벽!"
    elif ratio >= 0.6:
        return "👍 좋아!"
    else:
        return "💪 다음엔 더 잘할 수 있어!"

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("💙 용차니 컨트롤 패널")
    st.text_input("남자친구 이름", key="name_to")
    st.text_input("보내는 사람(선택)", key="name_from")
    st.selectbox("메시지 분위기", ["귀여움", "진지", "응원", "사과"], key="vibe")
    st.divider()

    st.subheader("📅 우리 기념일")
    first = st.date_input("처음 만난 날(선택)", value=st.session_state.first_date or date.today(), key="first_date")
    if first:
        diff = (date.today() - first).days
        st.metric("함께한 날", f"{diff}일", help="처음 만난 날 기준 D+N")

    st.divider()
    st.caption("Tips")
    st.write("• 아래 탭에서 퀴즈/밸런스게임/데이트 추천을 즐겨봐!\n• 메뉴룰렛은 후보만 적으면 바로 돌려줘요🎰")

# -----------------------------
# 탭 구성
# -----------------------------
tab_home, tab_picker, tab_quiz, tab_todos, tab_events, tab_album = st.tabs(
    ["🏠 홈", "🎲 선택 놀이", "🧠 퀴즈 & OX", "📝 버킷리스트", "🎉 기념일", "📷 사진 한마디"]
)

# -----------------------------
# 🏠 홈
# -----------------------------
with tab_home:
    st.title("용차니 전용 대시보드 💙")
    col1, col2 = st.columns([2,1], vertical_alignment="top")

    with col1:
        st.subheader("✉️ 오늘의 메시지")
        context = st.text_area("메시지에 곁들일 말(선택)", placeholder="오늘 있었던 재미난 일, 응원하고 싶은 말 등")
        if st.button("메시지 생성하기 ✨", use_container_width=True):
            msg = love_msg(st.session_state.name_from, st.session_state.name_to, st.session_state.vibe, context)
            st.success(msg)

    with col2:
        st.subheader("⏱️ 미니 타이머")
        mins = st.number_input("분", min_value=0, value=0, step=1)
        secs = st.number_input("초", min_value=0, value=30, step=5)
        if st.button("랜덤 응원 받기 💬", use_container_width=True):
            st.info(random.choice([
                "물 한 잔 마시고 파워업!💧",
                "1분 스트레칭 하고 올까? 🧘",
                "깊게 한숨 쉬고 다시 집중! 🌬️",
                "스스로를 너무 몰아붙이지 말기 🙌",
            ]))
        chip("작고 확실한 행복 모으기")

# -----------------------------
# 🎲 선택 놀이
# -----------------------------
with tab_picker:
    st.header("선택 놀이 & 랜덤 추천 🎲")
    sub1, sub2 = st.columns(2)

    # 밸런스 게임
    with sub1:
        st.subheader("⚖️ 밸런스 게임")
        q1 = st.radio("주말 데이트 스타일은?", ["집콕 넷플릭스", "야외 피크닉"], horizontal=True)
        q2 = st.radio("저녁 메뉴는?", ["파스타", "고기"], horizontal=True)
        q3 = st.radio("여행 타입은?", ["즉흥 번개✈️", "치밀한 계획📋"], horizontal=True)
        if st.button("우리 케미 분석하기 💞"):
            score = sum([q1=="야외 피크닉", q2=="파스타", q3=="치밀한 계획📋"])
            st.success(f"케미 점수: {score}/3 · {score_badge(score,3)}")

    # 메뉴 룰렛 & 데이트 추천
    with sub2:
        st.subheader("🎰 메뉴 룰렛")
        candidates = st.text_area("후보를 줄바꿈으로 입력", "마라탕\n초밥\n치킨\n쌀국수\n피자")
        if st.button("룰렛 돌리기!", type="primary"):
            items = [c.strip() for c in candidates.splitlines() if c.strip()]
            st.info(f"오늘은… **{random.choice(items)}** 어떠세요? 🍽️")

        st.markdown("---")
        st.subheader("💡 랜덤 데이트 제안")
        mood = st.selectbox("오늘의 무드", ["힐링", "액티브", "실내", "감성"], index=0)
        budget = st.slider("예상 예산(원)", 0, 100000, 30000, step=5000)
        ideas = {
            "힐링": ["한강 돗자리+라면", "도서관 데이트", "카페 투어(조용한 곳)"],
            "액티브": ["볼링+버블티", "실내 암벽", "자전거 타기"],
            "실내": ["보드게임 카페", "쿠킹클래스", "방탈출"],
            "감성": ["전시회+폴라로이드", "중고서점 산책", "야경 산책+사진"],
        }
        picked = random.choice(ideas[mood])
        if st.button("아이디어 뽑기 🎁"):
            st.success(f"추천: **{picked}** (예산 가이드 ~{budget:,}원)")

# -----------------------------
# 🧠 퀴즈 & OX
# -----------------------------
with tab_quiz:
    st.header("용차니 퀴즈존 🧠")
    quiz_tab1, quiz_tab2, quiz_tab3 = st.tabs(["🎯 객관식 퀴즈", "⭕️❌ OX 퀴즈", "🛠️ 내가 직접 만들기"])

    # 기본 객관식 퀴즈
    with quiz_tab1:
        st.subheader("나를 얼마나 알까? ‘스피드 5문제’")
        questions = [
            {
                "q": "내가 가장 좋아하는 커피 타입은?",
                "opts": ["아메리카노", "라떼", "콜드브루", "디카페인 드립"],
                "ans": 3
            },
            {
                "q": "이상적인 데이트 시간대는?",
                "opts": ["아침", "점심", "저녁", "새벽"],
                "ans": 2
            },
            {
                "q": "싫어하는 음식은?",
                "opts": ["고수", "올리브", "민트초코", "버섯"],
                "ans": 0
            },
            {
                "q": "가고 싶은 여행지는?",
                "opts": ["제주", "부산", "강릉", "여수"],
                "ans": 0
            },
            {
                "q": "피곤한 날 듣는 말 중 최고는?",
                "opts": ["수고했어!", "맛있는 거 먹자", "오늘은 내가 운전", "일찍 자자"],
                "ans": 1
            },
        ]
        user_answers = []
        for i, item in enumerate(questions, 1):
            user_answers.append(
                st.radio(f"{i}. {item['q']}", item["opts"], index=None, key=f"mc_{i}")
            )

        if st.button("채점하기 ✅"):
            score = 0
            for i, item in enumerate(questions):
                if user_answers[i] is not None and item["opts"].index(user_answers[i]) == item["ans"]:
                    score += 1
            st.success(f"점수: {score}/5 · {score_badge(score, 5)}")
            st.session_state.quiz_records.append(
                {"when": datetime.now().strftime("%Y-%m-%d %H:%M"), "mode": "객관식", "score": score, "total": 5}
            )

    # OX 퀴즈
    with quiz_tab2:
        st.subheader("스피드 OX")
        ox_bank = [
            ("나는 아침형 인간이다.", False),
            ("매운 음식 잘 먹는다.", True),
            ("비 오는 날을 좋아한다.", True),
            ("보드게임보다 퍼즐을 더 좋아한다.", False),
            ("영화관 팝콘은 달콤이파다.", True),
        ]
        ox_ans = []
        for i, (qq, _) in enumerate(ox_bank, 1):
            val = st.radio(f"{i}. {qq}", ["⭕️", "❌"], index=None, horizontal=True, key=f"ox_{i}")
            ox_ans.append(val)

        if st.button("OX 채점하기 ✅"):
            score = 0
            for i, (_, correct) in enumerate(ox_bank):
                if ox_ans[i] is None: 
                    continue
                user_true = (ox_ans[i] == "⭕️")
                if user_true == correct:
                    score += 1
            st.info(f"결과: {score}/{len(ox_bank)} · {score_badge(score, len(ox_bank))}")
            st.session_state.quiz_records.append(
                {"when": datetime.now().strftime("%Y-%m-%d %H:%M"), "mode": "OX", "score": score, "total": len(ox_bank)}
            )

    # 커스텀 퀴즈 작성
    with quiz_tab3:
        st.subheader("내가 만드는 ‘용차니 맞춤 퀴즈’")
        n = st.number_input("문항 수", 1, 10, 3)
        custom_qs = []
        for i in range(int(n)):
            st.markdown(f"**문항 {i+1}**")
            q = st.text_input(f"질문 {i+1}", key=f"cq_{i}", placeholder="예: 내가 제일 좋아하는 색은?")
            opts = st.text_area(f"선택지(줄바꿈으로 입력) {i+1}", "빨강\n파랑\n초록")
            ans_idx = st.number_input(f"정답 인덱스(0부터) {i+1}", 0, 9, 0, key=f"ca_{i}")
            custom_qs.append((q, [o.strip() for o in opts.splitlines() if o.strip()], int(ans_idx)))

        if st.button("커스텀 퀴즈 시작 ▶️"):
            score = 0
            for i, (q, opts, ans_idx) in enumerate(custom_qs, 1):
                choice = st.radio(q or f"문항 {i}", opts or ["옵션1","옵션2"], index=None, key=f"play_{i}")
                if st.button(f"문항 {i} 잠정 채점", key=f"chk_{i}"):
                    if choice is not None and opts and opts.index(choice) == ans_idx:
                        st.success("정답! ✅")
                        score += 1
                    else:
                        st.error(f"오답! 정답: {opts[ans_idx] if opts and 0 <= ans_idx < len(opts) else '설정필요'}")
            if st.button("전체 점수 저장 💾"):
                st.session_state.quiz_records.append({"when": datetime.now().strftime("%Y-%m-%d %H:%M"), "mode": "커스텀", "score": score, "total": len(custom_qs)})
                st.success("저장 완료!")

    st.markdown("---")
    st.subheader("📊 최근 퀴즈 기록")
    if st.session_state.quiz_records:
        for r in reversed(st.session_state.quiz_records[-10:]):
            chip(f"{r['when']} · {r['mode']} · {r['score']}/{r['total']}")
    else:
        st.caption("아직 기록이 없어요. 퀴즈를 한 번 시작해볼까요?")

# -----------------------------
# 📝 버킷리스트 / 할 일
# -----------------------------
with tab_todos:
    st.header("우리 버킷리스트 📝")
    new_item = st.text_input("추가할 항목", placeholder="예: 가을 단풍 구경 가기")
    if st.button("추가 ➕"):
        if new_item.strip():
            st.session_state.todos.append({"text": new_item.strip(), "done": False})
    for i, t in enumerate(st.session_state.todos):
        cols = st.columns([0.1, 0.75, 0.15])
        with cols[0]:
            st.session_state.todos[i]["done"] = st.checkbox("완료", value=t["done"], key=f"todo_{i}")
        with cols[1]:
            st.write("~~" + t["text"] + "~~" if t["done"] else t["text"])
        with cols[2]:
            if st.button("삭제", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()

# -----------------------------
# 🎉 기념일
# -----------------------------
with tab_events:
    st.header("기념일 & 디데이 🎉")
    colA, colB = st.columns(2)
    with colA:
        name = st.text_input("이벤트 이름", placeholder="예: 100일")
        when = st.date_input("날짜 선택", value=date.today())
        if st.button("기념일 추가 ➕"):
            st.session_state.custom_events.append({"name": name or "이벤트", "date": when})
    with colB:
        st.subheader("다가오는 일정")
        if not st.session_state.custom_events:
            st.caption("아직 등록된 일정이 없어요.")
        else:
            for ev in sorted(st.session_state.custom_events, key=lambda e: e["date"]):
                d = days_until(ev["date"])
                st.write(f"• **{ev['name']}** : {ev['date']} · {format_datediff(d)}")

# -----------------------------
# 📷 사진 한마디
# -----------------------------
with tab_album:
    st.header("사진 한마디 📷")
    up = st.file_uploader("사진 올리기(JPG/PNG)", type=["jpg","jpeg","png"])
    cap = st.text_input("캡션(선택)", placeholder="우리 오늘 진짜 귀여웠다 😆")
    cols = st.columns([0.3,0.7])
    with cols[0]:
        if st.button("추가하기 ➕"):
            if up is not None:
                st.session_state.photos.append({"bytes": up.getvalue(), "caption": cap})
                st.success("추가 완료!")
    with cols[1]:
        if st.session_state.photos:
            st.subheader("앨범")
            for i, ph in enumerate(reversed(st.session_state.photos)):
                st.image(ph["bytes"], caption=ph["caption"], use_column_width=True)
        else:
            st.caption("아직 사진이 없어요. 첫 사진을 올려볼까요? 📸")

# -----------------------------
# 푸터
# -----------------------------
st.markdown("<hr/>", unsafe_allow_html=True)
st.caption("Made for 용차니 💙  |  Created by 정연의 Streamlit 앱")
