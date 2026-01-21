"""
Test suite for hash_utils.py
Tests the generate_transaction_hash function
"""

import sys
import os

# Add parent directory to path so we can import from utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.hash_utils import generate_transaction_hash


def test_normal_transaction():
    """Test with a normal transaction that has all fields"""
    transaction = {
        'ticker': 'LSAK',
        'insider_name': 'Mazanderani Ali',
        'trade_date': '2025-12-31',
        'value': 9000000
    }
    
    result = generate_transaction_hash(transaction)
    expected = "LSAK_MazanderaniAli_20251231_9000000"
    
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ test_normal_transaction PASSED")


def test_transaction_with_spaces_in_name():
    """Test that spaces are removed from insider names"""
    transaction = {
        'ticker': 'TSLA',
        'insider_name': 'Elon Musk',
        'trade_date': '2025-01-15',
        'value': 500000
    }
    
    result = generate_transaction_hash(transaction)
    expected = "TSLA_ElonMusk_20250115_500000"
    
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ test_transaction_with_spaces_in_name PASSED")


def test_missing_ticker():
    """Test that missing ticker defaults to UNKNOWN"""
    transaction = {
        'insider_name': 'John Doe',
        'trade_date': '2025-01-10',
        'value': 100000
    }
    
    result = generate_transaction_hash(transaction)
    # Should have UNKNOWN as ticker
    assert result.startswith("Unknown_"), f"Expected to start with 'Unknown_', got {result}"
    print(f"✓ test_missing_ticker PASSED")


def test_missing_insider_name():
    """Test that missing insider name defaults to UNKNOWN"""
    transaction = {
        'ticker': 'AAPL',
        'trade_date': '2025-01-10',
        'value': 250000
    }
    
    result = generate_transaction_hash(transaction)
    # Should have UNKNOWN in second position
    parts = result.split('_')
    assert parts[1] == "Unknown", f"Expected 'Unknown' at position 1, got {parts[1]}"
    print(f"✓ test_missing_insider_name PASSED")


def test_missing_trade_date():
    """Test that missing trade date defaults to UNKNOWN"""
    transaction = {
        'ticker': 'MSFT',
        'insider_name': 'Bill Gates',
        'value': 1000000
    }
    
    result = generate_transaction_hash(transaction)
    # Should have UNKNOWN in third position
    parts = result.split('_')
    assert parts[2] == "Unknown", f"Expected 'Unknown' at position 2, got {parts[2]}"
    print(f"✓ test_missing_trade_date PASSED")


def test_missing_value():
    """Test that missing value defaults to 0"""
    transaction = {
        'ticker': 'GOOGL',
        'insider_name': 'Sundar Pichai',
        'trade_date': '2025-01-20'
    }
    
    result = generate_transaction_hash(transaction)
    # Should end with _0
    assert result.endswith("_0"), f"Expected to end with '_0', got {result}"
    print(f"✓ test_missing_value PASSED")


def test_all_missing_fields():
    """Test with completely empty transaction"""
    transaction = {}
    
    result = generate_transaction_hash(transaction)
    expected = "Unknown_Unknown_Unknown_0"
    
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ test_all_missing_fields PASSED")


def test_float_value_converted_to_int():
    """Test that float values are converted to integers"""
    transaction = {
        'ticker': 'NVDA',
        'insider_name': 'Jensen Huang',
        'trade_date': '2025-01-05',
        'value': 5500000.75  # Float value
    }
    
    result = generate_transaction_hash(transaction)
    # Should convert float to int (5500000.75 -> 5500000)
    assert result.endswith("_5500000"), f"Expected to end with '_5500000', got {result}"
    print(f"✓ test_float_value_converted_to_int PASSED")


def test_date_dashes_removed():
    """Test that dashes are removed from date format"""
    transaction = {
        'ticker': 'META',
        'insider_name': 'Mark Zuckerberg',
        'trade_date': '2025-01-20',  # Format with dashes
        'value': 2000000
    }
    
    result = generate_transaction_hash(transaction)
    # Should remove dashes: 2025-01-20 -> 20250120
    assert "20250120" in result, f"Expected date without dashes in {result}"
    assert "-" not in result, f"Result should not contain dashes: {result}"
    print(f"✓ test_date_dashes_removed PASSED")


def test_consistency():
    """Test that the same transaction always produces the same hash"""
    transaction = {
        'ticker': 'AMD',
        'insider_name': 'Lisa Su',
        'trade_date': '2025-01-12',
        'value': 750000
    }
    
    hash1 = generate_transaction_hash(transaction)
    hash2 = generate_transaction_hash(transaction)
    hash3 = generate_transaction_hash(transaction)
    
    assert hash1 == hash2 == hash3, f"Hashes should be consistent: {hash1}, {hash2}, {hash3}"
    print(f"✓ test_consistency PASSED")


def run_all_tests():
    """Run all test functions"""
    print("\n" + "="*60)
    print("RUNNING HASH_UTILS TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_normal_transaction,
        test_transaction_with_spaces_in_name,
        test_missing_ticker,
        test_missing_insider_name,
        test_missing_trade_date,
        test_missing_value,
        test_all_missing_fields,
        test_float_value_converted_to_int,
        test_date_dashes_removed,
        test_consistency
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