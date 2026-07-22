import os

import pandas as pd
import plotly.express as px
import streamlit as st

import theme

st.set_page_config(page_title="학급 분석", page_icon="🔭", layout="wide")
theme.apply_theme()

st.title("🔭 학급 분석 (교사용)")
st.write("학생들이 제출한 결과 파일(CSV)을 올리면 학급 전체의 역사 문해력을 진단합니다. 여러 파일을 한꺼번에 올릴 수 있어요.")

ITEM_COLS = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
AREAS = {
    "A. 내용 이해": ["A1", "A2"],
    "B. 맥락 파악": ["B1", "B2"],
    "C. 주장·근거 분석": ["C1", "C2"],
    "D. 자료 연계 해석": ["D1", "D2"],
}

uploaded_files = st.file_uploader("결과 CSV 업로드", type="csv", accept_multiple_files=True)
use_sample = st.checkbox("📁 샘플 데이터로 체험하기 (가상의 3학년 2반, 30명)")

frames = []
if uploaded_files:
    for f in uploaded_files:
        try:
            frames.append(pd.read_csv(f))
        except Exception:
            f.seek(0)
            frames.append(pd.read_csv(f, encoding="cp949"))
if use_sample:
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_class.csv")
    frames.append(pd.read_csv(sample_path))

if not frames:
    st.info("👆 파일을 올리거나 샘플 데이터를 선택하면 분석이 시작됩니다.")
    st.stop()

df = pd.concat(frames, ignore_index=True)
missing = [c for c in ITEM_COLS if c not in df.columns]
if missing:
    st.error(f"필요한 열이 없습니다: {', '.join(missing)} — 사료 분석 페이지에서 내려받은 결과 파일을 올려 주세요.")
    st.stop()

df[ITEM_COLS] = df[ITEM_COLS].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
df["총점"] = df[ITEM_COLS].sum(axis=1)

st.subheader("1. 학급 요약")
c1, c2, c3, c4 = st.columns(4)
c1.metric("응시 인원", f"{len(df)}명")
c2.metric("평균 총점", f"{df['총점'].mean():.1f} / 8")
c3.metric("최고점", f"{df['총점'].max()} / 8")
c4.metric("만점자", f"{(df['총점'] == 8).sum()}명")

st.subheader("2. 문항별 정답률")
area_of_item = {c: [a for a, cols in AREAS.items() if c in cols][0] for c in ITEM_COLS}
item_rate = pd.DataFrame({
    "문항": ITEM_COLS,
    "정답률(%)": [round(df[c].mean() * 100, 1) for c in ITEM_COLS],
    "영역": [area_of_item[c] for c in ITEM_COLS],
})
fig1 = px.bar(item_rate, x="문항", y="정답률(%)", color="영역", range_y=[0, 100], text="정답률(%)")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("3. 영역별 평균 — 학급의 문해력 지도")
area_df = pd.DataFrame(
    [{"영역": a, "평균 점수": round(df[cols].sum(axis=1).mean(), 2)} for a, cols in AREAS.items()]
)
radar = px.line_polar(area_df, r="평균 점수", theta="영역", line_close=True, range_r=[0, 2],
                      title="영역별 학급 평균 (각 2점 만점)")
radar.update_traces(fill="toself", fillcolor="rgba(142,197,232,0.25)", line_color="#8ec5e8")
col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(radar, use_container_width=True)
with col_b:
    fig3 = px.histogram(df, x="총점", nbins=9, title="총점 분포 (0~8점)")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. 자동 진단")
weakest = area_df.sort_values("평균 점수").iloc[0]
advice = {
    "A. 내용 이해": "사료의 사실 정보 확인(밑줄 긋기, 육하원칙 표) 활동부터 시작해 보세요.",
    "B. 맥락 파악": "사료를 제시할 때 '누가·언제·왜'를 먼저 추측하게 하는 발문이 효과적입니다.",
    "C. 주장·근거 분석": "주장과 근거를 문장으로 구분해 쓰는 서술 활동이 필요합니다. (→ 기말 AI 피드백 앱으로 연습!)",
    "D. 자료 연계 해석": "사료 한 편과 통계 한 장을 짝지어 '데이터로 이 문서를 설명해 보기' 활동을 추천합니다.",
}
st.error(f"이 학급의 취약 영역: **{weakest['영역']}** (평균 {weakest['평균 점수']} / 2)")
st.info(f"💡 수업 제안: {advice[weakest['영역']]}")

with st.expander("전체 데이터 보기"):
    st.dataframe(df, use_container_width=True, hide_index=True)
    