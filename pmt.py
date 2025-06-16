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
    cursor.execute("""
        INSERT INTO counter (market_title, created_at, market_value, p1)
        VALUES (%s, NOW(), %s, %s);
    """, (unique_title, 1.0, "-"))
    conn.commit()
