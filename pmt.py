

import streamlit as st
import requests
import json
from supabase import create_client


# URL of the API endpoint

urls = [
    "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august",
    "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-in-2025",
    "https://gamma-api.polymarket.com/markets?slug=us-x-iran-nuclear-deal-in-2025",
    "https://gamma-api.polymarket.com/markets?slug=us-iran-nuclear-deal-before-july",
    "https://gamma-api.polymarket.com/markets?slug=khamenei-out-as-supreme-leader-of-iran-by-june-30"
]

# urls = [
#     "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"
# ]
    

# for url in urls:
# url = "https://gamma-api.polymarket.com/markets?slug=us-military-action-against-iran-before-august"

for url in urls:
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    
        # Parse the JSON response
        data = response.json()
    
        # Check if the data is a list and not empty
        if isinstance(data, list) and data:
            market_data = data[0]
    
            # Extract the market title and outcomes
            title = market_data.get("question")
            outcomes = json.loads(market_data.get("outcomes", "[]"))
            outcome_prices = json.loads(market_data.get("outcomePrices", "[]"))
    
            # Find the index of the "Yes" outcome
            try:
                yes_index = outcomes.index("Yes")
                yes_price = outcome_prices[yes_index]
            except (ValueError, IndexError):
                yes_price = "Not available"
    
            # Display the information in the Streamlit app
            st.title("Polymarket Market Data")
            st.header(title)
            st.write(f"The current price for 'Yes' is: **{yes_price}**")
    
        else:
            st.error("No market data found in the response.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data from the URL: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Failed to parse the data: {e}")
    
    import streamlit as st
    import psycopg2
    from datetime import datetime
    
    conn = psycopg2.connect(
        host="aws-0-eu-north-1.pooler.supabase.com",
        database="postgres",
        user="postgres.yoapzdfznvualrngslfs",
        password="DDeras22",
        port=6543
    )
    cursor = conn.cursor()
    
    params = st.query_params
    if params.get("add", "").lower() == "true":
        unique_title = "entry_" + datetime.utcnow().isoformat()
        cursor.execute("""INSERT INTO counter (market_title, created_at, market_value, p1) VALUES (%s, NOW(), %s, %s);""", (title, yes_price, "-"))
        conn.commit()







import requests

# Configuration for Supabase REST API
API_URL = "https://aws-0-eu-north-1.pooler.supabase.com/rest/v1/counter"
API_KEY = "YOUR_SUPABASE_ANON_KEY"  # replace with your anon/public key
HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}

market_titles = [
    "us-military-action-against-iran-before-august",
    "khamenei-out-as-supreme-leader-of-iran-in-2025",
    "us-x-iran-nuclear-deal-in-2025",
    "us-iran-nuclear-deal-before-july",
    "khamenei-out-as-supreme-leader-of-iran-by-june-30",
]

diff_notifications = []

for title in market_titles:
    # Fetch the last 6 entries (current + previous 5) for this market, newest first
    resp = requests.get(
        API_URL,
        params={
            "market_title": f"eq.{title}",
            "order": "created_at.desc",
            "limit": 6
        },
        headers=HEADERS
    )
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        continue

    # The first row is the current value
    current = rows[0]["market_value"]

    # The next up to 5 rows are used to compute the baseline
    previous = rows[1:6]
    if previous:
        baseline = sum(r["market_value"] for r in previous) / len(previous)
    else:
        baseline = current

    diff = current - baseline  # in absolute terms (e.g. 0.07 = 7%)
    pct = diff * 100

    # Categorize by thresholds
    if diff > 0.08:
        emoji = "🟢"
    elif 0.05 < diff <= 0.08:
        emoji = "🎾"
    elif -0.08 <= diff < -0.05:
        emoji = "🟠"
    elif diff < -0.08:
        emoji = "🔴"
    else:
        # skip small moves
        continue

    diff_notifications.append(f"{emoji} {pct:+.2f}% – {title}")

# Now you can, for example, display or log these:
for note in diff_notifications:
    print(note)

