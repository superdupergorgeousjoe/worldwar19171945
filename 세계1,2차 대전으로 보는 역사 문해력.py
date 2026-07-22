import streamlit as st

import theme

st.set_page_config(page_title="두 개의 전쟁, 하나의 질문", page_icon="🌌", layout="wide")
theme.apply_theme()

st.title("🌌 두 개의 전쟁, 하나의 질문")
st.markdown("#### — 데이터와 사료로 읽는 1·2차 세계대전, 그리고 나의 역사 문해력")

st.markdown("""
<div class="dream-card">
<span class="dream-badge">역사 × 데이터 융합 수업</span>
<span class="dream-badge">사료 분석</span>
<span class="dream-badge">문해력 진단</span>
<p style="margin-top:0.8rem;">
두 차례의 세계대전은 숫자로도, 문서로도 기록을 남겼습니다.<br>
이 앱에서 여러분은 <b>114건의 역사 데이터</b>(사건 연표 66건 + 국가별 피해 통계 48건)를 탐험하고,
전쟁이 남긴 <b>두 편의 사료</b>(윌슨의 14개조 · 카이로 선언)를 데이터와 연결해 분석합니다.<br>
여러분의 답은 다시 데이터가 되어, <b>나의 역사 문해력</b>을 네 가지 영역으로 비춰줍니다.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🧭 여정 안내")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
<div class="dream-card">
<h3>1️⃣ 데이터 탐험</h3>
<p>사건 연표와 피해 통계를 차트로 탐험하며 전쟁의 크기를 몸으로 느껴 보세요.</p>
</div>
""", unsafe_allow_html=True)
with c2:
    st.markdown("""
<div class="dream-card">
<h3>2️⃣ 사료 분석</h3>
<p>사료를 읽고 8개의 질문에 답하세요. 데이터와 사료를 <b>연결</b>하는 질문도 있어요.
제출하면 나의 문해력이 네 영역으로 시각화됩니다.</p>
</div>
""", unsafe_allow_html=True)
with c3:
    st.markdown("""
<div class="dream-card">
<h3>3️⃣ 학급 분석 (교사)</h3>
<p>학생들의 결과 파일을 모아 학급 전체의 강점과 약점을 데이터로 진단합니다.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📐 역사 문해력 네 영역")
st.markdown("""
<div class="dream-card">
<p>
🔍 <b>A. 내용 이해</b> — 사료에 쓰인 사실 정보를 정확히 파악한다<br>
🏛️ <b>B. 맥락 파악</b> — 사료가 쓰인 시대 상황과 작성 주체를 이해한다<br>
⚖️ <b>C. 주장·근거 분석</b> — 사료 속 주장과 그것을 뒷받침하는 근거를 구분한다<br>
🔗 <b>D. 자료 연계 해석</b> — 사료와 통계 데이터를 서로 연결하여 해석한다
</p>
</div>
""", unsafe_allow_html=True)

st.caption("⚠️ 피해 통계는 널리 인용되는 추정치로, 출처에 따라 차이가 있습니다 — 이것 또한 역사 데이터를 읽을 때 기억해야 할 점이에요.")
st.caption("🚀 다음 버전 예고: 서술형 답변에 AI가 주장·근거·추론을 피드백하는 기능 (기말 프로젝트)")
