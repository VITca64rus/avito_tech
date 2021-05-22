import sqlite3
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS keys(
               id integer primary key autoincrement,
               key integer,
               count integer,
               timestamp integer,
               search_fraze TEXT,
               region integer);
            """)
conn.commit()
