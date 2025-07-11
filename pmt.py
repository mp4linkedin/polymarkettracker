

# import streamlit as st
# import requests
# import json



# # URL of the API endpoint

# urls = [
#     "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august",
#     "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-in-2025",
#     "https://gamma-api.polymarket.com/markets?slug=us-x-iran-nuclear-deal-in-2025",
#     "https://gamma-api.polymarket.com/markets?slug=us-iran-nuclear-deal-before-july",
#     "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-by-june-30"
# ]

# # urls = [
# #     "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"
# # ]
    

# # for url in urls:
# # url = "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"

# for url in urls:
    
#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for bad status codes
    
#         # Parse the JSON response
#         data = response.json()
    
#         # Check if the data is a list and not empty
#         if isinstance(data, list) and data:
#             market_data = data[0]
    
#             # Extract the market title and outcomes
#             title = market_data.get("question")
#             outcomes = json.loads(market_data.get("outcomes", "[]"))
#             outcome_prices = json.loads(market_data.get("outcomePrices", "[]"))
    
#             # Find the index of the "Yes" outcome
#             try:
#                 yes_index = outcomes.index("Yes")
#                 yes_price = outcome_prices[yes_index]
#             except (ValueError, IndexError):
#                 yes_price = "Not available"
    
#             # Display the information in the Streamlit app
#             st.title("Polymarket Market Data")
#             st.header(title)
#             st.write(f"The current price for 'Yes' is: **{yes_price}**")
    
#         else:
#             st.error("No market data found in the response.")
    
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to retrieve data from the URL: {e}")
#     except (json.JSONDecodeError, KeyError) as e:
#         st.error(f"Failed to parse the data: {e}")
    
  

#     import streamlit as st
#     import psycopg2
#     from datetime import datetime
    
#     conn = psycopg2.connect(
#         host="aws-0-eu-north-1.pooler.supabase.com",
#         database="postgres",
#         user="postgres.yoapzdfznvualrngslfs",
#         password="DDeras22",
#         port=6543
#     )
#     cursor = conn.cursor()
    
#     params = st.query_params
#     if params.get("add", "").lower() == "true":
#         unique_title = "entry_" + datetime.utcnow().isoformat()
#         cursor.execute("""
#             INSERT INTO counter (market_title, created_at, market_value, p1)
#             VALUES (%s, NOW(), %s, %s);
#         """, (unique_title, 1.0, "-"))
#         conn.commit()




import time
import streamlit as st
import requests
import json
import psycopg2
from datetime import datetime

# API URLs
urls = [
    "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august",
    "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-in-2025",
    "https://gamma-api.polymarket.com/markets?slug=us-x-iran-nuclear-deal-in-2025",
    "https://gamma-api.polymarket.com/markets?slug=us-iran-nuclear-deal-before-july",
    "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-by-june-30",
    "https://gamma-api.polymarket.com/markets?slug=israel-x-iran-ceasefire-before-july"
]

# PostgreSQL connection (Supabase)
conn = psycopg2.connect(
    host="aws-0-eu-north-1.pooler.supabase.com",
    database="postgres",
    user="postgres.yoapzdfznvualrngslfs",
    password="DDeras22",
    port=6543
)
cursor = conn.cursor()

# Placeholder: define the function you mentioned
import requests


def hadd_diff(message: str):
    url = "https://api.telegram.org/bot7194674196:AAHIs0vU-wbm8j_cleL68hALarIRqSp6DXs/sendMessage"

    payload = {
        "chat_id": "100010019",
        "text": message
    }
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    _ = response.text
    time.sleep(1)

    payload = {
        "chat_id": "289053770",
        "text": message
    }
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    _ = response.text
    time.sleep(1)

    payload = {
        "chat_id": "1827419176",
        "text": message
    }
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    _ = response.text
    time.sleep(1)
    
st.title("Polymarket Market Data")

def convert_gamma_to_polymarket_url(gamma_url: str) -> str:
    slug = gamma_url.split("slug=")[-1]
    return f"https://polymarket.com/event/{slug}"




for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            market_data = data[0]
            title = market_data.get("question")
            outcomes = json.loads(market_data.get("outcomes", "[]"))
            outcome_prices = json.loads(market_data.get("outcomePrices", "[]"))

            try:
                yes_index = outcomes.index("Yes")
                yes_price = outcome_prices[yes_index]
            except (ValueError, IndexError):
                yes_price = None

            st.header(title)
            if yes_price is not None:
                st.write(f"The current price for 'Yes' is: **{yes_price}**")

                # Optional insert
                params = st.query_params
                if params.get("add", "").lower() == "true":
                    cursor.execute("""
                        INSERT INTO counter (market_title, created_at, market_value, p1)
                        VALUES (%s, NOW(), %s, %s);
                    """, (title, yes_price, "-"))
                    conn.commit()

                # Trend detection
                cursor.execute("""
                    SELECT market_value FROM counter
                    WHERE market_title = %s
                    ORDER BY created_at DESC
                    LIMIT 6
                """, (title,))
                rows = cursor.fetchall()

                if len(rows) >= 6:
                    values = [r[0] for r in rows]
                    current = values[0]
                    baseline = sum(values[1:]) / 5
                    diff = current - baseline

                    # add_diff(f"{title}: current: {current}, baseline [{values[1:]}], {baseline}]")
                    # add_diff(convert_gamma_to_polymarket_url(url))

                    if diff > 0.035:
                        add_diff(f"Last 5 minutes 🔴⏫ +{diff * 100:.2f}% - {title}")
                    elif 0.025 < diff <= 0.035:
                        add_diff(f"Last 5 minutes 🟡🔼 +{diff * 100:.2f}% - {title}")
                    elif -0.035 <= diff < -0.025:
                        add_diff(f"Last 5 minutes 🟡🔽 {diff * 100:.2f}% - {title}")
                    elif diff < -0.035:
                        add_diff(f"Last 5 minutes 🔴⏬ {diff * 100:.2f}% - {title}")
                    
            else:
                st.warning("No valid 'Yes' outcome price found.")
        else:
            st.error("No market data found in the response.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Failed to parse data: {e}")

cursor.close()
conn.close()


