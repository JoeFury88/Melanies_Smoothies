# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app

Name_on_Order = st.text_input('Name on Smoothie','')
st.write('the name on your Smoothie will be:',Name_on_Order)
 

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:', my_dataframe
    , max_selections=5
)



if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, Name_on_Order)
            values ('""" + ingredients_string + """','""" +Name_on_Order+"""')"""
    time_to_insert = st.button('Submit Order')



   # st.write(my_insert_stmt)
    #st.stop
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, '+  Name_on_Order + ' !', icon="✅")
        