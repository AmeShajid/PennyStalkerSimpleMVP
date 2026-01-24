"""
Test suite for scrapers/openinsider.py
Tests the OpenInsiderScraper class including URL building, parsing, and data cleaning
"""

import sys
import os
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers.openinsider import OpenInsiderScraper, OPTIONS_DICTIONARY


def test_options_dictionary_exists():
    """Test that OPTIONS_DICTIONARY is defined and has all options"""
    assert OPTIONS_DICTIONARY is not None, "OPTIONS_DICTIONARY should exist"
    assert len(OPTIONS_DICTIONARY) == 16, f"Should have 16 options, got {len(OPTIONS_DICTIONARY)}"
    print(f"✓ test_options_dictionary_exists PASSED")


def test_options_dictionary_has_all_letters():
    """Test that all letters a-q are in OPTIONS_DICTIONARY"""
    expected_options = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']
    
    for option in expected_options:
        assert option in OPTIONS_DICTIONARY, f"Option '{option}' missing from OPTIONS_DICTIONARY"
    
    print(f"✓ test_options_dictionary_has_all_letters PASSED")


def test_options_dictionary_structure():
    """Test that each option has required fields (name, url, needs_timeframe)"""
    for option, config in OPTIONS_DICTIONARY.items():
        assert 'name' in config, f"Option '{option}' missing 'name'"
        assert 'url' in config, f"Option '{option}' missing 'url'"
        assert 'needs_timeframe' in config, f"Option '{option}' missing 'needs_timeframe'"
        assert isinstance(config['name'], str), f"Option '{option}' name should be string"
        assert isinstance(config['url'], str), f"Option '{option}' url should be string"
        assert isinstance(config['needs_timeframe'], bool), f"Option '{option}' needs_timeframe should be bool"
    
    print(f"✓ test_options_dictionary_structure PASSED")


def test_latest_options_need_timeframe():
    """Test that options a-k need timeframe"""
    latest_options = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    
    for option in latest_options:
        assert OPTIONS_DICTIONARY[option]['needs_timeframe'] is True, \
            f"Option '{option}' should need timeframe"
    
    print(f"✓ test_latest_options_need_timeframe PASSED")


def test_top_options_dont_need_timeframe():
    """Test that options l-q don't need timeframe"""
    top_options = ['l', 'm', 'n', 'o', 'p', 'q']
    
    for option in top_options:
        assert OPTIONS_DICTIONARY[option]['needs_timeframe'] is False, \
            f"Option '{option}' should not need timeframe"
    
    print(f"✓ test_top_options_dont_need_timeframe PASSED")


def test_openinsider_scraper_initialization():
    """Test that OpenInsiderScraper initializes correctly"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    assert scraper.scan_type == 'a', "scan_type should be 'a'"
    assert scraper.timeframe == '2weeks', "timeframe should be '2weeks'"
    assert scraper.scan_name == OPTIONS_DICTIONARY['a']['name'], "scan_name should match config"
    assert scraper.session is not None, "session should be initialized from BaseScraper"
    
    scraper.close()
    print(f"✓ test_openinsider_scraper_initialization PASSED")


def test_openinsider_scraper_invalid_option():
    """Test that invalid scan type raises error"""
    try:
        scraper = OpenInsiderScraper('z', '2weeks')  # Invalid option
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid scan type" in str(e)
        print(f"✓ test_openinsider_scraper_invalid_option PASSED")


def test_build_url_with_timeframe():
    """Test building URL for option that needs timeframe"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    url = scraper.build_url()
    
    # URL should be base URL + timeframe parameter
    assert 'latest-cluster-buys' in url, "URL should contain latest-cluster-buys"
    assert '2weeks' in url, "URL should contain timeframe parameter"
    
    scraper.close()
    print(f"✓ test_build_url_with_timeframe PASSED")


def test_build_url_with_month_timeframe():
    """Test building URL with month timeframe"""
    scraper = OpenInsiderScraper('a', 'month')
    
    url = scraper.build_url()
    
    assert 'latest-cluster-buys' in url, "URL should contain latest-cluster-buys"
    assert 'month' in url, "URL should contain month timeframe"
    
    scraper.close()
    print(f"✓ test_build_url_with_month_timeframe PASSED")


def test_build_url_without_timeframe():
    """Test building URL for option that doesn't need timeframe"""
    scraper = OpenInsiderScraper('l', None)  # TOP option, no timeframe needed
    
    url = scraper.build_url()
    
    # URL should be just base URL, no timeframe parameter
    assert 'top-officer-purchases' in url, "URL should contain top-officer-purchases"
    assert 'timeframe=' not in url, "URL should not contain timeframe parameter"
    
    scraper.close()
    print(f"✓ test_build_url_without_timeframe PASSED")


def test_clean_number_with_currency():
    """Test cleaning currency values"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.clean_number('$21,868,640', is_currency=True)
    assert result == 21868640.0, f"Expected 21868640.0, got {result}"
    
    scraper.close()
    print(f"✓ test_clean_number_with_currency PASSED")


def test_clean_number_with_comma():
    """Test cleaning numbers with commas"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.clean_number('1,024,000', is_integer=True)
    assert result == 1024000, f"Expected 1024000, got {result}"
    
    scraper.close()
    print(f"✓ test_clean_number_with_comma PASSED")


def test_clean_number_with_negative():
    """Test cleaning negative numbers"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.clean_number('-$500,000', is_currency=True)
    assert result == -500000.0, f"Expected -500000.0, got {result}"
    
    scraper.close()
    print(f"✓ test_clean_number_with_negative PASSED")


def test_clean_number_with_new():
    """Test cleaning 'New' value"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.clean_number('New')
    assert result == 0, f"Expected 0 for 'New', got {result}"
    
    scraper.close()
    print(f"✓ test_clean_number_with_new PASSED")


