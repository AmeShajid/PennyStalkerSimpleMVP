# PennyStalker MVP

**Insider Trading Activity Scanner**

A Python-based terminal application that tracks insider stock purchases by scraping OpenInsider.com, storing historical data, and displaying only new transactions ranked by value.

---

## 📋 Table of Contents

- [What Is This?](#what-is-this)
- [Why Build This?](#why-build-this)
- [How It Works](#how-it-works)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Technical Decisions](#technical-decisions)
- [Future Features](#future-features)
- [Disclaimer](#disclaimer)

---

## 🎯 What Is This?

PennyStalker MVP is a **research automation tool** that monitors insider trading activity. When company executives, directors, and major shareholders buy stock in their own companies, it's publicly reported. This tool:

1. **Scrapes** insider purchase data from OpenInsider.com
2. **Filters** to show only purchases (not sales)
3. **Deduplicates** to avoid showing the same transaction twice
4. **Ranks** transactions by dollar value
5. **Stores** everything in a local SQLite database for historical analysis

### What It Is NOT

- ❌ Not a trading bot or automation system
- ❌ Not providing buy/sell recommendations
- ❌ Not predicting stock prices
- ❌ Not financial advice

### What It IS

- ✅ A data collection and organization tool
- ✅ A time-saving research assistant
- ✅ A way to track insider activity patterns
- ✅ For educational and research purposes only

---

## 💡 Why Build This?

### The Problem

**Manual insider trading research is tedious:**

1. Open OpenInsider.com multiple times per day
2. Scan through tables manually
3. Copy interesting transactions to notepad
4. Forget what you already looked at yesterday
5. See the same transactions repeatedly
6. No easy way to search historical data

**Time spent:** 15-20 minutes per day, every day

### The Solution

**PennyStalker automates this workflow:**

1. Run one command
2. Pick what you want to see
3. Get ranked results in 10 seconds
4. Never see duplicates
5. Search historical data anytime

**Time spent:** 10 seconds

### Why Insider Buying Matters

When a CEO buys $5 million of their own company's stock:
- They're putting their own money at risk
- They likely know something positive is coming
- It's a stronger signal than any analyst report
- Following insider buying = following smart money

**Note:** Insider buying doesn't guarantee success, but it's a valuable data point for research.

---

## 🔧 How It Works

### User Workflow

```
1. User runs: python main.py
        ↓
2. Program displays menu of scan options
        ↓
3. User selects option (e.g., "Latest Cluster Buys")
        ↓
4. Program scrapes OpenInsider.com
        ↓
5. Program checks each transaction against database
        ↓
6. Only NEW transactions are saved and displayed
        ↓
7. Results shown ranked by dollar value
        ↓
8. User sees clean, organized output
```

### Behind The Scenes

```
OpenInsider.com
      ↓
   [Scraper] ← Fetches HTML, parses table
      ↓
   [Hash Generator] ← Creates unique ID per transaction
      ↓
   [Database] ← Checks: "Have we seen this before?"
      ↓
   [Repository] ← If NEW: store it
      ↓
   [Display] ← Format and show to user
```

---

## 🏗️ Project Architecture

### File Structure

```
PENNYSTALKERSIMPLEMVP/
│
├── scrapers/                    # Data collection
│   ├── __init__.py
│   ├── base.py                 # HTTP handling (shared)
│   └── openinsider.py          # OpenInsider scraping logic
│
├── database/                    # Data storage
│   ├── __init__.py
│   ├── db.py                   # SQLite connection management
│   ├── models.py               # Table schemas (SQL)
│   └── repository.py           # Database queries (CRUD)
│
├── utils/                       # Helper functions
│   ├── __init__.py
│   ├── display.py              # Terminal UI and formatting
│   └── hash_utils.py           # Generate transaction IDs
│
├── data/                        # Runtime data
│   └── pennystalker.db         # SQLite database (auto-created)
│
├── venv/                        # Virtual environment
│
├── main.py                      # Entry point (orchestrator)
├── .env                         # Environment variables
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Component Responsibilities

| Component | Responsibility | Why It Exists |
|-----------|---------------|---------------|
| **main.py** | Orchestrates entire workflow | Central control, ties everything together |
| **scrapers/base.py** | HTTP handling, rate limiting, error handling | Shared functionality for all scrapers |
| **scrapers/openinsider.py** | Scrape OpenInsider tables | Data acquisition from source |
| **database/db.py** | SQLite connection lifecycle | Centralized database access |
| **database/models.py** | SQL table definitions | Self-documenting schema |
| **database/repository.py** | Database queries | Separates SQL from business logic |
| **utils/display.py** | Terminal formatting | Clean, readable output |
| **utils/hash_utils.py** | Generate unique IDs | Deduplication logic |

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd PENNYSTALKERSIMPLEMVP
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser
- `python-dotenv` - Environment variables
- `python-dateutil` - Date handling

### Step 4: Verify Setup

```bash
python main.py
```

You should see the menu appear.

---

## 📖 Usage Guide

### Basic Usage

```bash
# Activate virtual environment (if not already active)
venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate   # Mac/Linux

# Run program
python main.py
```

### Menu Options

When you run the program, you'll see:

```
═══════════════════════════════════════════════════════
        PennyStalker - Insider Trading Scanner
═══════════════════════════════════════════════════════

What would you like to scan?

LATEST (Real-time feeds):
  a) Latest Cluster Buys
  b) Latest Penny Stock Buys
  c) Latest Insider Trading (all filings)
  d) Latest Insider Purchases
  e) Latest Insider Purchases $25k+
  f) Latest Officer Purchases $25k+
  g) Latest CEO/CFO Purchases $25k+

