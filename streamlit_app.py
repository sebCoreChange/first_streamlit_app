import streamlit
import requests
import snowflake.connector
import pandas

from urllib.error import URLError


streamlit.title("My Parents New Healthy Diner") 

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal.')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie.')
streamlit.text(' 🐔 Hard-Boild Free-Range Egg.')
streamlit.text(' 🥑🍞 Advocado Toast.')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Kiwifruit', 'Apple'] )
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)


#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

# Paramter to select fruit info.
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"  +  fruit_choice )

# Parse the reponse to a panadas data frame. 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Show the parsed data frame. 
streamlit.dataframe(fruityvice_normalized)


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")

my_data_rows = my_cur.fetchall()

streamlit.header("The fruit load lost contains:")
streamlit.dataframe(my_data_rows)

#streamlit.text("What fruit would you like to add") 
fruit_add = streamlit.text_input('What fruit would you like to add','Kiwi')
streamlit.text("Thanks for adding: " + fruit_add ) 

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from');")