"""
Test suite for scrapers/base.py
Tests the BaseScraper class including initialization, fetching, and error handling
"""

import sys
import os
from io import StringIO
from unittest.mock import Mock, patch, MagicMock
import requests

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers.base import BaseScraper


def test_base_scraper_initialization():
    """Test that BaseScraper initializes with correct attributes"""
    scraper = BaseScraper(rate_limit_delay=2.0)
    
    assert scraper.rate_limit_delay == 2.0, f"Rate limit should be 2.0, got {scraper.rate_limit_delay}"
    assert scraper.session is not None, "Session should be initialized"
    assert scraper.headers is not None, "Headers should be initialized"
    assert 'User-Agent' in scraper.headers, "Headers should contain User-Agent"
    
    scraper.close()
    print(f"✓ test_base_scraper_initialization PASSED")


def test_base_scraper_default_rate_limit():
    """Test that default rate limit is 2.0 seconds"""
    scraper = BaseScraper()  # No parameter
    
    assert scraper.rate_limit_delay == 2.0, f"Default rate limit should be 2.0, got {scraper.rate_limit_delay}"
    
    scraper.close()
    print(f"✓ test_base_scraper_default_rate_limit PASSED")


def test_base_scraper_custom_rate_limit():
    """Test that custom rate limit can be set"""
    scraper = BaseScraper(rate_limit_delay=5.0)
    
    assert scraper.rate_limit_delay == 5.0, f"Rate limit should be 5.0, got {scraper.rate_limit_delay}"
    
    scraper.close()
    print(f"✓ test_base_scraper_custom_rate_limit PASSED")


def test_base_scraper_headers():
    """Test that User-Agent header is present"""
    scraper = BaseScraper()
    
    assert 'User-Agent' in scraper.headers, "Headers should contain User-Agent"
    assert 'Mozilla' in scraper.headers['User-Agent'], "User-Agent should look like a browser"
    assert 'Accept' in scraper.headers, "Headers should contain Accept"
    assert 'Accept-Language' in scraper.headers, "Headers should contain Accept-Language"
    
    scraper.close()
    print(f"✓ test_base_scraper_headers PASSED")


