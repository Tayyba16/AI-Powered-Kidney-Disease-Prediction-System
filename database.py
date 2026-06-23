import sqlite3

def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            result TEXT,
            stage TEXT,
            accuracy REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_prediction(p_type, result, stage, accuracy):
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO predictions (type, result, stage, accuracy)
        VALUES (?, ?, ?, ?)
    """, (p_type, result, stage, accuracy))

    conn.commit()
    conn.close()