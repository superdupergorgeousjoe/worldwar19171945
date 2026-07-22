import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='사료 진단',
    page_icon='📜',
)

st.title('사료 진단')

st.info(
    '훈민정음 어제 서문의 현대어 풀이:\n'
    '나랏말이 중국과 달라서 문자와 말이 서로 맞지 않으니, \n'
    '백성이 하고자 하는 바를 이루지 못하는 일이 많다. \n'
    '내가 이것을 실로 돕고자 새로운 글자를 만들었노라.'
)

name = st.text_input('이름을 입력하세요')

st.subheader('진단 문항')

questions = {
    'A1': {
        'label': 'A1. 새로 만든 글자 수는 몇 자입니까?',
        'options': [
            '24자',
            '28자',
            '32자',
            '36자',
        ],
        'answer': '28자',
    },
    'A2': {
        'label': 'A2. 사료에서 도우려 한 대상은 누구인가요?',
        'options': [
            '관리',
            '학자',
            '백성',
            '왕',
        ],
        'answer': '백성',
    },
    'B1': {
        'label': 'B1. 이 글이 작성된 당시 상황의 핵심은 무엇인가요?',
        'options': [
            '국가 재정 문제 해결',
            '외국과의 무역 확대',
            '문자와 말이 서로 달라 불편함',
            '군사 전략 수립',
        ],
        'answer': '문자와 말이 서로 달라 불편함',
    },
    'B2': {
        'label': 'B2. 이 사료의 작성 주체는 누구인가요?',
        'options': [
            '세조',
            '세종',
            '문종',
            '집현전 학자',
        ],
        'answer': '세종',
    },
    'C1': {
        'label': 'C1. 글에서 제시하는 주장은 무엇인가요?',
        'options': [
            '새로운 글자를 배우자',
            '새로운 글자를 만든다',
            '기존 문자를 유지한다',
            '외국 문자를 도입한다',
        ],
        'answer': '새로운 글자를 만든다',
    },
    'C2': {
        'label': 'C2. 주장에 대한 근거로 제시된 내용은 무엇인가요?',
        'options': [
            '백성이 글을 잘 몰라서',
            '말과 글이 달라 백성이 뜻을 펴지 못함',
            '관리들이 문자를 독점함',
            '외국 문자가 너무 복잡함',
        ],
        'answer': '말과 글이 달라 백성이 뜻을 펴지 못함',
    },
}

responses = {}
for key, question in questions.items():
    responses[key] = st.radio(
        question['label'],
        question['options'],
        index=None,
        key=key,
    )

submitted = st.button('제출')

if submitted:
    if not name:
        st.warning('이름을 입력해주세요.')
    elif any(value is None for value in responses.values()):
        st.warning('모든 문항을 풀어주세요.')
    else:
        scores = {
            'A': sum(1 for key in ['A1', 'A2'] if responses[key] == questions[key]['answer']),
            'B': sum(1 for key in ['B1', 'B2'] if responses[key] == questions[key]['answer']),
            'C': sum(1 for key in ['C1', 'C2'] if responses[key] == questions[key]['answer']),
        }

        st.success('진단이 완료되었습니다.')
        score_df = pd.DataFrame({
            '영역': ['내용 이해', '맥락 파악', '주장·근거 분석'],
            '점수': [scores['A'], scores['B'], scores['C']],
        })

        fig = px.bar(
            score_df,
            x='영역',
            y='점수',
            range_y=[0, 2],
            text='점수',
            color='영역',
            color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96'],
        )
        fig.update_layout(showlegend=False, yaxis=dict(dtick=1))
        fig.update_traces(textposition='outside')

        st.plotly_chart(fig, use_container_width=True)

        if scores['A'] < 2:
            st.info('내용 이해 연습: 사료의 핵심 정보와 사실을 다시 확인하며, 구체적인 표현을 찾아보세요.')
        if scores['B'] < 2:
            st.info('맥락 파악 연습: 사료가 작성된 시대적 배경과 작성 주체의 목적을 다시 생각해보세요.')
        if scores['C'] < 2:
            st.info('주장·근거 분석 연습: 사료의 주장이 무엇인지 확인하고, 그 주장에 대한 근거를 찾아보세요.')

        result_df = pd.DataFrame([
            {
                '이름': name,
                'A1': int(responses['A1'] == questions['A1']['answer']),
                'A2': int(responses['A2'] == questions['A2']['answer']),
                'B1': int(responses['B1'] == questions['B1']['answer']),
                'B2': int(responses['B2'] == questions['B2']['answer']),
                'C1': int(responses['C1'] == questions['C1']['answer']),
                'C2': int(responses['C2'] == questions['C2']['answer']),
            }
        ])
        csv = result_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            '결과 CSV 다운로드',
            data=csv,
            file_name='사료_진단_결과.csv',
            mime='text/csv',
        )
