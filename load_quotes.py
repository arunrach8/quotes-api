
import sqlite3
import pandas as pd

# Load quotes from CSV
df = pd.read_csv("quotes_dataset.csv")

# Connect to SQLite and create table
conn = sqlite3.connect("quotes.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    author TEXT NOT NULL
)
""")

# Clear existing data
cursor.execute("DELETE FROM quotes")

# Insert quotes
for _, row in df.iterrows():
    cursor.execute("INSERT INTO quotes (quote, author) VALUES (?, ?)", (row['quote'], row['author']))

conn.commit()
conn.close()
print("Quotes loaded into SQLite database.")
