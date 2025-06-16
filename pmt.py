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

URL = "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"

response = requests.get(URL)
markets = response.json()

market = markets[0]  # assuming the first market in list
title = market['question']
outcomes = market['outcomes']
prices = market['outcomePrices']

yes_index = outcomes.index("Yes")
yes_price = prices[yes_index]

st.title("Market Information")
st.write(f"**Market Title:** {title}")
st.write(f"**Price of 'Yes':** {yes_price}")

