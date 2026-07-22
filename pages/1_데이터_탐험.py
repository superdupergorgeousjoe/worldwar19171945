import os

import pandas as pd
import plotly.express as px
import streamlit as st

import theme

st.set_page_config(page_title="데이터 탐험", page_icon="🗺️", layout="wide")
theme.apply_theme()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
events = pd.read_csv(os.path.join(DATA_DIR, "events.csv"))
cas = pd.read_csv(os.path.join(DATA_DIR, "casualties.csv"))

st.title("🗺️ 데이터 탐험: 두 전쟁의 기록")

m1, m2, m3, m4 = st.columns(4)
m1.metric("총 데이터", f"{len(events) + len(cas)}건")
m2.metric("사건 연표", f"{len(events)}건")
m3.metric("피해 통계", f"{len(cas)}건")
m4.metric("기록된 기간", "1914–1945")

st.divider()

# ===== 1. 사건 연표 =====
st.header("1. 사건의 흐름 — 32년의 연표")
sel_type = st.multiselect(
    "사건 유형 선택", events["유형"].unique().tolist(), default=events["유형"].unique().tolist()
)
ev = events[events["유형"].isin(sel_type)]
ev_count = ev.groupby(["연도", "유형"]).size().reset_index(name="사건 수")
fig_tl = px.bar(
    ev_count, x="연도", y="사건 수", color="유형",
    title="연도별 주요 사건 수 (1914–1945)",
)
fig_tl.add_vrect(x0=1913.5, x1=1918.5, fillcolor="#b8a7ea", opacity=0.08, line_width=0,
                 annotation_text="1차 대전", annotation_font_color="#cfc3f5")
fig_tl.add_vrect(x0=1938.5, x1=1945.5, fillcolor="#f2b8c6", opacity=0.08, line_width=0,
                 annotation_text="2차 대전", annotation_font_color="#f2b8c6")
st.plotly_chart(fig_tl, use_container_width=True)

with st.expander("📜 연표 전체 보기 (한국사 연계 사건 포함)"):
    st.dataframe(ev, use_container_width=True, hide_index=True)

st.divider()

# ===== 2. 피해 통계 =====
st.header("2. 전쟁의 크기 — 국가별 피해")
war = st.radio("전쟁 선택", ["제1차 세계대전", "제2차 세계대전"], horizontal=True)
sub = cas[cas["전쟁"] == war]
metric = st.selectbox("지표 선택", sub["지표"].unique().tolist())
sub_m = sub[sub["지표"] == metric].sort_values("값(만 명)", ascending=True)

fig_bar = px.bar(
    sub_m, x="값(만 명)", y="국가", color="진영", orientation="h",
    title=f"{war} — 국가별 {metric} (단위: 만 명)", text="값(만 명)",
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===== 3. 두 전쟁 비교 =====
st.header("3. 두 전쟁, 얼마나 달랐나")
mil = cas[cas["지표"] == "군인 사망"].groupby("전쟁")["값(만 명)"].sum().reset_index()
civ = cas[cas["지표"] == "민간인 사망"].groupby("전쟁")["값(만 명)"].sum().reset_index()
mil["구분"] = "군인 사망"
civ["구분"] = "민간인 사망"
comp = pd.concat([mil, civ])
fig_comp = px.bar(
    comp, x="전쟁", y="값(만 명)", color="구분", barmode="group",
    title="두 전쟁의 사망자 비교 — 2차 대전에서 민간인 피해가 폭증했다 (주요국 합계, 만 명)",
)
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("""
<div class="dream-card">
💭 <b>탐험하며 생각해 보기</b><br>
· 1차 대전 데이터에는 '민간인 사망' 지표가 왜 따로 없을까? 2차 대전과 무엇이 달랐을까?<br>
· 연표에서 <b>한국사 연계</b> 사건 4건을 찾아보자. 세계의 전쟁은 한국의 역사와 어떻게 이어져 있을까?<br>
· 이 통계는 '추정치'다. 전쟁의 피해는 왜 정확히 세기 어려울까?
</div>
""", unsafe_allow_html=True)