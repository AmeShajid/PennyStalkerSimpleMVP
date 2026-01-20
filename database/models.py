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


#Second tabel Scan History
"""
id - Unique identifier for each scan (1, 2, 3, ...)
scan_type - What was scanned (e.g., "Latest Cluster Buys", "Top Officer Purchases Today")
scan_timestamp - When we ran this scan (auto-filled)
num_transactions - Total transactions found on OpenInsider
num_new - How many were NEW (not already in database)
num_duplicates - How many were already in database (skipped)
highest_value - Largest transaction value found in this scan
"""
SCAN_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS scan_history (
    -- Primary key (auto-incrementing unique ID for each scan)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- What type of scan was performed
    scan_type TEXT NOT NULL,
    
    -- When the scan occurred (auto-filled by SQLite)
    scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Statistics about the scan
    num_transactions INTEGER,
    num_new INTEGER,
    num_duplicates INTEGER,
    highest_value REAL
);
"""

#Creating INDEXES(this make sql queries alot faster)
"""
Without indexes: Database must scan EVERY row to find matches (slow)
With indexes: Database can jump directly to relevant rows (fast)

Example without index:
  Query: "Find all LSAK transactions"
  Database checks: Row 1? No. Row 2? No. Row 3? No... (checks all 10,000 rows)
  Time: Slow (seconds)

Example with index on ticker:
  Query: "Find all LSAK transactions"
  Database looks up LSAK in index, jumps directly to those rows
  Time: Fast (milliseconds)
"""

# Index on ticker column (makes searching by ticker fast)
CREATE_TICKER_INDEX = """
CREATE INDEX IF NOT EXISTS idx_ticker 
ON insider_transactions(ticker);
"""

# Index on trade_date column (makes date range queries fast)
CREATE_TRADE_DATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_trade_date 
ON insider_transactions(trade_date);
"""

# Index on value column (makes "top purchases" queries fast)
CREATE_VALUE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_value 
ON insider_transactions(value DESC);
"""

#Creating all the schemas
#List containing all CREATE statements in order
#This will be used by db.py to initialize the database
ALL_SCHEMAS = [
    INSIDER_TRANSACTIONS_TABLE,
    SCAN_HISTORY_TABLE,
    CREATE_TICKER_INDEX,
    CREATE_TRADE_DATE_INDEX,
    CREATE_VALUE_INDEX
]