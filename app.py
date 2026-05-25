import streamlit as st
import pandas as pd

try:
    import OpenDartReader
    DartClient = OpenDartReader
except ModuleNotFoundError:
    from opendartreader import OpenDartReader
    DartClient = OpenDartReader

API_KEY = 'c0aacbfba7404217704ef01f2bdce5467a353fce'
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
                    # 매출액, 영업이익 행 찾기
                    revenue_row = fs.loc[(fs['account_nm'] == '매출액') | (fs['account_nm'] == '수익(매출액)')]
                    op_profit_row = fs.loc[fs['account_nm'] == '영업이익']
                    
                    if not revenue_row.empty and not op_profit_row.empty:
                        # 콤마(,) 제거 후 숫자로 안전하게 변환
                        revenue_raw = str(revenue_row['thstrm_amount'].values[0]).replace(',', '')
                        op_profit_raw = str(op_profit_row['thstrm_amount'].values[0]).replace(',', '')
                        
                        revenue = int(revenue_raw) if revenue_raw.replace('-', '').isdigit() else 0
                        op_profit = int(op_profit_raw) if op_profit_raw.replace('-', '').isdigit() else 0
                        
                        st.subheader(f"🏢 {company_name} (2023년 기준)")
                        st.metric(label="매출액", value=f"{revenue:,} 원")
                        st.metric(label="영업이익", value=f"{op_profit:,} 원")
                    else:
                        st.warning("재무제표에서 매출액 또는 영업이익 항목을 찾을 수 없습니다.")
                        
            except Exception as e:
                # 💡 어떤 오류인지 정확히 화면에 빨간 글씨로 출력해 줌
                st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")