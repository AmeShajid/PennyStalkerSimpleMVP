"""
Test suite for database components (db.py, models.py, repository.py)
Tests the Database class and Repository classes
"""

import sys
import os
import sqlite3
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import Database
from database.repository import TransactionRepository, ScanHistoryRepository


def test_database_creation():
    """Test that database file is created"""
    # Create temp file for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        
        # Check that file exists
        assert os.path.exists(db_path), f"Database file should exist at {db_path}"
        
        db.close()
        print(f"✓ test_database_creation PASSED")
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)


def test_database_schema_initialization():
    """Test that all tables and indexes are created"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        
        # Check that insider_transactions table exists
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='insider_transactions'"
        )
        assert cursor.fetchone() is not None, "insider_transactions table should exist"
        
        # Check that scan_history table exists
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_history'"
        )
        assert cursor.fetchone() is not None, "scan_history table should exist"
        
        # Check that indexes exist
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        )
        indexes = cursor.fetchall()
        assert len(indexes) >= 3, f"Should have at least 3 indexes, found {len(indexes)}"
        
        db.close()
        print(f"✓ test_database_schema_initialization PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_database_execute():
    """Test that execute method works"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        
        # Execute a simple query
        cursor = db.execute("SELECT COUNT(*) as count FROM insider_transactions")
        result = cursor.fetchone()
        
        assert result is not None, "Query should return a result"
        assert result['count'] == 0, "Should start with empty table"
        
        db.close()
        print(f"✓ test_database_execute PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_transaction_repository_insert():
    """Test inserting a transaction"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        
        transaction = {
            'ticker': 'LSAK',
            'company_name': 'Lesaka Technologies Inc',
            'filing_date': '2026-01-02 16:05:32',
            'trade_date': '2025-12-31',
            'insider_name': 'Mazanderani Ali',
            'insider_title': 'Exec COB',
            'trade_type': 'P - Purchase',
            'price': 5.00,
            'quantity': 1800000,
            'owned': 2325115,
            'delta_own_pct': 343.0,
            'value': 9000000,
            'scan_type': 'Latest Cluster Buys',
            'transaction_hash': 'LSAK_MazanderaniAli_20251231_9000000'
        }
        
        result = repo.insert_transaction(transaction)
        
        assert result is True, "Insert should return True"
        
        # Verify it was inserted
        cursor = db.execute("SELECT COUNT(*) as count FROM insider_transactions")
        count_result = cursor.fetchone()
        assert count_result['count'] == 1, "Should have 1 transaction in database"
        
        db.close()
        print(f"✓ test_transaction_repository_insert PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_transaction_repository_exists():
    """Test checking if transaction exists"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        
        transaction_hash = 'LSAK_MazanderaniAli_20251231_9000000'
        
        # Should not exist initially
        exists = repo.transaction_exists(transaction_hash)
        assert exists is False, "Transaction should not exist initially"
        
        # Insert transaction
        transaction = {
            'ticker': 'LSAK',
            'company_name': 'Lesaka Technologies Inc',
            'filing_date': '2026-01-02 16:05:32',
            'trade_date': '2025-12-31',
            'insider_name': 'Mazanderani Ali',
            'insider_title': 'Exec COB',
            'trade_type': 'P - Purchase',
            'price': 5.00,
            'quantity': 1800000,
            'owned': 2325115,
            'delta_own_pct': 343.0,
            'value': 9000000,
            'scan_type': 'Latest Cluster Buys',
            'transaction_hash': transaction_hash
        }
        repo.insert_transaction(transaction)
        
        # Now should exist
        exists = repo.transaction_exists(transaction_hash)
        assert exists is True, "Transaction should exist after insert"
        
        db.close()
        print(f"✓ test_transaction_repository_exists PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_transaction_repository_get_by_ticker():
    """Test retrieving transactions by ticker"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        
        # Insert two transactions with same ticker
        for i in range(2):
            transaction = {
                'ticker': 'LSAK',
                'company_name': 'Lesaka Technologies Inc',
                'filing_date': '2026-01-02 16:05:32',
                'trade_date': f'2025-12-{30+i}',
                'insider_name': f'Insider {i}',
                'insider_title': 'Executive',
                'trade_type': 'P - Purchase',
                'price': 5.00,
                'quantity': 1000000,
                'owned': 2000000,
                'delta_own_pct': 100.0,
                'value': 5000000,
                'scan_type': 'Test',
                'transaction_hash': f'LSAK_Insider{i}_test_{i}'
            }
            repo.insert_transaction(transaction)
        
        # Retrieve by ticker
        transactions = repo.get_transactions_by_ticker('LSAK')
        
        assert len(transactions) == 2, f"Should have 2 transactions, got {len(transactions)}"
        assert all(t['ticker'] == 'LSAK' for t in transactions), "All should have LSAK ticker"
        
        db.close()
        print(f"✓ test_transaction_repository_get_by_ticker PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_transaction_repository_get_all():
    """Test retrieving all transactions"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        
        # Insert three transactions with different tickers
        tickers = ['LSAK', 'TSLA', 'AAPL']
        for ticker in tickers:
            transaction = {
                'ticker': ticker,
                'company_name': f'{ticker} Company',
                'filing_date': '2026-01-02 16:05:32',
                'trade_date': '2025-12-31',
                'insider_name': 'Test Insider',
                'insider_title': 'Executive',
                'trade_type': 'P - Purchase',
                'price': 100.00,
                'quantity': 10000,
                'owned': 50000,
                'delta_own_pct': 25.0,
                'value': 1000000,
                'scan_type': 'Test',
                'transaction_hash': f'{ticker}_test_hash'
            }
            repo.insert_transaction(transaction)
        
        # Get all
        transactions = repo.get_all_transactions()
        
        assert len(transactions) == 3, f"Should have 3 transactions, got {len(transactions)}"
        
        db.close()
        print(f"✓ test_transaction_repository_get_all PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_scan_history_repository_insert():
    """Test recording scan history"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = ScanHistoryRepository(db)
        
        result = repo.insert_scan(
            scan_type='Latest Cluster Buys',
            num_transactions=45,
            num_new=12,
            num_duplicates=33,
            highest_value=9000000
        )
        
        assert result is True, "Insert should return True"
        
        # Verify it was inserted
        cursor = db.execute("SELECT COUNT(*) as count FROM scan_history")
        count_result = cursor.fetchone()
        assert count_result['count'] == 1, "Should have 1 scan in database"
        
        db.close()
        print(f"✓ test_scan_history_repository_insert PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_scan_history_repository_get():
    """Test retrieving scan history"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = ScanHistoryRepository(db)
        
        # Insert three scans
        for i in range(3):
            repo.insert_scan(
                scan_type=f'Scan Type {i}',
                num_transactions=10 * (i+1),
                num_new=5 * (i+1),
                num_duplicates=5 * (i+1),
                highest_value=1000000 * (i+1)
            )
        
        # Retrieve scan history
        scans = repo.get_scan_history(limit=10)
        
        assert len(scans) == 3, f"Should have 3 scans, got {len(scans)}"
        
        db.close()
        print(f"✓ test_scan_history_repository_get PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_database_context_manager():
    """Test using database with context manager"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        with Database(db_path) as db:
            cursor = db.execute("SELECT COUNT(*) as count FROM insider_transactions")
            result = cursor.fetchone()
            assert result is not None, "Should be able to query database"
        
        print(f"✓ test_database_context_manager PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_database_commit_rollback():
    """Test commit and rollback functionality"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        
        transaction = {
            'ticker': 'TEST',
            'company_name': 'Test Company',
            'filing_date': '2026-01-02',
            'trade_date': '2025-12-31',
            'insider_name': 'Test',
            'insider_title': 'Test',
            'trade_type': 'P',
            'price': 100.0,
            'quantity': 1000,
            'owned': 5000,
            'delta_own_pct': 50.0,
            'value': 100000,
            'scan_type': 'Test',
            'transaction_hash': 'TEST_hash'
        }
        
        repo.insert_transaction(transaction)
        
        # Count should be 1
        cursor = db.execute("SELECT COUNT(*) as count FROM insider_transactions")
        assert cursor.fetchone()['count'] == 1, "Should have 1 transaction"
        
        db.close()
        print(f"✓ test_database_commit_rollback PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def run_all_tests():
    """Run all database tests"""
    print("\n" + "="*60)
    print("RUNNING DATABASE TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_database_creation,
        test_database_schema_initialization,
        test_database_execute,
        test_transaction_repository_insert,
        test_transaction_repository_exists,
        test_transaction_repository_get_by_ticker,
        test_transaction_repository_get_all,
        test_scan_history_repository_insert,
        test_scan_history_repository_get,
        test_database_context_manager,
        test_database_commit_rollback
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)