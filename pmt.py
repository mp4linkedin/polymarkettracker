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

market = markets[0]

st.write("Full outcomes data:", market.get('outcomes'))

# If outcomes is a list of dicts, try:
if isinstance(market.get('outcomes'), list) and isinstance(market['outcomes'][0], dict):
    for outcome in market['outcomes']:
        st.write(outcome)
        if outcome.get('name') == 'Yes':
            st.write("Yes price:", outcome.get('price'))
else:
    # fallback to old approach
    outcomes = market.get('outcomes', [])
    prices = market.get('outcomePrices', [])
    if "Yes" in outcomes:
        yes_index = outcomes.index("Yes")
        yes_price = prices[yes_index]
        st.write("Yes price:", yes_price)