TOP (Aggregated rankings):
  h) Top Officer Purchases Today
  i) Top Officer Purchases Past Week
  j) Top Officer Purchases Past Month
  k) Top Insider Purchases Today
  l) Top Insider Purchases Past Week
  m) Top Insider Purchases Past Month

Enter your choice (a-m): _
```

### Understanding The Options

**LATEST feeds** show transactions in chronological order (most recent first):
- **Cluster Buys** - Multiple insiders buying the same stock (strong signal)
- **Penny Stock Buys** - Insider purchases of stocks under $5
- **Purchases $25k+** - Significant purchases only (filters out small symbolic buys)
- **CEO/CFO Purchases** - C-suite purchases only (highest conviction)

**TOP rankings** show largest purchases by dollar value:
- **Today** - Highest value purchases filed today
- **Past Week** - Biggest purchases from last 7 days
- **Past Month** - Largest purchases from last 30 days

### Example Output

```
═══════════════════════════════════════════════════════
Scanning: Latest Cluster Buys
Timeframe: Last 2 weeks
═══════════════════════════════════════════════════════

Processing 45 transactions...
Found 12 NEW purchases (33 already in database)

═══════════════════════════════════════════════════════
#1: LSAK - Lesaka Technologies Inc
═══════════════════════════════════════════════════════

INSIDER TRANSACTION:
  Insider:         Mazanderani Ali
  Title:           Exec COB
  Filing Date:     2026-01-02 16:05:32
  Trade Date:      2025-12-31

TRANSACTION DETAILS:
  Price:           $5.00
  Quantity:        +1,800,000 shares
  Total Value:     $9,000,000 ⭐
  Now Owns:        2,325,115 shares
  Change:          +343% 🚀

═══════════════════════════════════════════════════════

... (more transactions)

═══════════════════════════════════════════════════════
SCAN COMPLETE
═══════════════════════════════════════════════════════

Summary:
  • Total scraped:      45 transactions
  • New transactions:   12
  • Already in DB:      33
  • Highest value:      $9,000,000 (LSAK)

