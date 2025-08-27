# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
# Write directly to the app
st.write(
  """wiz-con
  """
)


title = st.text_input("Name on Smoothie: ")
name_on_order = title
st.write("Choose the fruits you want in your custom Smoothie", title)

 session = Session.builder.configs(st.secrets["connections.snowflake"]).create()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    'choose up to 5 ingredients:'
    ,my_dataframe
)

if ingredients_List:
    ingredients_string =''

    for fruit_chosen in ingredients_List: 
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
   
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