def test_clean_number_empty():
    """Test cleaning empty value"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.clean_number('')
    assert result == 0, f"Expected 0 for empty string, got {result}"
    
    scraper.close()
    print(f"✓ test_clean_number_empty PASSED")


def test_extract_percentage():
    """Test extracting percentage from text"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.extract_percentage('+343%')
    assert result == 343.0, f"Expected 343.0, got {result}"
    
    scraper.close()
    print(f"✓ test_extract_percentage PASSED")


def test_extract_percentage_negative():
    """Test extracting negative percentage"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.extract_percentage('-15%')
    assert result == -15.0, f"Expected -15.0, got {result}"
    
    scraper.close()
    print(f"✓ test_extract_percentage_negative PASSED")


def test_extract_percentage_no_percent():
    """Test extracting percentage when none present"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.extract_percentage('no percent here')
    assert result == 0.0, f"Expected 0.0 for missing percent, got {result}"
    
    scraper.close()
    print(f"✓ test_extract_percentage_no_percent PASSED")


def test_extract_currency():
    """Test extracting currency from text"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.extract_currency('$21,868,640')
    assert result == 21868640.0, f"Expected 21868640.0, got {result}"
    
    scraper.close()
    print(f"✓ test_extract_currency PASSED")


def test_extract_currency_negative():
    """Test extracting negative currency"""
    scraper = OpenInsiderScraper('a', '2weeks')
    
    result = scraper.extract_currency('-$500,000')
    assert result == -500000.0, f"Expected -500000.0, got {result}"
    
    scraper.close()
    print(f"✓ test_extract_currency_negative PASSED")


@patch('scrapers.openinsider.OpenInsiderScraper.fetch')
def test_scrape_fetch_failure(mock_fetch):
    """Test scrape when fetch returns None"""
    mock_fetch.return_value = None
    
    scraper = OpenInsiderScraper('a', '2weeks')
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.scrape()
        sys.stdout = old_stdout
        
        assert result == [], "Should return empty list when fetch fails"
        assert mock_fetch.called, "fetch should have been called"
        
        print(f"✓ test_scrape_fetch_failure PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.openinsider.OpenInsiderScraper.fetch')
def test_scrape_empty_html(mock_fetch):
    """Test scrape with no table in HTML"""
    mock_fetch.return_value = "<html><body>No table here</body></html>"
    
    scraper = OpenInsiderScraper('a', '2weeks')
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.scrape()
        sys.stdout = old_stdout
        
        assert result == [], "Should return empty list when no table found"
        
        print(f"✓ test_scrape_empty_html PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.openinsider.OpenInsiderScraper.fetch')
def test_scrape_with_sample_table(mock_fetch):
    """Test scrape with sample HTML table"""
    # Sample HTML with a simple transaction table
    sample_html = """
    <html>
    <body>
    <table>
        <tr>
            <th>Filing Date</th>
            <th>Trade Date</th>
            <th>Ticker</th>
            <th>Company Name</th>
            <th>Industry</th>
            <th>Insider Name</th>
            <th>Title</th>
            <th>Trade Type</th>
            <th>Price</th>
            <th>Qty</th>
            <th>Owned</th>
            <th>ΔOwn Value</th>
        </tr>
        <tr>
            <td>2026-01-22 16:02:03</td>
            <td>2026-01-21</td>
            <td>GME</td>
            <td>Gamestop Corp</td>
            <td>Retail</td>
            <td>Zhou Hongyi</td>
            <td>Dr</td>
            <td>P - Purchase</td>
            <td>$21.36</td>
            <td>1,024,000</td>
            <td>38,944,306</td>
            <td>+343% $21,868,640</td>
        </tr>
    </table>
    </body>
    </html>
    """
    
    mock_fetch.return_value = sample_html
    
    scraper = OpenInsiderScraper('a', '2weeks')
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.scrape()
        sys.stdout = old_stdout
        
        # Should have extracted 1 transaction (header row should be skipped)
        assert len(result) >= 1, f"Should extract at least 1 transaction, got {len(result)}"
        
        # Check first transaction has required fields
        if len(result) > 0:
            trans = result[0]
            assert 'ticker' in trans, "Transaction should have ticker"
            assert 'company_name' in trans, "Transaction should have company_name"
            assert 'price' in trans, "Transaction should have price"
            assert 'quantity' in trans, "Transaction should have quantity"
        
        print(f"✓ test_scrape_with_sample_table PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("RUNNING OPENINSIDER SCRAPER TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_options_dictionary_exists,
        test_options_dictionary_has_all_letters,
        test_options_dictionary_structure,
        test_latest_options_need_timeframe,
        test_top_options_dont_need_timeframe,
        test_openinsider_scraper_initialization,
        test_openinsider_scraper_invalid_option,
        test_build_url_with_timeframe,
        test_build_url_with_month_timeframe,
        test_build_url_without_timeframe,
        test_clean_number_with_currency,
        test_clean_number_with_comma,
        test_clean_number_with_negative,
        test_clean_number_with_new,
        test_clean_number_empty,
        test_extract_percentage,
        test_extract_percentage_negative,
        test_extract_percentage_no_percent,
        test_extract_currency,
        test_extract_currency_negative,
        test_scrape_fetch_failure,
        test_scrape_empty_html,
        test_scrape_with_sample_table,
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