import sqlite3

def init_db():
    conn = sqlite3.connect("metadata.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            metadata TEXT,
            pca_result TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_image_with_metadata(filename, metadata):
    conn = sqlite3.connect("metadata.db")
    c = conn.cursor()
    c.execute("INSERT INTO images (file_path, metadata) VALUES (?, ?) ", (filename, metadata))
    conn.commit()
    conn.close()

def update_image_with_pca_result(filename, pca_result):
    conn = sqlite3.connect("metadata.db")
    c = conn.cursor()
    c.execute("UPDATE images SET pca_result = ? WHERE filename = ?) ", (filename, pca_result))
    conn.commit()
    conn.close()

def get_image(filename):
    conn = sqlite3.connect("metadata.db")
    c = conn.cursor()
    c.execute("SELECT metadata, pca_result FROM images WHERE filename = ?) ", (filename,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'status': 'Success', 'data': [row[0], row[1]]}
    else:
        return {'status': 'Error'}
