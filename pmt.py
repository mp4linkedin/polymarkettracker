import streamlit as st
import psycopg2

conn = psycopg2.connect(
    host="db.yoapzdfznvualrngslfs.supabase.co",  # ✅ Direct connection
    database="postgres",
    user="postgres",
    password="DDeras22",  # 🔒 must be the correct password
    port=5432
)
cursor = conn.cursor()

params = st.query_params
if params.get("add", "").lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()
