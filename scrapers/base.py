"""
PennyStalker - Base Scraper Class
Shared functionality for all scrapers
"""

import requests
import time
import logging
from typing import Optional
from abc import ABC

from config_files import ScanParameters

# Setup logging
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Base class for all scrapers
    Provides common HTTP functionality, error handling, and rate limiting
    """
    
    def __init__(self):
        """Initialize base scraper with session and settings"""
        
        # Request settings from config
        self.timeout = ScanParameters.REQUEST_TIMEOUT
        self.delay = ScanParameters.REQUEST_DELAY
        
        # Create persistent session for connection pooling
        self.session = requests.Session()
        
        # Default headers (can be overridden by subclasses)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        logger.debug(f"{self.__class__.__name__} initialized")
    
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        Make an HTTP request with error handling and rate limiting
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional arguments passed to requests
            
        Returns:
            Response object or None if request failed
        """
        
        # Rate limiting - respect the delay
        time.sleep(self.delay)
        
        try:
            # Set timeout if not provided
            if 'timeout' not in kwargs:
                kwargs['timeout'] = self.timeout
            
            # Make request
            if method.upper() == 'GET':
                response = self.session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, **kwargs)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            # Check for HTTP errors
            response.raise_for_status()
            
            logger.debug(f"Request successful: {url} (Status: {response.status_code})")
            return response
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {url}")
            return None
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error requesting {url}: {e}")
            return None
    
    
    def test_connection(self, url: str) -> bool:
        """
        Test if a URL is accessible
        
        Args:
            url: URL to test
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    
    def close(self):
        """Close the session (cleanup)"""
        self.session.close()
        logger.debug(f"{self.__class__.__name__} session closed")
    
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto cleanup"""
        self.close()