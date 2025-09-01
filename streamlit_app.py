import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# 네이버 API 인증 정보
CLIENT_ID = "q3Yd8CQkM7oHlqOzMeQL"
CLIENT_SECRET = "hGWoNfAcAD"

# 검색어 트렌드 요청 함수
def get_trend_data(keyword, start_date, end_date, time_unit="date"):
    url = "https://openapi.naver.com/v1/datalab/search"

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",  # "date" = daily
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ],
        "device": "pc",  # 또는 "all"
        "ages": [],
        "gender": ""
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API 호출 실패: {response.status_code}")
        st.text(response.text)
        return None

# 날짜 변환
def format_trend_response(result):
    dates = []
    ratios = []

    for entry in result['results'][0]['data']:
        dates.append(entry['period'])
        ratios.append(entry['ratio'])

    df = pd.DataFrame({'날짜': dates, '검색량 지수': ratios})
    return df

# Streamlit 시작
st.title("📊 네이버 검색어 트렌드")

# 기본 검색어 및 날짜
keyword = "나이키운동화"
start_date = "2025-08-01"
end_date = "2025-08-31"

st.write(f"🔍 검색어: `{keyword}` (기간: {start_date} ~ {end_date})")

# API 호출
trend_data = get_trend_data(keyword, start_date, end_date)

if trend_data:
    df = format_trend_response(trend_data)
    st.dataframe(df, use_container_width=True)
