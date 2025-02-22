import sqlite3

def init_db():
    conn = sqlite3.connect("processed_image.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            metadata TEXT,
            statistics TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_image(filename, metadata, statistics):
    conn = sqlite3.connect("processed_image.db")
    c = conn.cursor()
    c.execute("INSERT INTO images (filename, metadata, statistics) VALUES (?, ?,?) ON CONFLICT(filename) DO UPDATE SET metadata = ?, statistics = ?", (filename, metadata, statistics, metadata, statistics))
    conn.commit()
    conn.close()

def get_image(filename):
    conn = sqlite3.connect("processed_image.db")
    c = conn.cursor()
    c.execute("""SELECT metadata, statistics FROM images WHERE filename = "%s" """% filename)
    row = c.fetchone()
    conn.close()
    if row:
        return {'status': 'Success', 'data': [row[0], row[1]]}
    else:
        return {'status': 'Error'}