Results saved to database: data/pennystalker.db
```

### Understanding The Output

**Key Fields Explained:**

- **Filing Date** - When the insider reported the transaction to SEC
- **Trade Date** - When the actual purchase occurred
- **Insider + Title** - Who bought and their role (CEO, CFO, Director, etc.)
- **Price** - Price per share
- **Quantity** - Number of shares purchased
- **Total Value** - Dollar amount (Quantity × Price)
- **Now Owns** - Total shares owned after purchase
- **Change (ΔOwn)** - Percentage increase in ownership

**Signals to Watch:**

- 🚀 **Large ΔOwn% (50%+)** - Insider significantly increased their position
- ⭐ **High dollar value ($1M+)** - Serious money at risk
- 👥 **Cluster buys** - Multiple insiders buying = strong conviction
- 💼 **CEO/CFO purchases** - Top executives have best information

---

## 🔄 Data Flow

### Complete Pipeline (Technical)

```
┌─────────────────────────────────────────────────────────────┐
│ USER                                                        │
│ python main.py                                              │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ main.py (PennyStalkerApp)                                   │
│ • Initialize components (scraper, database, display)       │
│ • Show menu                                                 │
│ • Get user choice                                           │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ scrapers/openinsider.py                                     │
│ • Build URL from user choice                                │
│ • Make HTTP request (with rate limiting)                    │
│ • Parse HTML table with BeautifulSoup                       │
│ • Extract transaction data                                  │
│ • Return list of transactions                               │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ main.py (Process Transactions)                              │
│ For each transaction:                                       │
│   1. Generate hash (utils/hash_utils.py)                   │
│   2. Check if exists (database/repository.py)              │
│   3. If NEW: store + mark for display                      │
│   4. If EXISTS: skip                                        │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ database/repository.py                                      │
│ • Insert new transactions                                   │
│ • Record scan metadata                                      │
│ • Commit to SQLite                                          │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ main.py (Display Results)                                   │
│ • Sort by value (descending)                                │
│ • Format with utils/display.py                             │
│ • Print to terminal                                         │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ TERMINAL OUTPUT                                             │
│ Ranked list of NEW insider purchases                        │
└─────────────────────────────────────────────────────────────┘
```

### Deduplication Strategy

**Problem:** OpenInsider pages show transactions for 2+ weeks. Running the program twice in one day would show the same transactions again.

**Solution:** Transaction hashing

```
Transaction Data:
  Ticker: LSAK
  Insider: Mazanderani Ali
  Trade Date: 2025-12-31
  Value: 9000000

      ↓ (hash_utils.py)

Transaction Hash:
  "LSAK_MazanderaniAli_20251231_9000000"

      ↓ (check database)

If hash exists in database:
  → Skip (already processed)

If hash NOT in database:
  → NEW transaction
  → Store in database
  → Display to user
