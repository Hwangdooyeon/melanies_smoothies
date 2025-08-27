# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"과일 선택해보기")
st.write(
  """wiz - con
  """
)


option = st.selectbox(
    "과일 종류를 선택해주세요",
    ("사과","바나나","복숭아","포도","멜론"),
)

st.write("제일 좋아하는 과일:", option)
    
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)
