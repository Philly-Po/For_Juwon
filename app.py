# app.py
# -*- coding: utf-8 -*-

import random
import datetime as dt
from pathlib import Path

import streamlit as st
from algo_problems import PROBLEMS  # PROBLEMS: [{"id","title","body","hint","solution"}, ...]

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="F팀 막냉이 주원이",
    page_icon="💌",
    layout="wide",
)

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).parent
LETTERS_DIR = BASE_DIR / "letters"
ASSETS_DIR = BASE_DIR / "assets"

# ---------------------------
# Data
# ---------------------------
TITLE = "F팀 막냉이 주원이를 생각하는 형/누나들의 마음~"
SUBTITLE = "💌 2026.01.19 입대 전, 우리 마음 한가득 모아둔 페이지"

# 슬러그는 파일명/이미지명과 연결됩니다:
# letters/<slug>.md, assets/<slug>.jpg(or png/webp)
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

# ---------------------------
# Helpers
# ---------------------------
def _find_asset(name_no_ext: str):
    for ext in ["jpg", "png", "webp", "jpeg"]:
        p = ASSETS_DIR / f"{name_no_ext}.{ext}"
        if p.exists():
            return str(p)
    return None


def cover_image():
    return _find_asset("cover")


def find_person_image(slug: str):
    return _find_asset(slug)

def find_person_images(slug: str):
    # assets 폴더에서 slug로 시작하는 이미지 전부 찾기 (예: seuk_1.jpg, seuk_2.png ...)
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    paths = []
    if ASSETS_DIR.exists():
        for p in ASSETS_DIR.iterdir():
            if p.is_file() and p.suffix.lower() in exts and p.stem.lower().startswith(slug.lower()):
                paths.append(str(p))
    # 보기 좋게 파일명 기준 정렬
    paths.sort()
    return paths

def render_image_gallery(paths: list[str]):
    if not paths:
        return
    # 1장은 그냥 크게, 여러 장이면 2~3열 갤러리
    if len(paths) == 1:
        st.image(paths[0], use_container_width=True)
    else:
        cols = st.columns(2, gap="small")  # 2열 (원하면 3으로 바꿔도 됨)
        for i, img_path in enumerate(paths):
            with cols[i % 2]:
                st.image(img_path, width="stretch")


def load_md(slug: str) -> str:
    p = LETTERS_DIR / f"{slug}.md"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return (
        "아직 편지가 비어있어!\n\n"
        "여기에 내용을 **그대로 복붙**해주면 돼 🙂\n\n"
        f"- 파일 위치: `letters/{slug}.md`"
    )


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


