import streamlit as st
import pandas as pd

# 💡 리눅스 환경 대소문자 구분 및 최신 0.3.2 버전 대응을 위한 완벽한 임포트
try:
    # 구버전 또는 윈도우 환경에서의 방식
    import OpenDartReader
    DartClient = OpenDartReader
except ModuleNotFoundError:
    # 최신 버전(0.3.2) 및 Streamlit 리눅스 서버에서의 방식
    from opendartreader import OpenDartReader
    DartClient = OpenDartReader

API_KEY = 'c0aacbfba7404217704ef01f2bdce5467a353fce'
# 에러 없이 안전하게 객체 생성
dart = DartClient(API_KEY)

st.title("📊 DART 재무정보 검색 에이전트")
company_name = st.text_input("회사명 (예: 삼성전자, 카카오)")

if st.button("검색"):
    if company_name:
        with st.spinner('데이터를 불러오는 중...'):
            try:
                # 2023년 사업보고서 기준 재무제표 불러오기
                fs = dart.finstate(company_name, 2023)
                
                if fs is None or fs.empty:
                    st.warning("해당 기업의 데이터를 찾을 수 없거나 아직 공시되지 않았습니다.")
                else:
                    revenue = fs.loc[(fs['account_nm'] == '매출액') | (fs['account_nm'] == '수익(매출액)'), 'thstrm_amount'].values[0]
                    op_profit = fs.loc[fs['account_nm'] == '영업이익', 'thstrm_amount'].values[0]
                    
                    st.subheader(f"🏢 {company_name} (2023년 기준)")
                    st.metric(label="매출액", value=f"{int(revenue):,} 원")
                    st.metric(label="영업이익", value=f"{int(op_profit):,} 원")
            except Exception as e:
                st.error("오류가 발생했습니다.")