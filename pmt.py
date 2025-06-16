import streamlit as st
import psycopg2
import urllib.parse

# Decode URL password if needed
password = urllib.parse.quote("YOUR_PASSWORD")  # e.g., if it has @ or special chars

conn = psycopg2.connect(
    host="db.yoapzdfznvualrngslfs.supabase.co",
    database="postgres",
    user="postgres",
    password="DDeras22",  # or use decoded `password` if special characters
    port=5432
)
cursor = conn.cursor()

# Add row if ?add=true
params = st.query_params
if params.get("add", "").lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()
