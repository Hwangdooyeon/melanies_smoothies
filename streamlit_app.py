# streamlit_app.py

import streamlit as st

conn = st.connection("snowflake")  # 🔐 secrets.toml에서 자동 연결

@st.cache_data
def load_table():
    session = conn.session()  # ✅ Snowpark 세션 생성
    return session.table("smoothies.public.fruit_options").to_pandas()

df = load_table()

st.dataframe(df)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', df['FRUIT_NAME']
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    name = st.text_input("Name on Smoothie:")
    if st.button("Submit Order"):
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name}')
        """
        conn.session().sql(insert_stmt).collect()
        st.success("✅ Smoothie ordered!")

