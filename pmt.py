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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote, unquote
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Polymarket Market Info", layout="centered")
st.title("📊 Polymarket Market Data")

@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_market():
    url = "https://polymarket.com/event/us-military-action-against-iran-before-august?tid=1750074158260"
    driver = get_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        title_elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        price_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='market-outcome-price']")))

        title = title_elem.text.strip()
        price = price_elem.text.strip()

        return title, price

    except Exception as e:
        return None, f"Error: {e}"

    finally:
        driver.quit()

# Read query params
params = st.experimental_get_query_params()
title_param = params.get("title", [None])[0]
price_param = params.get("price", [None])[0]

if title_param and price_param:
    st.success("Loaded from URL")
    st.markdown(f"**Market Title:** {unquote(title_param)}")
    st.markdown(f"**Market Price (Yes):** {price_param}")
else:
    with st.spinner("Fetching market data..."):
        title, price = fetch_market()
    if title:
        st.experimental_set_query_params(title=quote(title), price=price)
        st.success("Fetched and updated URL!")
        st.markdown(f"**Market Title:** {title}")
        st.markdown(f"**Market Price (Yes):** {price}")
    else:
        st.error(price)
