"""
Base is a parent class for all the other scrapers, instead of writing the same http logic multiple times we do it once.
So it has shared HTTP functionality for all scrapers.
It handles making web requests safely with headers, rate limiting,
error handling, and session cleanup so the scrapers can focus on parsing data.
"""

#to handle making http req
import requests
#to handle rate limiting
import time
#these two are used for automatic retires
    #if a req fails temp, it retries automatically without giving up
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class BaseScraper:
    """
    Attributes:
        session (requests.Session) - HTTP session for making requests
        rate_limit_delay (float) - Seconds to wait between requests
        headers (dict) - HTTP headers to include in requests
    """
    #initialize the base scraper with a session and also rate limitng
    def __init__(self, rate_limit_delay : float = 2.0):
        #store the rate limit in a var
        self.rate_limit_delay = rate_limit_delay

        #creaet the req sessions 
        self.session = requests.Session()

        #setting up headers for the actual browser
        #this also helps with not getting blocked as a bot
        self.headers = {

        }

    def fetch():
        pass 
    
    #this is just to close the session
    def close(self): 
        """
        Close the session and clean up resources
        Always call this when done with the scraper
        """
        self.session.close()
        print("Session Closed")

    #dunder method so we can use WITH
    def __enter__(self):
        """        
        Returns:
            self (BaseScraper instance)
            
        Example:
            with BaseScraper() as scraper:
                html = scraper.fetch("https://")
            Session automatically closed when exiting with 
        """
        return self
    
    #dunder for exiting the with and we also just need to ahve all 3 exc
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - automatically closes session.
        """
        # Always close the session when exiting the with
        self.close()