# ---------------------------
# CSS (Pretty UI)
# ---------------------------
st.markdown(
    """
<style>
.stApp {
  background: radial-gradient(1200px 600px at 10% 0%, rgba(255, 230, 240, 0.35), transparent 60%),
              radial-gradient(1200px 600px at 90% 0%, rgba(210, 240, 255, 0.35), transparent 60%),
              linear-gradient(180deg, rgba(255,255,255,0.96), rgba(255,255,255,0.92));
}

.main .block-container {
  padding-top: 1.2rem;
  padding-bottom: 2rem;
  max-width: 1100px;
}

.hero-title {
  text-align:center;
  font-weight: 900;
  font-size: 2.2rem;
  letter-spacing: -0.6px;
  margin: 0.15rem 0 0.35rem 0;
}

.hero-sub {
  text-align:center;
  opacity: 0.78;
  margin-bottom: 1.0rem;
}

.badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.85rem;
  border: 1px solid rgba(49,51,63,0.12);
  background: rgba(255,255,255,0.78);
  margin: 0 4px;
}

.card {
  border: 1px solid rgba(49,51,63,0.10);
  background: rgba(255,255,255,0.78);
  border-radius: 18px;
  padding: 18px 18px 12px 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.06);
  backdrop-filter: blur(6px);
}

.small-muted {
  opacity: 0.72;
  font-size: 0.9rem;
}

.stTabs [data-baseweb="tab"] {
  padding: 10px 12px;
}

details {
  border-radius: 14px !important;
  border: 1px solid rgba(49,51,63,0.10) !important;
  background: rgba(255,255,255,0.74) !important;
}

hr {
  border: none;
  height: 1px;
  background: rgba(49,51,63,0.10);
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar (D-day, 안내)
# ---------------------------
with st.sidebar:
    st.markdown("### 📌 안내")
    st.write("주원이 들어오면 탭 눌러서 편지 읽고, 마지막에 알고리즘 풀기!")
    st.markdown("---")

    target = dt.date(2026, 1, 19)
    today = dt.date.today()
    diff = (target - today).days
    st.markdown("### ⏳ D-Day")
    st.metric("입대까지", f"D-{max(diff, 0)}")

    st.markdown("---")
    st.markdown("### 🧩 구성")
    st.write("• 편지 12개 탭\n• 알고리즘 19문제 탭")


# ---------------------------
# Hero header
# ---------------------------
st.markdown(f'<div class="hero-title">{TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-sub">{SUBTITLE}</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;">'
    '<span class="badge">12개의 편지</span>'
    '<span class="badge">+ 알고리즘 19문제</span>'
    "</div>",
    unsafe_allow_html=True,
)
st.write("")

cv = cover_image()
if cv:
    st.image(cv, width="stretch")

else:
    st.info("메인 사진 넣고 싶으면 `assets/cover.jpg`(또는 png/webp) 파일을 추가해줘!")

st.markdown("---")

# ---------------------------
# Tabs
# ---------------------------
tab_labels = [p["label"] for p in PEOPLE] + ["알고리즘(19)"]
tabs = st.tabs(tab_labels)

# ---------------------------
# Letter tabs (12)
# ---------------------------
for i, person in enumerate(PEOPLE):
    with tabs[i]:
        st.markdown(f"## To. 주원이 — from **{person['label']}**")
        left, right = st.columns([2, 1], gap="large")

        with left:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(load_md(person["slug"]))
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img = find_person_image(person["slug"])
            if img:
                st.image(img, use_container_width=True)
            else:
                st.markdown(
                    f'<div class="small-muted">사진을 넣고 싶으면 아래 파일을 추가해줘:</div>'
                    f'<div class="small-muted"><code>assets/{person["slug"]}.jpg</code> (또는 png/webp)</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Algorithm tab
# ---------------------------
with tabs[-1]:
    st.markdown("## 🧠 알고리즘 19문제")
    st.markdown('<div class="small-muted">힌트/해설은 필요할 때만 열어봐 🙂</div>', unsafe_allow_html=True)
    st.write("")

    if "picked_idx" not in st.session_state:
        st.session_state.picked_idx = 0

    n_probs = len(PROBLEMS)
    if n_probs == 0:
        st.warning("PROBLEMS가 비어있어! algo_problems.py를 확인해줘.")
    else:
        top = st.columns([1, 1, 3], gap="medium")

        with top[0]:
            if st.button("🎲 랜덤 뽑기", use_container_width=True):
                st.session_state.picked_idx = random.randrange(n_probs)

        with top[1]:
            num = st.number_input(
                "문제 번호",
                min_value=1,
                max_value=n_probs,
                value=clamp(int(st.session_state.picked_idx) + 1, 1, n_probs),
                step=1,
            )
            st.session_state.picked_idx = int(num) - 1

        titles = [f"{p['id']:02d}. {p['title']}" for p in PROBLEMS]
        chosen = st.selectbox("문제 선택", titles, index=clamp(int(st.session_state.picked_idx), 0, n_probs - 1))
        idx = titles.index(chosen)
        st.session_state.picked_idx = idx

        p = PROBLEMS[idx]

        st.markdown("---")
        st.markdown(f"### {p['id']:02d}. {p['title']}")

        # Body card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(p.get("body", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        with st.expander("💡 힌트 열기"):
            st.markdown(p.get("hint", "") or "힌트 준비 중!")

        with st.expander("🧩 해설(개요) 열기"):
            st.markdown(p.get("solution", "") or "해설 준비 중!")
