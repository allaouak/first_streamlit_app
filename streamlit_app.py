import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = st.text_input('What fruit would you like information about?')
   if not fruit_choice:
        st.error("Please select a fruit to get information.")
   else:
       back_from_function=get_fruityvice_data(fruit_choice)
       st.dataframe(back_from_function)
except URLError as e:
     st.error()

#st.stop()

st.header("View Our Fruit List - Add Your Favorites!")
#Snowflake-related functions
def get_fruit_load_list():
       with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from fruit_load_list")
            return my_cur.fetchall()
       
# Add a button to load the fruit
if st.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   st.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def inert_row_snowflake(new_fruit):
       with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')") 
            return "Thanks for adding "+new_fruit
s_fruit_choice = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   back_from_function=inert_row_snowflake(s_fruit_choice)
   st.text(back_from_function)
   my_cnx.close()


