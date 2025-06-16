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
from urllib.parse import quote, unquote

st.set_page_config("📊 Polymarket Tracker", layout="centered")

def fetch_market_data(slug):
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if data:
            market = data[0]
            title = market.get("title", "")
            outcomes = market.get("outcomes", [])
            yes_price = next((o["price"] for o in outcomes if o["name"].lower() == "yes"), "N/A")
            return title, yes_price
        return None, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# Read from URL query
params = st.experimental_get_query_params()
slug = params.get("slug", ["us-military-action-against-iran-before-august"])[0]
title = params.get("title", [None])[0]
price = params.get("price", [None])[0]

if title and price:
    st.success("Loaded from URL")
    st.markdown(f"**Market Title:** {unquote(title)}")
    st.markdown(f"**Price (Yes):** {price}")
else:
    with st.spinner("Fetching market info..."):
        title, price = fetch_market_data(slug)

    if title and price:
        st.experimental_set_query_params(slug=slug, title=quote(title), price=price)
        st.success("Data fetched and URL updated")
        st.markdown(f"**Market Title:** {title}")
        st.markdown(f"**Price (Yes):** {price}")
    else:
        st.error(price or "Unable to load market data.")
