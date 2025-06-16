

import streamlit as st
import requests
import json



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
        import psycopg2Add commentMore actions
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
            cursor.execute("""
                INSERT INTO counter (market_title, created_at, market_value, p1)
                VALUES (%s, NOW(), %s, %s);
            """, (unique_title, 1.0, "-"))
            conn.commit()
