import streamlit as st
import sqlite3

# DB setup
conn = sqlite3.connect("example.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS counter (value INTEGER);")
conn.commit()

# Insert if ?add=true
params = st.query_params
if params.get("add", "").lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()

# Show current count
count = cursor.execute("SELECT COUNT(*) FROM counter").fetchone()[0]
st.write("Total rows:", count)
