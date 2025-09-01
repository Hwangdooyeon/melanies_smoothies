# -*- coding: utf-8 -*-
import streamlit as st
import json
import urllib.request
import pandas as pd

# ✅ 1. 네이버 API 정보
client_id = "q3Yd8CQkM7oHlqOzMeQL"
client_secret = "hGWoNfAcAD"

# ✅ 2. 검색 요청 정보
url = "https://openapi.naver.com/v1/datalab/search"
body = {
    "startDate": "2025-08-01",
    "endDate": "2025-08-31",
    "timeUnit": "date",
    "keywordGroups": [
        {
            "groupName": "나이키운동화",
            "keywords": ["나이키운동화"]
        }
    ],
    "device": "pc",
    "ages": [],
    "gender": ""
}
body_str = json.dumps(body)

# ✅ 3. API 호출 (urllib.request 사용)
req = urllib.request.Request(url)
req.add_header("X-Naver-Client-Id", client_id)
req.add_header("X-Naver-Client-Secret", client_secret)
req.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(req, data=body_str.encode("utf-8"))
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
    else:
        st.error(f"Error Code: {rescode}")
        st.stop()

except Exception as e:
    st.error("API 호출 실패")
    st.text(str(e))
    st.stop()

# ✅ 4. 결과 처리
dates = []
ratios = []

for entry in result['results'][0]['data']:
    dates.append(entry['period'])
    ratios.append(entry['ratio'])

df = pd.DataFrame({'날짜': pd.to_datetime(dates), '검색량 지수': ratios})
df = df.set_index('날짜')

# ✅ 5. Streamlit 시각화
st.title("📊 나이키운동화 - 네이버 검색 트렌드 (2025년 8월)")

st.subheader("🔎 일자별 검색량 지수")
st.dataframe(df, use_container_width=True)

st.subheader("📈 꺾은선 그래프")
st.line_chart(df)
