import streamlit as st
import sqlite3

# DB setup
conn = sqlite3.connect("example.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS counter (value INTEGER);")
conn.commit()

# Use new query param API
params = st.query_params
if params.get("add", "").lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()
