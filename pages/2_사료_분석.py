import os

import pandas as pd
import plotly.express as px
import streamlit as st

import theme

st.set_page_config(page_title="사료 분석", page_icon="📜", layout="centered")
theme.apply_theme()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
events = pd.read_csv(os.path.join(DATA_DIR, "events.csv"))
cas = pd.read_csv(os.path.join(DATA_DIR, "casualties.csv"))

st.title("📜 사료 분석: 문서와 데이터를 잇다")
st.write("두 편의 사료를 읽고 8개의 질문에 답하세요. 🔗 표시가 있는 질문은 **차트(데이터)와 사료를 연결**해야 풀 수 있어요.")

name = st.text_input("이름 (결과 파일에 기록됩니다)", placeholder="예: 김하늘")

AREA_NAME = {"A": "내용 이해", "B": "맥락 파악", "C": "주장·근거 분석", "D": "자료 연계 해석"}

# =========================================================
# 사료 1 — 윌슨의 14개조 (1918)
# =========================================================
st.header("사료 ① 윌슨의 「14개조 평화 원칙」 (1918. 1.)")
st.markdown("""
<div class="dream-quote">
"강화 조약은 공개적으로 진행되어야 하며, 비밀 외교는 없어야 한다. (제1조)<br>
식민지의 요구를 조정할 때에는 해당 주민의 이익이
동등하게 고려되어야 한다. (제5조)<br>
강대국과 약소국을 가리지 않고 정치적 독립과 영토 보전을 서로 보장하기 위한
국가들의 연합체가 결성되어야 한다. (제14조)"<br>
<span style="opacity:0.7;">— 미국 대통령 윌슨의 의회 연설 요지 (현대어 풀이)</span>
</div>
""", unsafe_allow_html=True)

q = {}

q["A1"] = st.radio(
    "**[A. 내용 이해]** 1. 제14조에서 윌슨이 만들자고 제안한 것은 무엇인가요?",
    ["강대국만의 군사 동맹", "국가들의 연합체(국제기구)", "유럽 단일 국가", "세계 단일 화폐"],
    index=None, key="A1",
)
q["B1"] = st.radio(
    "**[B. 맥락 파악]** 2. 이 연설이 발표된 1918년 1월의 상황으로 알맞은 것은?",
    ["1차 대전이 아직 진행 중이었다", "1차 대전이 끝난 지 10년이 지났다",
     "2차 대전이 시작된 직후였다", "미국은 아직 참전하지 않았다"],
    index=None, key="B1",
)
q["C1"] = st.radio(
    "**[C. 주장·근거 분석]** 3. 이 사료에서 윌슨의 핵심 주장은 무엇인가요?",
    ["전쟁 배상금을 최대한 받아내야 한다", "비밀 외교와 힘의 정치 대신 새로운 국제 질서를 만들어야 한다",
     "식민지를 강대국이 나눠 가져야 한다", "미국이 유럽을 직접 통치해야 한다"],
    index=None, key="C1",
)

st.markdown("**🔗 [D. 자료 연계 해석] 4번 문제는 아래 데이터를 보고 답하세요.**")
mil1 = cas[(cas["전쟁"] == "제1차 세계대전") & (cas["지표"] == "군인 사망")].sort_values("값(만 명)")
fig_d1 = px.bar(mil1, x="값(만 명)", y="국가", orientation="h",
                title="제1차 세계대전 국가별 군인 사망 (만 명)")
st.plotly_chart(fig_d1, use_container_width=True)
q["D1"] = st.radio(
    "4. 위 데이터는 윌슨의 주장이 힘을 얻은 배경을 보여줍니다. 가장 알맞은 해석은?",
    ["미국의 피해가 가장 컸기 때문에 미국이 주도권을 잡았다",
     "여러 나라가 수십~수백만 명의 군인을 잃을 만큼 피해가 컸기에, 전쟁 재발을 막을 장치가 필요했다",
     "사망자가 적어서 전쟁을 한 번 더 해도 된다는 여론이 많았다",
     "데이터와 윌슨의 주장은 아무 관련이 없다"],
    index=None, key="D1",
)

st.divider()

# =========================================================
# 사료 2 — 카이로 선언 (1943)
# =========================================================
st.header("사료 ② 「카이로 선언」 (1943. 11.)")
st.markdown("""
<div class="dream-quote">
"3대 동맹국(미국·영국·중국)은 일본이 폭력과 탐욕으로 빼앗은 모든 지역에서
일본을 몰아내는 것을 목적으로 한다. …<br>
앞의 3대국은 한국 인민의 노예 상태에 유의하여,
적당한 시기에 한국을 자주 독립시킬 것을 결의한다."<br>
<span style="opacity:0.7;">— 카이로 회담 공동 선언 (현대어 풀이)</span>
</div>
""", unsafe_allow_html=True)

