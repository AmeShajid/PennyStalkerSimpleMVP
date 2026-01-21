# PennyStalker Test Suite

This folder contains comprehensive tests for all completed components of the PennyStalker project.

## Test Files

### 1. `test_hash_utils.py`
Tests the `hash_utils.generate_transaction_hash()` function

**What it tests:**
- Hash generation with valid transaction data
- Handling of spaces in insider names (removal)
- Handling of dashes in dates (removal)
- Handling of missing fields (defaults to "UNKNOWN")
- Float to integer conversion for values
- Hash consistency (same input = same output)

**How to run:**
```bash
python test_hash_utils.py
```

**Expected output:** 10 tests should pass

---

### 2. `test_display.py`
Tests the `TerminalDisplay` class and all display methods

**What it tests:**
- Border and separator creation
- Transaction display formatting
- Emoji indicators:
  - ⭐ for transactions $1M+
  - 🚀 for ownership changes 50%+
- Number formatting (commas for thousands)
- Summary statistics display
- Error message display
- Message display for no new transactions

**How to run:**
```bash
python test_display.py
```

**Expected output:** 11 tests should pass

---

### 3. `test_database.py`
Tests the database layer (db.py, models.py, repository.py)

**What it tests:**
- Database file creation
- Schema initialization (tables and indexes)
- Database execution (queries)
- TransactionRepository:
  - Inserting transactions
  - Checking if transaction exists (by hash)
  - Getting transactions by ticker
  - Getting all transactions
- ScanHistoryRepository:
  - Recording scan metadata
  - Retrieving scan history
- Context manager functionality
- Commit/rollback operations

**How to run:**
```bash
python test_database.py
```

**Expected output:** 11 tests should pass

---

## Running All Tests

### Option 1: Run Master Test Suite
```bash
python run_all_tests.py
```

This will run all tests in sequence and provide a summary.

### Option 2: Run Individual Tests
```bash
python test_hash_utils.py
python test_display.py
python test_database.py
```

### Option 3: Run Tests with Coverage (advanced)
```bash
pip install coverage
coverage run -m pytest tests/
coverage report
```

---

## Test Results Legend

- **✓ PASSED** - Test completed successfully
- **✗ FAILED** - Test encountered an assertion error
- **✗ ERROR** - Test crashed with an exception

---

## What Gets Tested

### Hash Utils
- [x] Normal transaction hashing
- [x] Space removal in names
- [x] Dash removal in dates
- [x] Missing field defaults
- [x] Type conversion (float to int)
- [x] Hash consistency

### Display
- [x] Border/separator creation
- [x] Transaction display
- [x] Emoji indicators (⭐, 🚀)
- [x] Number formatting
- [x] Summary display
- [x] Error messages
- [x] No transactions message

### Database
- [x] Database creation
- [x] Schema initialization
- [x] Table creation
- [x] Index creation
- [x] Query execution
- [x] Transaction insertion
- [x] Deduplication (hash uniqueness)
- [x] Ticker search
- [x] Scan history recording
- [x] Context manager
- [x] Commit/rollback

---

## Before Running Tests

Make sure your project structure looks like this:

```
PENNYSTALKERSIMPLEMVP/
├── database/
│   ├── __init__.py
│   ├── db.py
│   ├── models.py
│   └── repository.py
├── utils/
│   ├── __init__.py
│   ├── display.py
│   └── hash_utils.py
├── scrapers/
│   └── __init__.py
├── tests/              ← You are here
│   ├── test_hash_utils.py
│   ├── test_display.py
│   ├── test_database.py
│   ├── run_all_tests.py
│   └── TEST_README.md
└── main.py
```

---

## Test Isolation

Each database test uses temporary files (`tempfile.NamedTemporaryFile`) so tests don't interfere with each other or your main database file.

---

## Debugging Failed Tests

If a test fails:

1. **Read the error message** - It will tell you exactly what assertion failed
2. **Check the test code** - Look at what the test expected vs. what it got
3. **Check your implementation** - Make sure the function matches the expected behavior
4. **Run in isolation** - Run just that one test file to focus on the problem

Example:
```bash
# This will show detailed error info
python test_hash_utils.py
```

---

## Next Steps

Once all tests pass:

1. ✅ Hash utils - TESTED
2. ✅ Display - TESTED  
3. ✅ Database - TESTED
4. ⏳ Scrapers - Ready to build (base.py and openinsider.py)
5. ⏳ Main orchestrator - Will tie everything together

---

## Notes

- Tests create temporary databases and clean them up automatically
- No real API calls are made during tests (all data is mocked)
- Each test is independent and can be run in any order
- Tests verify core functionality, not edge cases (those can be added later)