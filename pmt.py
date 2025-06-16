

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





```python
import streamlit as st
import psycopg2
import numpy as np

# This list will hold the formatted difference strings for each market.
diff_messages = []

# Assume 'conn' and 'cursor' for the database connection are already established
# and 'urls' and 'titles' (from the API calls) are available from the preceding code.

# This example uses a placeholder for market titles. In the full script,
# this would be populated dynamically from the API call results.
market_titles = [
    "Will the US conduct military action against Iran before August 1?",
    "Will Ali Khamenei be the Supreme Leader of Iran at the end of 2025?",
    "Will the US and Iran have a public nuclear deal in 2025?",
    "Will the US and Iran have a public nuclear deal before July 1?",
    "Will Ali Khamenei be the Supreme Leader of Iran on June 30, 2025?"
]


for market_title in market_titles:
    try:
        # 1. Select the last 6 rows for the current market to get the current value and baseline values.
        # We order by creation time in descending order to get the newest entries first.
        cursor.execute("""
            SELECT market_value FROM counter
            WHERE market_title = %s
            ORDER BY created_at DESC
            LIMIT 6;
        """, (market_title,))
        
        rows = cursor.fetchall()

        # We need at least 2 data points (1 for current, 1 for baseline) to make a comparison.
        # The pseudo-code implies needing 6 (1 current + 5 for baseline avg).
        if len(rows) < 6:
            # Not enough data to calculate a baseline and difference, so we skip this market.
            # st.write(f"Not enough data for '{market_title}' to calculate trend.")
            continue

        # 2. The first row is the most recent entry (current value).
        # The values are stored as floats (e.g., 0.15), so we multiply by 100 to work with percentages.
        current = float(rows[0][0]) * 100
        
        # 3. The next 5 rows are used to calculate the baseline average.
        baseline_values = [float(row[0]) * 100 for row in rows[1:]]
        baseline = np.mean(baseline_values)

        # 4. Calculate the difference between the current value and the baseline.
        diff = current - baseline

        # 5. Based on the difference, format a string with an appropriate emoji and add it to our list.
        # The thresholds (e.g., 8, 5) represent percentage point changes.
        if diff > 8:
            diff_messages.append(f"🟢 +{diff:.2f}% - {market_title}")
        elif 5 < diff <= 8:
            diff_messages.append(f"🎾 +{diff:.2f}% - {market_title}")
        elif -8 <= diff < -5:
            diff_messages.append(f"🟠 {diff:.2f}% - {market_title}")
        elif diff < -8:
            diff_messages.append(f"🔴 {diff:.2f}% - {market_title}")

    except psycopg2.Error as e:
        st.error(f"Database error for market '{market_title}': {e}")
    except (ValueError, IndexError) as e:
        st.error(f"Data processing error for market '{market_title}': {e}")


# After checking all markets, display the collected trend messages.
if diff_messages:
    st.header("Recent Market Trends")
    for message in diff_messages:
        st.write(message)
else:
    st.info("No significant market trends detected based on the defined thresholds.")

# It's important to close the cursor and connection after all operations are complete.
# This would typically be at the end of the script.
# cursor.close()
# conn.close()
```

