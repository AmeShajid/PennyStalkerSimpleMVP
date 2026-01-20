"""
This file contains the strucutre of our SQLite db tables
We store the insider transactions and scan history

This just has SQL create table statements and thats IT
"""

#First table Insider_Transactions table
"""
id - Unique identifier for each transaction (1, 2, 3, ...)
ticker - Stock symbol (e.g., "LSAK", "AAPL")
company_name - Full company name (e.g., "Lesaka Technologies Inc")
filing_date - When insider filed Form 4 with SEC
trade_date - When the actual stock purchase occurred
insider_name - Person who bought stock (e.g., "Mazanderani Ali")
insider_title - Their role (e.g., "CEO", "CFO", "Director")
trade_type - Type of transaction (always "P - Purchase" for our MVP)
price - Price per share in dollars (e.g., 5.00)
quantity - Number of shares purchased (e.g., 1800000)
owned - Total shares owned after this purchase (e.g., 2325115)
delta_own_pct - Percentage change in ownership (e.g., 343.0 means +343%)
value - Total dollar value of purchase (price × quantity)
scan_type - Which scan found this (e.g., "Latest Cluster Buys")
scraped_at - When we added this to database (auto-filled by SQLite)
transaction_hash - Unique ID (e.g., "LSAK_MazanderaniAli_20251231_9000000")

"""
INSIDER_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS insider_transactions (
    -- Primary key (auto-incrementing unique ID for each row)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Stock identification
    ticker TEXT NOT NULL,
    company_name TEXT,
    
    -- Transaction dates (stored as text in ISO format: YYYY-MM-DD HH:MM:SS)
    filing_date TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    
    -- Insider information
    insider_name TEXT,
    insider_title TEXT,
    
    -- Transaction details
    trade_type TEXT,
    price REAL,
    quantity INTEGER,
    owned INTEGER,
    delta_own_pct REAL,
    value REAL,
    
    -- Metadata (tracking information)
    scan_type TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Deduplication (unique hash prevents duplicate entries)
    transaction_hash TEXT UNIQUE
);
"""