q["A2"] = st.radio(
    "**[A. 내용 이해]** 5. 이 선언에서 독립을 약속받은 나라는 어디인가요?",
    ["필리핀", "베트남", "한국", "인도"],
    index=None, key="A2",
)
q["B2"] = st.radio(
    "**[B. 맥락 파악]** 6. 이 선언이 발표된 1943년 11월의 상황으로 알맞은 것은?",
    ["2차 대전이 진행 중이었고, 연합국이 전쟁 이후의 처리를 논의하고 있었다",
     "2차 대전이 이미 끝나 있었다", "일본이 이미 항복한 뒤였다", "미국과 일본이 동맹을 맺고 있었다"],
    index=None, key="B2",
)
q["C2"] = st.radio(
    "**[C. 주장·근거 분석]** 7. 연합국이 '일본을 몰아내야 한다'는 주장의 근거로 내세운 것은?",
    ["일본의 인구가 너무 많다는 것", "일본이 폭력과 탐욕으로 그 지역들을 빼앗았다는 것",
     "일본의 종교가 다르다는 것", "일본의 경제가 약하다는 것"],
    index=None, key="C2",
)

st.markdown("**🔗 [D. 자료 연계 해석] 8번 문제는 아래 데이터를 보고 답하세요.**")
tail = events[(events["연도"] >= 1943) & (events["연도"] <= 1945)]
fig_d2 = px.scatter(
    tail, x="연도", y="유형", color="유형", hover_name="사건", size=[9] * len(tail),
    title="1943–1945 주요 사건 (점 위에 마우스를 올리면 사건 이름이 보여요)",
)
fig_d2.update_layout(showlegend=False)
st.plotly_chart(fig_d2, use_container_width=True)
q["D2"] = st.radio(
    "8. 카이로 선언(1943.11)과 8·15 광복(1945.8) 사이의 연표에서 알 수 있는 사실은?",
    ["선언 즉시 한국이 독립하였다",
     "선언 이후에도 전쟁이 2년 가까이 이어졌고, 일본이 항복한 뒤에야 독립이 실현되었다",
     "카이로 선언 이후 아무 사건도 일어나지 않았다",
     "한국의 독립은 카이로 선언과 관계없이 1943년에 이루어졌다"],
    index=None, key="D2",
)

# =========================================================
# 채점
# =========================================================
ANSWERS = {
    "A1": "국가들의 연합체(국제기구)",
    "B1": "1차 대전이 아직 진행 중이었다",
    "C1": "비밀 외교와 힘의 정치 대신 새로운 국제 질서를 만들어야 한다",
    "D1": "여러 나라가 수십~수백만 명의 군인을 잃을 만큼 피해가 컸기에, 전쟁 재발을 막을 장치가 필요했다",
    "A2": "한국",
    "B2": "2차 대전이 진행 중이었고, 연합국이 전쟁 이후의 처리를 논의하고 있었다",
    "C2": "일본이 폭력과 탐욕으로 그 지역들을 빼앗았다는 것",
    "D2": "선언 이후에도 전쟁이 2년 가까이 이어졌고, 일본이 항복한 뒤에야 독립이 실현되었다",
}
ITEM_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]

st.divider()
if st.button("제출하고 나의 문해력 보기 🌠", type="primary", use_container_width=True):
    unanswered = [k for k in ITEM_ORDER if q[k] is None]
    if unanswered:
        st.warning(f"아직 답하지 않은 문항이 있어요: {', '.join(unanswered)}")
        st.stop()

    scores = {k: int(q[k] == ANSWERS[k]) for k in ITEM_ORDER}
    area_df = pd.DataFrame([
        {"영역": f"{a}. {AREA_NAME[a]}", "점수": scores[a + "1"] + scores[a + "2"]}
        for a in ["A", "B", "C", "D"]
    ])
    total = int(area_df["점수"].sum())

    st.subheader("🌠 나의 역사 문해력")
    st.metric("총점", f"{total} / 8")

    radar = px.line_polar(
        area_df, r="점수", theta="영역", line_close=True, range_r=[0, 2],
        title="영역별 점수 (각 2점 만점)",
    )
    radar.update_traces(fill="toself", fillcolor="rgba(184,167,234,0.25)",
                        line_color="#b8a7ea")
    st.plotly_chart(radar, use_container_width=True)

    tips = {
        "A. 내용 이해": "사료의 숫자·대상·행동 같은 사실 정보에 밑줄을 그으며 읽어 보세요.",
        "B. 맥락 파악": "'누가, 언제, 어떤 상황에서 썼을까?'를 먼저 묻는 습관을 들여 보세요.",
        "C. 주장·근거 분석": "'글쓴이가 하려는 것(주장)'과 '그 이유(근거)'를 한 문장씩 구분해 써 보세요.",
        "D. 자료 연계 해석": "사료를 읽은 뒤, 관련된 데이터(연표·통계)를 찾아 '이 숫자가 이 문서를 어떻게 설명해 주지?'라고 물어 보세요.",
    }
    weak = area_df[area_df["점수"] < 2]["영역"].tolist()
    if not weak:
        st.success("✨ 모든 영역 만점! 문서와 데이터를 넘나들며 읽는 진짜 역사가의 눈을 갖고 있네요.")
        st.balloons()
    else:
        for w in weak:
            st.warning(f"**{w}** — {tips[w]}")

    with st.expander("문항별 정오표 보기"):
        for k in ITEM_ORDER:
            mark = "✅" if scores[k] else "❌"
            st.write(f"{mark} **{k}** [{AREA_NAME[k[0]]}] 정답: {ANSWERS[k]}")

    result_df = pd.DataFrame([{"이름": name if name else "이름없음", **scores}])
    csv = result_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 내 결과 내려받기 (선생님께 제출)",
        data=csv, file_name=f"문해력진단_{name if name else '이름없음'}.csv",
        mime="text/csv", use_container_width=True,
    )