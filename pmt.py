import streamlit as st
import sqlite3
from urllib.parse import urlparse, parse_qs

# Connect to SQLite (use external DB for production)
conn = sqlite3.connect("example.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS counter (value INTEGER);")
conn.commit()

# Parse URL parameters
params = parse_qs(urlparse(st.experimental_get_query_params()).get("add", [""])[0])

# Insert row if ?add=true
if "add" in st.experimental_get_query_params() and st.experimental_get_query_params()["add"][0].lower() == "true":
    cursor.execute("INSERT INTO counter (value) VALUES (1);")
    conn.commit()
