
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import random

app = FastAPI(title="Quotes API")

DATABASE = "quotes.db"

class Quote(BaseModel):
    id: int
    quote: str
    author: str

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/quotes", response_model=List[Quote])
def get_quotes(author: Optional[str] = Query(None, description="Filter by author")):
    conn = get_db_connection()
    cursor = conn.cursor()
    if author:
        cursor.execute("SELECT * FROM quotes WHERE lower(author) = lower(?)", (author,))
    else:
        cursor.execute("SELECT * FROM quotes")
    quotes = cursor.fetchall()
    conn.close()
    return [dict(q) for q in quotes]

@app.get("/random", response_model=Quote)
def get_random_quote():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    quotes = cursor.fetchall()
    conn.close()
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    return dict(random.choice(quotes))
