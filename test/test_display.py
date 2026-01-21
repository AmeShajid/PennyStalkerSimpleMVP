"""
Test suite for display.py
Tests the TerminalDisplay class
"""

import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.display import TerminalDisplay


def test_border_creation():
    """Test that borders are created with correct width"""
    display = TerminalDisplay()
    border = display.create_border()
    
    assert len(border) == 60, f"Border should be 60 chars, got {len(border)}"
    assert border == "=" * 60, f"Border should be all '=', got {border}"
    print(f"✓ test_border_creation PASSED")


def test_separator_creation():
    """Test that separators are created with correct width"""
    display = TerminalDisplay()
    separator = display.create_separator()
    
    assert len(separator) == 60, f"Separator should be 60 chars, got {len(separator)}"
    assert separator == "-" * 60, f"Separator should be all '-', got {separator}"
    print(f"✓ test_separator_creation PASSED")


def test_display_attributes():
    """Test that display object initializes with correct attributes"""
    display = TerminalDisplay()
    
    assert display.border_char == "=", f"Expected border_char '=', got {display.border_char}"
    assert display.separator_char == "-", f"Expected separator_char '-', got {display.separator_char}"
    assert display.width == 60, f"Expected width 60, got {display.width}"
    print(f"✓ test_display_attributes PASSED")


def test_display_transaction_basic():
    """Test that transaction displays without error"""
    display = TerminalDisplay()
    
    transaction = {
        'ticker': 'LSAK',
        'company_name': 'Lesaka Technologies Inc',
        'insider_name': 'Mazanderani Ali',
        'insider_title': 'Exec COB',
        'filing_date': '2026-01-02 16:05:32',
        'trade_date': '2025-12-31',
        'price': 5.00,
        'quantity': 1800000,
        'owned': 2325115,
        'delta_own_pct': 343.0,
        'value': 9000000
    }
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_transaction(transaction, rank=1)
        output = sys.stdout.getvalue()
        
        # Check that key information is in output
        assert 'LSAK' in output, "Output should contain ticker"
        assert 'Lesaka Technologies Inc' in output, "Output should contain company name"
        assert 'Mazanderani Ali' in output, "Output should contain insider name"
        assert '$9,000,000' in output, "Output should contain formatted value"
        assert '1,800,000 shares' in output, "Output should contain formatted quantity"
        assert '343.0%' in output, "Output should contain delta ownership percentage"
        
        print(f"✓ test_display_transaction_basic PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_transaction_with_star():
    """Test that transactions over $1M display with star emoji"""
    display = TerminalDisplay()
    
    transaction = {
        'ticker': 'AAPL',
        'company_name': 'Apple Inc',
        'insider_name': 'Tim Cook',
        'insider_title': 'CEO',
        'filing_date': '2025-12-01',
        'trade_date': '2025-11-30',
        'price': 200.00,
        'quantity': 10000,
        'owned': 50000,
        'delta_own_pct': 25.0,
        'value': 2000000  # Over $1M
    }
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_transaction(transaction, rank=1)
        output = sys.stdout.getvalue()
        
        assert '⭐' in output, "Output should contain star emoji for $1M+ transactions"
        
        print(f"✓ test_display_transaction_with_star PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_transaction_with_rocket():
    """Test that transactions with 50%+ ownership change display rocket emoji"""
    display = TerminalDisplay()
    
    transaction = {
        'ticker': 'TSLA',
        'company_name': 'Tesla Inc',
        'insider_name': 'Elon Musk',
        'insider_title': 'CEO',
        'filing_date': '2025-12-15',
        'trade_date': '2025-12-14',
        'price': 250.00,
        'quantity': 5000,
        'owned': 100000,
        'delta_own_pct': 60.0,  # Over 50%
        'value': 1250000
    }
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_transaction(transaction, rank=1)
        output = sys.stdout.getvalue()
        
        assert '🚀' in output, "Output should contain rocket emoji for 50%+ ownership change"
        
        print(f"✓ test_display_transaction_with_rocket PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_summary():
    """Test that summary displays correctly"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_summary(
            total_scraped=45,
            num_new=12,
            num_duplicates=33,
            highest_value=9000000
        )
        output = sys.stdout.getvalue()
        
        assert 'SCAN COMPLETE' in output, "Output should contain SCAN COMPLETE"
        assert '45 transactions' in output, "Output should show total scraped"
        assert '12' in output, "Output should show new transactions"
        assert '33' in output, "Output should show duplicates"
        assert '9,000,000' in output, "Output should show highest value"
        
        print(f"✓ test_display_summary PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_no_new_transactions():
    """Test that no new transactions message displays"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_no_new_transactions()
        output = sys.stdout.getvalue()
        
        assert 'No new transactions found' in output, "Output should contain 'No new transactions found'"
        
        print(f"✓ test_display_no_new_transactions PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_error():
    """Test that error messages display correctly"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_error("Test error message")
        output = sys.stdout.getvalue()
        
        assert 'ERROR' in output, "Output should contain ERROR"
        assert 'Test error message' in output, "Output should contain error message"
        
        print(f"✓ test_display_error PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_display_processing_message():
    """Test processing message displays"""
    display = TerminalDisplay()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_processing_message(50)
        output = sys.stdout.getvalue()
        
        assert '50' in output, "Output should contain transaction count"
        assert 'Processing' in output, "Output should say Processing"
        
        print(f"✓ test_display_processing_message PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_number_formatting():
    """Test that numbers are formatted with commas"""
    display = TerminalDisplay()
    
    transaction = {
        'ticker': 'TEST',
        'company_name': 'Test Company',
        'insider_name': 'Test Person',
        'insider_title': 'Test Title',
        'filing_date': '2025-01-01',
        'trade_date': '2025-01-01',
        'price': 100.00,
        'quantity': 1000000,  # Should format as 1,000,000
        'owned': 5000000,
        'delta_own_pct': 25.0,
        'value': 100000000  # Should format as 100,000,000
    }
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        display.display_transaction(transaction, rank=1)
        output = sys.stdout.getvalue()
        
        assert '1,000,000' in output, "Quantity should be formatted with commas"
        assert '100,000,000' in output, "Value should be formatted with commas"
        
        print(f"✓ test_number_formatting PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def run_all_tests():
    """Run all display tests"""
    print("\n" + "="*60)
    print("RUNNING DISPLAY TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_border_creation,
        test_separator_creation,
        test_display_attributes,
        test_display_transaction_basic,
        test_display_transaction_with_star,
        test_display_transaction_with_rocket,
        test_display_summary,
        test_display_no_new_transactions,
        test_display_error,
        test_display_processing_message,
        test_number_formatting
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}", file=sys.stderr)
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}", file=sys.stderr)
            failed += 1
    
    print("\n" + "="*60, file=sys.stderr)
    print(f"RESULTS: {passed} passed, {failed} failed", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)