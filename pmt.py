import streamlit as st
import psycopg2

conn = psycopg2.connect(
    host="aws-0-eu-north-1.pooler.supabase.com",
    database="postgres",
    user="postgres.yoapzdfznvualrngslfs",  # note the format: user.projectref
    password="DDeras22",
    port=6543
)
cursor = conn.cursor()

params = st.query_params
if params.get("add", "").lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()
