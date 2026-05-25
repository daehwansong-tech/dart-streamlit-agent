import streamlit as st
import OpenDartReader
import pandas as pd

API_KEY = 'c0aacbfba7404217704ef01f2bdce5467a353fce'
dart = OpenDartReader(API_KEY)

st.title("📊 DART 재무정보 검색 에이전트")
company_name = st.text_input("회사명 (예: 삼성전자, 카카오)")

if st.button("검색"):
    if company_name:
        with st.spinner('데이터를 불러오는 중...'):
            try:
                fs = dart.finstate(company_name, 2023)
                if fs is None or fs.empty:
                    st.warning("데이터를 찾을 수 없습니다.")
                else:
                    revenue = fs.loc[(fs['account_nm'] == '매출액') | (fs['account_nm'] == '수익(매출액)'), 'thstrm_amount'].values[0]
                    op_profit = fs.loc[fs['account_nm'] == '영업이익', 'thstrm_amount'].values[0]
                    
                    st.subheader(f"🏢 {company_name} (2023년 기준)")
                    st.metric(label="매출액", value=f"{int(revenue):,} 원")
                    st.metric(label="영업이익", value=f"{int(op_profit):,} 원")
            except Exception as e:
                st.error("오류가 발생했습니다.")