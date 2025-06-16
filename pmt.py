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

URL = "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"

# Wait 1 second before request
time.sleep(1)

response = requests.get(URL)
markets = response.json()

market = markets[0]
title = market.get('question', 'No title found')
outcomes = market.get('outcomes', [])
prices = market.get('outcomePrices', [])

if "Yes" in outcomes:
    yes_index = outcomes.index("Yes")
    try:
        yes_price = float(prices[yes_index])
    except (IndexError, ValueError):
        yes_price = None
else:
    yes_price = None

st.title("Market Information")
st.write(f"**Market Title:** {title}")
if yes_price is not None and yes_price > 0:
    st.write(f"**Price of 'Yes':** {yes_price}")
else:
    st.write("Price of 'Yes' not available yet, retry shortly.")


