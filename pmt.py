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
import json
from urllib.parse import quote, unquote

st.set_page_config("📊 Polymarket Tracker", layout="centered")

def fetch_market(slug: str):
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, list) and data:
            market = data[0]
            title = market.get("question", "Unknown Title")

            # Parse prices from stringified list
            raw_prices = market.get("outcomePrices", "[]")
            prices = json.loads(raw_prices)

            yes_price = prices[0] if len(prices) > 0 else "N/A"
            no_price = prices[1] if len(prices) > 1 else "N/A"

            return title, str(yes_price), str(no_price)
        return None, None, None
    except Exception as e:
        return None, None, f"Error: {str(e)}"

# ✅ Read query parameters (they come as flat strings)
params = st.query_params
slug = params.get("slug", "us-military-action-against-iran-before-august")
title = params.get("title")
yes_price = params.get("yes")
no_price = params.get("no")

if title and yes_price and no_price:
    st.success("Loaded from URL")
    st.markdown(f"**Market Title:** {unquote(title)}")
    st.markdown(f"**Yes Price:** {yes_price}")
    st.markdown(f"**No Price:** {no_price}")
else:
    with st.spinner("Fetching market data..."):
        title, yes_price, no_price = fetch_market(slug)

    if title and yes_price and no_price:
        # ✅ store only clean, flat values
        st.query_params.update({
            "slug": slug,
            "title": quote(title),
            "yes": yes_price,
            "no": no_price
        })
        st.success("Fetched and updated URL")
        st.markdown(f"**Market Title:** {title}")
        st.markdown(f"**Yes PrFFice:** {yes_price}")
        st.markdown(f"**No Price:** {no_price}")
    else:
        st.error(no_price or "Failed to fetch market data.")