def test_close_method():
    """Test that close() method works without error"""
    scraper = BaseScraper()
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        scraper.close()
        output = sys.stdout.getvalue()
        
        assert 'closed' in output.lower(), "Output should mention closing"
        
        print(f"✓ test_close_method PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_context_manager_enter():
    """Test that __enter__ returns self"""
    scraper = BaseScraper()
    
    result = scraper.__enter__()
    
    assert result is scraper, "__enter__ should return self"
    
    scraper.close()
    print(f"✓ test_context_manager_enter PASSED")


def test_context_manager_exit():
    """Test that __exit__ closes the session"""
    scraper = BaseScraper()
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        scraper.__exit__(None, None, None)
        output = sys.stdout.getvalue()
        
        assert 'closed' in output.lower(), "Should close session"
        
        print(f"✓ test_context_manager_exit PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


def test_context_manager_with_statement():
    """Test using BaseScraper with 'with' statement"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        with BaseScraper() as scraper:
            assert scraper is not None, "Scraper should be initialized in with block"
            assert scraper.session is not None, "Session should exist"
        
        output = sys.stdout.getvalue()
        assert 'closed' in output.lower(), "Should close when exiting with block"
        
        print(f"✓ test_context_manager_with_statement PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_success_200(mock_sleep, mock_get):
    """Test successful fetch with 200 status code"""
    # Mock the response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test Content</body></html>"
    mock_get.return_value = mock_response
    
    scraper = BaseScraper(rate_limit_delay=2.0)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result == "<html><body>Test Content</body></html>", "Should return HTML content"
        assert "fetching" in output, f"Should log fetching, got: {output}"
        assert "Succesfully fetched" in output, f"Should log success, got: {output}"
        
        # Verify rate limit was applied
        mock_sleep.assert_called_once_with(2.0)
        
        print(f"✓ test_fetch_success_200 PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_rate_limited_429(mock_sleep, mock_get):
    """Test fetch when rate limited (429 status)"""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_get.return_value = mock_response
    
    scraper = BaseScraper(rate_limit_delay=2.0)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on 429"
        assert "429" in output, f"Should mention 429 status, got: {output}"
        assert "rate limited" in output, f"Should mention rate limiting, got: {output}"
        
        print(f"✓ test_fetch_rate_limited_429 PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_not_found_404(mock_sleep, mock_get):
    """Test fetch when page not found (404 status)"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com/notfound")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on 404"
        assert "404" in output, f"Should mention 404 status, got: {output}"
        assert "page not found" in output, f"Should mention page not found, got: {output}"
        
        print(f"✓ test_fetch_not_found_404 PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_other_status_code(mock_sleep, mock_get):
    """Test fetch with other error status codes"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        
        assert result is None, "Should return None on 500"
        assert "500" in output, "Should mention 500 status"
        
        print(f"✓ test_fetch_other_status_code PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_timeout(mock_sleep, mock_get):
    """Test fetch when request times out"""
    # Mock a timeout exception
    mock_get.side_effect = requests.exceptions.Timeout()
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on timeout"
        assert "Timeout" in output, f"Should mention timeout, got: {output}"
        assert "10 seconds" in output, f"Should mention 10 second timeout, got: {output}"
        
        print(f"✓ test_fetch_timeout PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_connection_error(mock_sleep, mock_get):
    """Test fetch when connection fails"""
    # Mock a connection error
    mock_get.side_effect = requests.exceptions.ConnectionError()
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on connection error"
        assert "Connection Error" in output, f"Should mention connection error, got: {output}"
        
        print(f"✓ test_fetch_connection_error PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_generic_request_exception(mock_sleep, mock_get):
    """Test fetch with generic RequestException"""
    mock_get.side_effect = requests.exceptions.RequestException("Generic error")
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on RequestException"
        assert "Request Error" in output, f"Should mention request error, got: {output}"
        
        print(f"✓ test_fetch_generic_request_exception PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_unexpected_exception(mock_sleep, mock_get):
    """Test fetch with unexpected exception"""
    mock_get.side_effect = Exception("Unexpected error")
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        result = scraper.fetch("https://example.com")
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert result is None, "Should return None on unexpected error"
        assert "Unexpected error" in output, f"Should mention unexpected error, got: {output}"
        
        print(f"✓ test_fetch_unexpected_exception PASSED")
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_respects_rate_limit_delay(mock_sleep, mock_get):
    """Test that rate limit delay is actually applied"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Content"
    mock_get.return_value = mock_response
    
    scraper = BaseScraper(rate_limit_delay=3.5)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        scraper.fetch("https://example.com")
        
        # Verify sleep was called with correct delay
        mock_sleep.assert_called_once_with(3.5)
        
        print(f"✓ test_fetch_respects_rate_limit_delay PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_uses_correct_timeout(mock_sleep, mock_get):
    """Test that fetch uses 10 second timeout"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Content"
    mock_get.return_value = mock_response
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        scraper.fetch("https://example.com")
        
        # Verify get was called with timeout=10
        call_args = mock_get.call_args
        assert call_args[1]['timeout'] == 10, "Should use 10 second timeout"
        
        print(f"✓ test_fetch_uses_correct_timeout PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout
        scraper.close()


@patch('scrapers.base.requests.Session.get')
@patch('scrapers.base.time.sleep')
def test_fetch_passes_headers(mock_sleep, mock_get):
    """Test that fetch passes headers in request"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Content"
    mock_get.return_value = mock_response
    
    scraper = BaseScraper()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        scraper.fetch("https://example.com")
        
        # Verify headers were passed
        call_args = mock_get.call_args
        assert 'headers' in call_args[1], "Should pass headers"
        assert call_args[1]['headers'] == scraper.headers, "Should use scraper headers"
        
        print(f"✓ test_fetch_passes_headers PASSED", file=sys.stderr)
    finally:
        sys.stdout = old_stdout
        scraper.close()


def run_all_tests():
    """Run all base scraper tests"""
    print("\n" + "="*60)
    print("RUNNING BASE SCRAPER TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_base_scraper_initialization,
        test_base_scraper_default_rate_limit,
        test_base_scraper_custom_rate_limit,
        test_base_scraper_headers,
        test_close_method,
        test_context_manager_enter,
        test_context_manager_exit,
        test_context_manager_with_statement,
        test_fetch_success_200,
        test_fetch_rate_limited_429,
        test_fetch_not_found_404,
        test_fetch_other_status_code,
        test_fetch_timeout,
        test_fetch_connection_error,
        test_fetch_generic_request_exception,
        test_fetch_unexpected_exception,
        test_fetch_respects_rate_limit_delay,
        test_fetch_uses_correct_timeout,
        test_fetch_passes_headers
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