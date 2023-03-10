import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(fruit_choice):
    """Get the data of the fruit choice as a normalized dataframe."""
    fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# Snowflake functions
def snowflake_connection():
    return snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruit_load_list(connection) -> pd.DataFrame:
    with connection.cursor() as my_cur:
        my_cur.execute('Select * from fruit_load_list')
        return my_cur.fetchall()
        
def insert_row_snowflake(connection, new_fruit: str) -> str:
    with connection.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
        return f'Thanks for adding {new_fruit}'
        
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
        fruit_df = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruit_df)
      
except URLError as e:
    streamlit.error()

# Snowflake Connection
# Fruit Load List and button
streamlit.header('View Our Fruit List - Add Your Favorites')

if streamlit.button('Get Fruit List'):
    my_cnx = snowflake_connection()
    my_data_rows = get_fruit_load_list(my_cnx)
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Add fruit to list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake_connection()
    thank_you_string = insert_row_snowflake(my_cnx, add_my_fruit)
    my_cnx.close()
    streamlit.write(thank_you_string)
