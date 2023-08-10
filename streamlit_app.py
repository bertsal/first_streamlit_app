import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruitchoice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruitchoice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display Fruityvice
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    from_fn = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(from_fn)
except URLError as e:
  streamlit.error()

streamlit.header("View our fruit list! Add your favorites!")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

# Add streamlit app > Settings > Secrets:
#[snowflake]
#user = "RWS"
#password = ""
#account = "KZ80468.ca-central-1.aws"
#warehouse = "pc_rivery_wh" 
#database = "pc_rivery_db" 
#schema = "public"
#role = "pc_rivery_role"

# if MODULE_NOT_FOUND error: [ < Manage App ] > [:] > [Reboot App]

# Add a button
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# Allow user to add another fruit
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
      return 'Thanks for adding ', new_fruit

add_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a fruit to the list':
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  from_fn = insert_row_snowflake(add_fruit)
  my_cnx.close()
  streamlit.text(from_fn)

# Halt exec
#streamlit.stop()
