import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title='학급 분석',
    page_icon='🏫',
)

st.title('학급 분석')

sample_checkbox = st.checkbox('샘플 데이터로 체험하기')

uploaded_files = st.file_uploader(
    '결과 CSV 파일을 여러 개 업로드하세요',
    type='csv',
    accept_multiple_files=True,
)

data_frames = []

if sample_checkbox:
    sample_path = Path(__file__).parents[1] / 'data' / 'sample_class.csv'
    if sample_path.exists():
        data_frames.append(pd.read_csv(sample_path))
    else:
        st.error('샘플 데이터 파일을 찾을 수 없습니다: data/sample_class.csv')

for uploaded_file in uploaded_files:
    try:
        data_frames.append(pd.read_csv(uploaded_file))
    except Exception as exc:
        st.warning(f'파일을 읽는 중 오류가 발생했습니다: {uploaded_file.name} ({exc})')

if not data_frames:
    st.info('CSV 파일을 업로드하거나 샘플 데이터로 체험하기를 선택하세요.')
    st.stop()

class_df = pd.concat(data_frames, ignore_index=True)
required_columns = ['이름', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
if list(class_df.columns) != required_columns:
    st.error('CSV 열 형식이 올바르지 않습니다. 열은 이름,A1,A2,B1,B2,C1,C2 여야 합니다.')
    st.stop()

for col in required_columns[1:]:
    class_df[col] = pd.to_numeric(class_df[col], errors='coerce').fillna(0).astype(int)

class_df['총점'] = class_df[['A1', 'A2', 'B1', 'B2', 'C1', 'C2']].sum(axis=1)

exam_count = len(class_df)
avg_total = class_df['총점'].mean() if exam_count else 0
nbest = int((class_df['총점'] == 6).sum())
max_score = int(class_df['총점'].max()) if exam_count else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric('응시 인원', exam_count)
col2.metric('평균 총점', f'{avg_total:.2f} / 6')
col3.metric('최고점', max_score)
col4.metric('만점자 수', nbest)

question_cols = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
question_categories = {
    'A1': '내용 이해',
    'A2': '내용 이해',
    'B1': '맥락 파악',
    'B2': '맥락 파악',
    'C1': '주장·근거 분석',
    'C2': '주장·근거 분석',
}

question_stats = [
    {
        '문항': col,
        '정답률': class_df[col].mean() * 100,
        '영역': question_categories[col],
    }
    for col in question_cols
]
question_df = pd.DataFrame(question_stats)

area_stats = []
for area, cols in [('내용 이해', ['A1', 'A2']), ('맥락 파악', ['B1', 'B2']), ('주장·근거 분석', ['C1', 'C2'])]:
    area_score = class_df[cols].sum(axis=1).mean()
    area_stats.append({'영역': area, '평균 점수': area_score})
area_df = pd.DataFrame(area_stats)

st.subheader('문항별 정답률')
fig_questions = px.bar(
    question_df,
    x='문항',
    y='정답률',
    color='영역',
    barmode='group',
    text='정답률',
    color_discrete_map={
        '내용 이해': '#636EFA',
        '맥락 파악': '#EF553B',
        '주장·근거 분석': '#00CC96',
    },
)
fig_questions.update_layout(yaxis_title='정답률 (%)', yaxis=dict(range=[0, 100]), showlegend=True)
fig_questions.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig_questions, use_container_width=True)

st.subheader('영역별 평균 점수')
fig_areas = px.bar(
    area_df,
    x='영역',
    y='평균 점수',
    color='영역',
    text='평균 점수',
    color_discrete_map={
        '내용 이해': '#636EFA',
        '맥락 파악': '#EF553B',
        '주장·근거 분석': '#00CC96',
    },
)
fig_areas.update_layout(yaxis_title='평균 점수 (2점 만점)', yaxis=dict(range=[0, 2]), showlegend=False)
fig_areas.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_areas, use_container_width=True)

st.subheader('총점 분포')
fig_hist = px.histogram(
    class_df,
    x='총점',
    nbins=7,
    text_auto=True,
    range_x=[-0.5, 6.5],
)
fig_hist.update_layout(xaxis_title='총점', yaxis_title='학생 수')
st.plotly_chart(fig_hist, use_container_width=True)

lowest_area = area_df.loc[area_df['평균 점수'].idxmin()]
weak_area = lowest_area['영역']
weak_score = lowest_area['평균 점수']

st.markdown(f'### 이 학급의 취약 영역: {weak_area} ({weak_score:.2f}점)')

suggestions = {
    '내용 이해': '사료의 핵심 문장과 표현을 함께 분석하며, 중요 정보를 빠르게 찾는 연습을 권장합니다.',
    '맥락 파악': '사료가 작성된 시대적 배경과 작성 의도를 중심으로 토론형 학습을 진행하세요.',
    '주장·근거 분석': '주장과 근거를 분리해 파악하는 서술 활동을 늘리고, 논리적 연결을 점검하세요.',
}

st.info(suggestions[weak_area])
if weak_area == '주장·근거 분석':
    st.warning('서술 활동 필요(기말 AI 피드백 앱으로 연습)')
