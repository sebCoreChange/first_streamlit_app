import streamlit
import requests
# import snowflake.connector
import pandas
import duckdb


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

## Create function block to get reusable logic
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"  +  this_fruit_choice )
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try: 
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else: 
        back_from_function= get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        streamlit.write('The user entered ', fruit_choice)

except URLERROR as e:
    streamlit.error()


streamlit.header("The fruit load lost contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select fruit_name, count(*) as row_count from fruit_load_list group by 1 ")
        return my_cur.fetchall()

# if streamlit.button('Get Know cold fruits'):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#     my_data_rows = get_fruit_load_list()
#     streamlit.dataframe(my_data_rows)

    

# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

# def insert_row_snowflake(new_fruit):
#     with my_cnx.cursor() as my_cur:
#         my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+ new_fruit +"');")
#         return "thanks for adding " + new_fruit

# streamlit.text("What fruit would you like to add") 
# try: 
#     fruit_add = streamlit.text_input('Anything missing from the list?')
#     if not fruit_add:
#         streamlit.error("Specifie a fruit to add.")
#     else:
#         if streamlit.button('Add new fruit to snowflake.'):
#             my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#             back_from_function = insert_row_snowflake(fruit_add)
#             streamlit.text(back_from_function)
#         streamlit.text("inner text")
# except URLERROR as e:
#     streamlit.error()


streamlit.stop()
mother_duck_toekn = streamlit.secrets.MotherDuck.MotherDuckKey 

con = duckdb.connect('md:?motherduck_token=' + )

# Query for filtered data
query = """
SELECT * From StreamLitFruitInfo
"""
df = con.execute(query).df()




#fruit_add = streamlit.text_input('What fruit would you like to add','Kiwi')
#streamlit.text("Thanks for adding: " + fruit_add ) 