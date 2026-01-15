import random
from pathlib import Path

import streamlit as st
from algo_problems import PROBLEMS


# ---------- Config ----------
st.set_page_config(
    page_title="F팀 막냉이 주원이",
    page_icon="💌",
    layout="wide",
)

BASE_DIR = Path(__file__).parent
LETTERS_DIR = BASE_DIR / "letters"
ASSETS_DIR = BASE_DIR / "assets"

TITLE = 'F팀 막냉이 주원이를 생각하는 형/누나들의 마음~'

PEOPLE = [
    {"label": "세욱이형", "slug": "세욱"},
    {"label": "민재형", "slug": "민재"},
    {"label": "두산이형", "slug": "두산"},
    {"label": "필도형", "slug": "필도"},
    {"label": "소은이누나", "slug": "소은"},
    {"label": "원렬이형", "slug": "원렬"},
    {"label": "종진이형", "slug": "종진"},
    {"label": "예빈이누나", "slug": "예빈"},
    {"label": "태백이형", "slug": "태백"},
    {"label": "정훈이형", "slug": "정훈"},
    {"label": "민석이형", "slug": "민석"},
    {"label": "세원이누나", "slug": "세원"},
]


def load_md(slug: str) -> str:
    p = LETTERS_DIR / f"{slug}.md"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return "아직 편지가 비어있어! 여기에 내용을 붙여넣어줘 🙂"


def find_image(slug: str):
    # jpg/png/webp 순서로 탐색
    for ext in ["jpg", "png", "webp", "jpeg"]:
        p = ASSETS_DIR / f"{slug}.{ext}"
        if p.exists():
            return str(p)
    return None


def cover_image():
    for ext in ["jpg", "png", "webp", "jpeg"]:
        p = ASSETS_DIR / f"cover.{ext}"
        if p.exists():
            return str(p)
    return None


# ---------- Style ----------
st.markdown(
    """
    <style>
      .title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
      }
      .subtitle {
        text-align: center;
        opacity: 0.85;
        margin-bottom: 1.2rem;
      }
      .card {
        border: 1px solid rgba(49,51,63,0.2);
        border-radius: 16px;
        padding: 18px 18px 6px 18px;
        background: rgba(255,255,255,0.02);
      }
      .small-muted {
        opacity: 0.7;
        font-size: 0.9rem;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Main ----------
st.markdown(f'<div class="title">{TITLE}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">💌 입대(1/19) 전에, 우리 마음 한가득 모아서 남기는 페이지</div>', unsafe_allow_html=True)

cv = cover_image()
if cv:
    st.image(cv, use_container_width=True)
else:
    st.info("`assets/cover.jpg`(또는 png/webp)를 넣으면 메인 사진이 보여!")

st.markdown("---")

tab_labels = [p["label"] for p in PEOPLE] + ["알고리즘(19)"]
tabs = st.tabs(tab_labels)

# ---------- Letter Tabs ----------
for i, person in enumerate(PEOPLE):
    with tabs[i]:
        st.markdown(f"## To. 주원이 — from **{person['label']}**")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(load_md(person["slug"]))
        st.markdown("</div>", unsafe_allow_html=True)

        img = find_image(person["slug"])
        st.markdown("")
        if img:
            st.image(img, use_container_width=True)
        else:
            st.caption(f"사진을 넣고 싶다면 `assets/{person['slug']}.jpg/png` 파일을 추가해줘!")

# ---------- Algorithm Tab ----------
with tabs[-1]:
    st.markdown("## 🧠 주원이 심심할 틈 없게: 알고리즘 19문제")
    st.markdown(
        "난이도 있는 문제들로 준비했어. **힌트/해설은 숨겨두고** 필요할 때만 열어봐!"
    )

    if "picked" not in st.session_state:
        st.session_state.picked = 0

    cols = st.columns([1, 1, 2])
    with cols[0]:
        if st.button("🎲 랜덤 문제 뽑기"):
            st.session_state.picked = random.randrange(len(PROBLEMS))
    with cols[1]:
        st.session_state.picked = st.number_input(
            "문제 번호",
            min_value=1,
            max_value=len(PROBLEMS),
            value=int(st.session_state.picked) + 1,
            step=1
        ) - 1

    titles = [f"{p['id']:02d}. {p['title']}" for p in PROBLEMS]
    chosen = st.selectbox("문제 선택", titles, index=int(st.session_state.picked))
    idx = titles.index(chosen)
    st.session_state.picked = idx

    p = PROBLEMS[idx]
    st.markdown("---")
    st.markdown(f"### {p['id']:02d}. {p['title']}")
    st.markdown(p["markdown"])

    with st.expander("💡 힌트 열기"):
        st.markdown(p["hint"])

    with st.expander("🧩 해설(개요) 열기"):
        st.markdown(p["solution_outline"])

    st.caption("원하면 내가 여기 문제들을 '주원이 취향'으로 더 악랄(?)하게 커스텀해줄 수도 있어 😈")
