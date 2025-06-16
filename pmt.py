# import streamlit as st
# import psycopg2
# from datetime import datetime

# conn = psycopg2.connect(
#     host="aws-0-eu-north-1.pooler.supabase.com",
#     database="postgres",
#     user="postgres.yoapzdfznvualrngslfs",
#     password="DDeras22",
#     port=6543
# )
# cursor = conn.cursor()

# params = st.query_params
# if params.get("add", "").lower() == "true":
#     unique_title = "entry_" + datetime.utcnow().isoformat()
#     cursor.execute("""
#         INSERT INTO counter (market_title, created_at, market_value, p1)
#         VALUES (%s, NOW(), %s, %s);
#     """, (unique_title, 1.0, "-"))
#     conn.commit()

import streamlit as st
import requests
import time

time.sleep(1)  # wait 1 second

response = requests.get("https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august")
market = response.json()[0]

title = market['question']
yes_index = market['outcomes'].index("Yes")
yes_price = market['outcomePrices'][yes_index]

st.title("Market Information")
st.write(f"Market Title: {title}")
st.write(f"Price of 'Yes': {yes_price}")



