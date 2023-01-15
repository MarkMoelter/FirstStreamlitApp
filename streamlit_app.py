import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# Create website
# New Section
streamlit.title('My Parent\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# New Section
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load fruit from csv file
text_file = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt'
my_fruit_list = pd.read_csv(text_file)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Fruit multiselect
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]                    
streamlit.dataframe(fruits_to_show)

# New Section
# Display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

# Handle Errors
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:
        fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
        fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
      
except URLError as e:
    streamlit.error()

streamlit.stop()

# Snowflake Connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
