import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__),
                       '..', 'data', 'market_data.db')


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_listings (
        item_name TEXT PRIMARY KEY,
        current_price REAL NOT NULL,
        supply_volume INTEGER NOT NULL,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        metadata TEXT -- JSON string for qualities, tiers, wear, etc.
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        volume INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_name) REFERENCES market_listings(item_name)
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_item_time ON historical_prices(item_name, timestamp);
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_wallet (
        id INTEGER PRIMARY KEY CHECK (id = 1), -- Forces single row for local sim
        balance REAL NOT NULL DEFAULT 1000.00  -- Starting paper capital
    )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO user_wallet (id, balance) VALUES (1, 1000.00)")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        purchase_price REAL NOT NULL,
        purchase_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'HOLDING', -- 'HOLDING' or 'SOLD'
        sell_price REAL,
        sell_timestamp DATETIME,
        net_profit REAL -- Calculated using the precise Steam tax floor logic
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database successfully initialized at {DB_PATH}")


if __name__ == "__main__":
    init_db()