```

This ensures you never see the same transaction twice.

---

## 🗄️ Database Schema

### Table: `insider_transactions`

Stores every insider purchase scraped.

**Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `ticker` | TEXT | Stock symbol (e.g., "LSAK") |
| `company_name` | TEXT | Full company name |
| `filing_date` | TEXT | When filed with SEC (ISO format) |
| `trade_date` | TEXT | When trade occurred (ISO format) |
| `insider_name` | TEXT | Person who bought |
| `insider_title` | TEXT | Their role (CEO, CFO, Director, etc.) |
| `trade_type` | TEXT | Always "P - Purchase" |
| `price` | REAL | Price per share |
| `quantity` | INTEGER | Number of shares |
| `owned` | INTEGER | Total shares owned after |
| `delta_own_pct` | REAL | Percentage change in ownership |
| `value` | REAL | Total dollar value |
| `scan_type` | TEXT | Which scan found this |
| `scraped_at` | TIMESTAMP | When we scraped it |
| `transaction_hash` | TEXT | Unique ID (UNIQUE constraint) |

**Indexes:**
- `ticker` (for fast ticker searches)
- `trade_date` (for date range queries)
- `value` (for top purchases queries)

### Table: `scan_history`

Tracks metadata about each scan run.

**Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `scan_type` | TEXT | What was scanned |
| `scan_timestamp` | TIMESTAMP | When scan occurred |
| `num_transactions` | INTEGER | Total transactions scraped |
| `num_new` | INTEGER | How many were NEW |
| `num_duplicates` | INTEGER | How many were already in DB |
| `highest_value` | REAL | Largest transaction value |

**Purpose:** Track usage patterns, performance metrics, historical context.

---

## 🤔 Technical Decisions

### Why Python?

- Fast development
- Excellent libraries for web scraping (BeautifulSoup, requests)
- Built-in SQLite support
- Easy to read and maintain

### Why SQLite?

- Zero configuration (no database server to set up)
- Single file (easy backup: just copy `pennystalker.db`)
- Fast for our use case (simple reads/writes)
- Embedded (no network latency)
- Upgradeable (can migrate to PostgreSQL later if needed)

**When to upgrade:** If you need concurrent writes or web application deployment.

### Why Class-Based Architecture?

**Benefits:**
- **Encapsulation** - Each class has clear responsibility
- **State management** - Database connection, HTTP session
- **Testability** - Can mock components
- **Scalability** - Easy to add new features
- **Inheritance** - Scrapers share base functionality

**Example:** All scrapers inherit from `BaseScraper` to get HTTP handling, rate limiting, and error handling without duplicating code.

### Why Separate Files?

**Single Responsibility Principle:**
- `scraper.py` only scrapes
- `db.py` only manages database connection
- `repository.py` only executes queries
- `display.py` only formats output

**Benefit:** Change one part without breaking others. Add features without touching existing code.

### Why Repository Pattern?

Separates SQL from business logic:
- All SQL queries in `repository.py`
- Rest of app doesn't know it's SQLite
- Can swap to Postgres without changing interface
- Industry standard pattern

### Why Terminal UI (Not Web)?

**MVP Philosophy:**
- Fastest to build
- No server setup
- No security concerns
- Focus on core functionality first

**V2+ Plan:** Build web interface once terminal version proves useful.

---

## 🚧 Future Features (Not In MVP)

### Planned for V2:

- [ ] **StockTitan Integration** - Add company news and financials
- [ ] **Scoring System** - Rank by conviction (ΔOwn%, value, role)
- [ ] **Filtering** - Minimum value, minimum ΔOwn%, specific insiders
- [ ] **Search Command** - `python main.py --search LSAK`
- [ ] **Export** - Save results as CSV/JSON
- [ ] **Alerts** - Email/SMS when high-value purchases detected
- [ ] **Charts** - Visualize insider activity over time
- [ ] **Web Interface** - Browser-based UI

### Ideas for V3+:

- [ ] Track insider sales (bearish signals)
- [ ] Pattern detection (serial buyers, clusters)
- [ ] Correlation with price movements
- [ ] Multi-source aggregation (SEC, Yahoo Finance, etc.)
- [ ] API for external integrations

---

## ⚠️ Disclaimer

### Important Legal Notice

**This software is for educational and research purposes only.**

- ❌ **NOT financial advice**
- ❌ **NOT investment recommendations**
- ❌ **NOT trading signals**

**You are solely responsible for your own investment decisions.**

### Risk Warning

- Insider buying does NOT guarantee stock price increases
- Past insider activity does NOT predict future results
- Markets are unpredictable and irrational
- You can lose money even following insider activity
- Always do your own research (DYOR)
- Consult a licensed financial advisor before investing

### Data Accuracy

- Data is scraped from OpenInsider.com (third-party source)
- Scraping can break if websites change structure
- Data may be delayed or incomplete
- Always verify with official SEC filings (sec.gov)
- Tool may have bugs or errors

**Use at your own risk.**

### Ethical Usage

- Respect OpenInsider's rate limits (we add delays)
- Do not abuse the scraping functionality
- Do not use for illegal purposes
- Insider trading laws apply (trading on material non-public information is illegal)

**This tool only uses publicly reported information.**

---

## 🙏 Acknowledgments

**Data Sources:**
- [OpenInsider](http://openinsider.com/) - Insider transaction data
- [SEC Edgar](https://www.sec.gov/) - Official filing source

**Technologies:**
- [Python](https://www.python.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/)
- [SQLite](https://www.sqlite.org/)

---

**Built with ❤️ for research and learning.**

*Remember: The best trade is often the one you don't make.*