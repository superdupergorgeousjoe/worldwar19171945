"""몽환(드리미) 테마 — 모든 페이지에서 import 해서 사용합니다."""
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# 몽환 팔레트: 깊은 밤하늘 배경 위 라벤더·별빛 파스텔
DREAM_COLORS = ["#b8a7ea", "#8ec5e8", "#f2b8c6", "#ffd9a0", "#9be8c8", "#e0c3fc"]
BG_DEEP = "#131029"
INK = "#efeaff"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 15% 10%, rgba(120, 90, 200, 0.35) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 20%, rgba(70, 120, 200, 0.28) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 95%, rgba(200, 120, 180, 0.18) 0%, transparent 60%),
        linear-gradient(160deg, #131029 0%, #1d1638 45%, #172042 100%);
    color: #efeaff;
}
[data-testid='stAppViewContainer'],
main,
.block-container,
.css-1d391kg,
.css-1v3fvcr {
    background: transparent !important;
    color: #efeaff !important;
}
h1, h2, h3 { font-family: 'Gowun Batang', serif !important; color: #f3edff !important; letter-spacing: 0.02em; }
p, li, label, .stMarkdown { font-family: 'Noto Sans KR', sans-serif; color: #ddd6f3; }

/* 유리 카드 */
.dream-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(184, 167, 234, 0.35);
    border-radius: 18px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px rgba(20, 10, 60, 0.35);
}
.dream-quote {
    font-family: 'Gowun Batang', serif;
    font-size: 1.05rem;
    line-height: 2.0;
    color: #f5f0ff;
    background: linear-gradient(135deg, rgba(184,167,234,0.14), rgba(142,197,232,0.10));
    border-left: 4px solid #b8a7ea;
    border-radius: 0 16px 16px 0;
    padding: 1.4rem 1.7rem;
    margin: 0.8rem 0;
}
.dream-badge {
    display: inline-block; padding: 2px 14px; border-radius: 999px;
    background: rgba(184,167,234,0.22); border: 1px solid rgba(184,167,234,0.5);
    color: #cfc3f5; font-size: 0.82rem; margin-right: 6px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161231 0%, #1a1a3d 100%);
    border-right: 1px solid rgba(184,167,234,0.25);
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(184,167,234,0.3);
    border-radius: 14px; padding: 0.8rem 1rem;
}
[data-testid="stMetricValue"] { color: #cdbdf6 !important; }
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7a5fd0, #5f7ad0) !important;
    color: #fff !important; border: none !important; border-radius: 12px !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    box-shadow: 0 0 18px rgba(150, 120, 240, 0.55) !important;
}
hr { border-color: rgba(184,167,234,0.25) !important; }
</style>
"""


def apply_theme():
    """페이지 상단에서 한 번 호출: CSS 주입 + plotly 몽환 템플릿 등록."""
    st.markdown(CSS, unsafe_allow_html=True)
    pio.templates["dream"] = go.layout.Template(
        layout=dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Noto Sans KR, sans-serif", color="#ddd6f3", size=13),
            title_font=dict(family="Gowun Batang, serif", size=17, color="#f3edff"),
            colorway=DREAM_COLORS,
            xaxis=dict(gridcolor="rgba(184,167,234,0.15)", zerolinecolor="rgba(184,167,234,0.3)"),
            yaxis=dict(gridcolor="rgba(184,167,234,0.15)", zerolinecolor="rgba(184,167,234,0.3)"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=60, r=20, b=40, l=20),
        )
    )
    pio.templates.default = "dream"


def card(html_inner):
    """유리 카드 안에 내용 넣기."""
    st.markdown(f'<div class="dream-card">{html_inner}</div>', unsafe_allow_html=True)
