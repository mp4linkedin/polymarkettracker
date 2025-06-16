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
import re
from urllib.parse import quote, unquote

st.set_page_config("Polymarket Tracker", layout="centered")

def fetch_market_raw(slug: str):
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        text = res.text  # get raw text response

        # Extract title using regex on "question":"..."
        title_match = re.search(r'"question"\s*:\s*"([^"]+)"', text)
        title = title_match.group(1) if title_match else "Unknown Title"

        # Extract outcomePrices string (which looks like ["0.475", "0.525"])
        prices_match = re.search(r'"outcomePrices"\s*:\s*"(\[[^\]]+\])"', text)
        prices_str = prices_match.group(1) if prices_match else "[]"

        # Extract numbers from prices_str (e.g. 0.475 and 0.525)
        prices = re.findall(r'\d+\.\d+', prices_str)
        yes_price = prices[0] if len(prices) > 0 else "N/A"
        no_price = prices[1] if len(prices) > 1 else "N/A"

        return title, yes_price, no_price

    except Exception as e:
        return None, None, f"Error: {str(e)}"

def get_first_param(param):
    if param is None:
        return None
    if isinstance(param, list):
        return param[0]
    return param

params = st.query_params
slug = get_first_param(params.get("slug")) or "us-military-action-against-iran-before-august"
title_param = get_first_param(params.get("title"))
yes_param = get_first_param(params.get("yes"))
no_param = get_first_param(params.get("no"))

if title_param and yes_param and no_param:
    st.success("Loaded from URL")
    st.markdown(f"**Market Title:** {unquote(title_param)}")
    st.markdown(f"**Yes Price:** {yes_param}")
    st.markdown(f"**No Price:** {no_param}")
else:
    with st.spinner("Fetching market data..."):
        title, yes_price, no_price = fetch_market_raw(slug)

    if title and yes_price and no_price:
        st.query_params.update({
            "slug": slug,
            "title": quote(title),
            "yes": yes_price,
            "no": no_price
        })
        st.success("Fetched and updated URL")
        st.markdown(f"**Market Title:** {title}")
        st.markdown(f"**Yes Price:** {yes_price}")
        st.markdown(f"**No Price:** {no_price}")
    else:
        st.error(no_price or "Unable to load market data.")

