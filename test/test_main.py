"""
Integration tests for main.py

Tests the complete 7-phase pipeline using mocked data.
Does NOT require network access or real OpenInsider scraping.

This validates:
1. User input handling
2. Data processing (deduplication)
3. Display logic
4. Scan history recording
5. Resource cleanup

Run with: python test/test_main_integration.py
"""

import sys
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    process_transactions,
    display_results,
    record_scan_history,
    cleanup_resources
)
from database.db import Database
from database.repository import TransactionRepository, ScanHistoryRepository
from utils.display import TerminalDisplay


# ============================================================================
# MOCK DATA
# ============================================================================

def create_mock_transaction(ticker, insider, trade_date, value):
    """Create a mock transaction dict"""
    return {
        'ticker': ticker,
        'company_name': f'{ticker} Corp',
        'filing_date': '2026-01-22 16:05:32',
        'trade_date': trade_date,
        'insider_name': insider,
        'insider_title': 'Executive',
        'trade_type': 'P - Purchase',
        'price': 100.0,
        'quantity': int(value / 100),
        'owned': 50000,
        'delta_own_pct': 25.0,
        'value': value,
        'scan_type': 'Test Scan'
    }


# ============================================================================
# TEST 1: Process Transactions - Empty List
# ============================================================================
def test_process_empty():
    """Test processing empty transaction list"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        display = TerminalDisplay()
        
        result = process_transactions([], repo, display)
        
        assert result['num_insert_success'] == 0, "No transactions should be inserted"
        assert result['num_duplicates'] == 0, "No duplicates should be found"
        assert result['highest_value'] == 0, "Highest value should be 0"
        assert len(result['new_transactions']) == 0, "New transactions list should be empty"
        
        db.close()
        print("✓ test_process_empty PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# TEST 2: Process Transactions - All New
# ============================================================================
def test_process_all_new():
    """Test processing all new transactions"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        display = TerminalDisplay()
        
        # Create mock transactions
        transactions = [
            create_mock_transaction('LSAK', 'Ali Mazanderani', '2026-01-21', 9000000),
            create_mock_transaction('TSLA', 'Elon Musk', '2026-01-20', 5000000),
            create_mock_transaction('AAPL', 'Tim Cook', '2026-01-19', 2000000),
        ]
        
        result = process_transactions(transactions, repo, display)
        
        assert result['num_insert_success'] == 3, "All 3 should be inserted"
        assert result['num_duplicates'] == 0, "No duplicates"
        assert result['highest_value'] == 9000000, "Highest should be 9M"
        assert len(result['new_transactions']) == 3, "Should have 3 new transactions"
        
        db.close()
        print("✓ test_process_all_new PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# TEST 3: Process Transactions - Mixed (New & Duplicates)
# ============================================================================
def test_process_mixed():
    """Test processing mix of new and duplicate transactions"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        display = TerminalDisplay()
        
        # First transaction (will be inserted)
        trans1 = create_mock_transaction('LSAK', 'Ali Mazanderani', '2026-01-21', 9000000)
        trans1['transaction_hash'] = 'LSAK_AliMazanderani_20260121_9000000'
        
        # Pre-insert one transaction
        repo.insert_transaction(trans1)
        
        # Now process batch with one new and one duplicate
        transactions = [
            trans1,  # Duplicate (already in DB)
            create_mock_transaction('TSLA', 'Elon Musk', '2026-01-20', 5000000),  # New
        ]
        
        result = process_transactions(transactions, repo, display)
        
        assert result['num_insert_success'] == 1, "Only 1 new should be inserted"
        assert result['num_duplicates'] == 1, "Should detect 1 duplicate"
        assert result['highest_value'] == 5000000, "Highest of NEW should be 5M"
        assert len(result['new_transactions']) == 1, "Should have 1 new transaction"
        
        db.close()
        print("✓ test_process_mixed PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# TEST 4: Process Transactions - All Duplicates
# ============================================================================
def test_process_all_duplicates():
    """Test processing all transactions that already exist"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = TransactionRepository(db)
        display = TerminalDisplay()
        
        # Create and pre-insert transactions
        trans = create_mock_transaction('LSAK', 'Ali Mazanderani', '2026-01-21', 9000000)
        trans['transaction_hash'] = 'LSAK_AliMazanderani_20260121_9000000'
        repo.insert_transaction(trans)
        
        # Process same transaction again
        result = process_transactions([trans], repo, display)
        
        assert result['num_insert_success'] == 0, "Should not insert duplicate"
        assert result['num_duplicates'] == 1, "Should detect duplicate"
        assert len(result['new_transactions']) == 0, "No new transactions"
        
        db.close()
        print("✓ test_process_all_duplicates PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# TEST 5: Display Results - No New Transactions
# ============================================================================
def test_display_no_new():
    """Test display when no new transactions"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        process_results = {
            'new_transactions': [],
            'num_insert_success': 0,
            'num_duplicates': 5,
            'num_insert_failed': 0,
            'highest_value': 0
        }
        
        display_results(display, process_results, "Test Scan", 5)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert 'No new transactions found' in output
        print("✓ test_display_no_new PASSED")
    finally:
        sys.stdout = old_stdout


# ============================================================================
# TEST 6: Display Results - With New Transactions
# ============================================================================
def test_display_with_new():
    """Test display with new transactions"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        transactions = [
            create_mock_transaction('LSAK', 'Ali', '2026-01-21', 9000000),
            create_mock_transaction('TSLA', 'Elon', '2026-01-20', 5000000),
        ]
        
        process_results = {
            'new_transactions': transactions,
            'num_insert_success': 2,
            'num_duplicates': 0,
            'num_insert_failed': 0,
            'highest_value': 9000000
        }
        
        display_results(display, process_results, "Test Scan", 2)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Should contain transaction info
        assert 'LSAK' in output, "Should display ticker"
        assert 'TSLA' in output, "Should display ticker"
        assert 'SCAN COMPLETE' in output, "Should show completion"
        
        print("✓ test_display_with_new PASSED")
    finally:
        sys.stdout = old_stdout


# ============================================================================
# TEST 7: Display Results - Sorting by Value
# ============================================================================
def test_display_sorting():
    """Test that results are sorted by value (highest first)"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Create transactions with different values
        trans_low = create_mock_transaction('LOW', 'Person1', '2026-01-20', 1000000)
        trans_high = create_mock_transaction('HIGH', 'Person2', '2026-01-21', 9000000)
        trans_mid = create_mock_transaction('MID', 'Person3', '2026-01-19', 5000000)
        
        # Add in random order
        transactions = [trans_low, trans_high, trans_mid]
        
        process_results = {
            'new_transactions': transactions,
            'num_insert_success': 3,
            'num_duplicates': 0,
            'num_insert_failed': 0,
            'highest_value': 9000000
        }
        
        display_results(display, process_results, "Test Scan", 3)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Find positions of each ticker in output
        high_pos = output.find('HIGH')
        mid_pos = output.find('MID')
        low_pos = output.find('LOW')
        
        # HIGH should appear before MID, MID before LOW (sorted by value descending)
        assert high_pos < mid_pos < low_pos, "Should be sorted by value (highest first)"
        
        print("✓ test_display_sorting PASSED")
    finally:
        sys.stdout = old_stdout


# ============================================================================
# TEST 8: Record Scan History
# ============================================================================
def test_record_scan_history():
    """Test recording scan metadata"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        repo = ScanHistoryRepository(db)
        
        record_scan_history(
            repo,
            scan_name="Test Scan",
            total_scraped=45,
            num_insert_success=12,
            num_duplicates=33,
            highest_value=9000000
        )
        
        # Verify it was recorded
        history = repo.get_scan_history(limit=1)
        
        assert len(history) == 1, "Should have recorded 1 scan"
        assert history[0]['scan_type'] == 'Test Scan'
        assert history[0]['num_transactions'] == 45
        assert history[0]['num_new'] == 12
        assert history[0]['num_duplicates'] == 33
        assert history[0]['highest_value'] == 9000000
        
        db.close()
        print("✓ test_record_scan_history PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# TEST 9: Cleanup Resources
# ============================================================================
def test_cleanup_resources():
    """Test that cleanup doesn't crash even if resources are None"""
    # Should not crash
    cleanup_resources(None, None)
    
    # Should not crash with mock objects
    mock_scraper = Mock()
    mock_db = Mock()
    cleanup_resources(mock_scraper, mock_db)
    
    # Verify close was called
    mock_scraper.close.assert_called_once()
    mock_db.close.assert_called_once()
    
    print("✓ test_cleanup_resources PASSED")


# ============================================================================
# TEST 10: End-to-End Pipeline (Simulated)
# ============================================================================
def test_end_to_end_pipeline():
    """
    Simulate complete 7-phase pipeline:
    1. Initialize
    2. Get input (mocked)
    3. Get data (mocked)
    4. Process
    5. Display
    6. Record history
    7. Cleanup
    """
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Phase 1: Initialize
        db = Database(db_path)
        transaction_repo = TransactionRepository(db)
        scan_history_repo = ScanHistoryRepository(db)
        display = TerminalDisplay()
        
        # Phase 2: Get input (simulated)
        choice = 'a'
        scan_name = 'Latest Cluster Buys'
        
        # Phase 3: Get data (mocked - return transaction list)
        transactions = [
            create_mock_transaction('LSAK', 'Ali', '2026-01-21', 9000000),
            create_mock_transaction('TSLA', 'Elon', '2026-01-20', 5000000),
            create_mock_transaction('AAPL', 'Tim', '2026-01-19', 2000000),
        ]
        scraper = None  # Not used in this test
        
        # Phase 4: Process
        process_results = process_transactions(transactions, transaction_repo, display)
        
        # Verify processing worked
        assert process_results['num_insert_success'] == 3
        assert len(process_results['new_transactions']) == 3
        
        # Phase 5: Display (in stdout, just don't crash)
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        display_results(display, process_results, scan_name, len(transactions))
        sys.stdout = old_stdout
        
        # Phase 6: Record history
        record_scan_history(
            scan_history_repo,
            scan_name,
            len(transactions),
            process_results['num_insert_success'],
            process_results['num_duplicates'],
            process_results['highest_value']
        )
        
        # Verify history was recorded
        history = scan_history_repo.get_scan_history(limit=1)
        assert len(history) == 1
        assert history[0]['num_new'] == 3
        
        # Phase 7: Cleanup
        cleanup_resources(scraper, db)
        
        print("✓ test_end_to_end_pipeline PASSED")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# ============================================================================
# RUN ALL TESTS
# ============================================================================
def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("RUNNING MAIN.PY INTEGRATION TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_process_empty,
        test_process_all_new,
        test_process_mixed,
        test_process_all_duplicates,
        test_display_no_new,
        test_display_with_new,
        test_display_sorting,
        test_record_scan_history,
        test_cleanup_resources,
        test_end_to_end_pipeline,
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