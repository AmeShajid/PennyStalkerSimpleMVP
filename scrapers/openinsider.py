"""
This will scrape the insider trading data from the website
IT will fetch the html from the website and parse the transacation dataes

Class structure:
    OpenInsiderScraper
        Inherits from BaseScraper
            Handles opensinsder specific parsing
"""

#import the base 
from scrapers.base import BaseScraper
#import scraper
from bs4 import BeautifulSoup

#first we need a dict with all of our urls and data for EACH option
#Also we are adding a bool sections for the optoins that need a timeframe vs dont
options_dictionary = {
    #these topsion dont need
    'a': {
        'name': 'Latest Cluster Buys',
        'url': 'http://openinsider.com/latest-cluster-buys',
        'needs_timeframe': True
    },
    'b': {
        'name': 'Latest Penny Stock Buys',
        'url': 'http://openinsider.com/latest-penny-stock-buys',
        'needs_timeframe': True
    },
    'c': {
        'name': 'Latest Insider Trading (all filings)',
        'url': 'http://openinsider.com/latest-insider-trading',
        'needs_timeframe': True
    },
    'd': {
        'name': 'Latest Insider Purchases',
        'url': 'http://openinsider.com/insider-purchases',
        'needs_timeframe': True
    },
    'e': {
        'name': 'Latest Insider Purchases $25k+',
        'url': 'http://openinsider.com/latest-insider-purchases-25k',
        'needs_timeframe': True
    },
    'f': {
        'name': 'Latest Officer Purchases $25k+',
        'url': 'http://openinsider.com/latest-officer-purchases-25k',
        'needs_timeframe': True
    },
    'g': {
        'name': 'Latest CEO/CFO Purchases $25k+',
        'url': 'http://openinsider.com/latest-ceo-cfo-purchases-25k',
        'needs_timeframe': True
    },
    'h': {
        'name': 'Latest Insider Sales',
        'url': 'http://openinsider.com/insider-sales',
        'needs_timeframe': True
    },
    'i': {
        'name': 'Latest Insider Sales $100k+',
        'url': 'http://openinsider.com/latest-insider-sales-100k',
        'needs_timeframe': True
    },
    'j': {
        'name': 'Latest Officer Sales $100k+',
        'url': 'http://openinsider.com/latest-officer-sales-100k',
        'needs_timeframe': True
    },
    'k': {
        'name': 'Latest CEO/CFO Sales $100k+',
        'url': 'http://openinsider.com/latest-ceo-cfo-sales-100k',
        'needs_timeframe': True
    },
    
    #these topions do need 
    'l': {
        'name': 'Top Officer Purchases Today',
        'url': 'http://openinsider.com/top-officer-purchases-of-the-day',
        'needs_timeframe': False
    },
    'm': {
        'name': 'Top Officer Purchases Past Week',
        'url': 'http://openinsider.com/top-officer-purchases-of-the-week',
        'needs_timeframe': False
    },
    'n': {
        'name': 'Top Insider Purchases Today',
        'url': 'http://openinsider.com/top-insider-purchases-of-the-day',
        'needs_timeframe': False
    },
    'o': {
        'name': 'Top Insider Purchases Past Week',
        'url': 'http://openinsider.com/top-insider-purchases-of-the-week',
        'needs_timeframe': False
    },
    'p': {
        'name': 'Top Insider Sales Today',
        'url': 'http://openinsider.com/top-insider-sales-of-the-day',
        'needs_timeframe': False
    },
    'q': {
        'name': 'Top Insider Sales Past Week',
        'url': 'http://openinsider.com/top-insider-sales-of-the-week',
        'needs_timeframe': False
    }
}

#the actual class
#This will scrape the insider trading data from the web
class OpenInsiderScraper(BaseScraper):
    #initialzing the scraper
    """
    Args:
        scan_type (str): Option letter (a-q)
        timeframe (str): '2weeks' or 'month'
        rate_limit_delay (float): Seconds to wait between requests
    """
    def __init__(self, scan_type: str, timeframe: str = None, rate_limit_delay: float = 2.0):
        #call the partent constructor 
        super().__init__(rate_limit_delay=rate_limit_delay)
        
        #store both variables so we can use it
        self.scan_type = scan_type
        self.timeframe = timeframe

        #if the scan type not in dict throw an error
        if scan_type not in options_dictionary:
            raise ValueError(f"Invalid option : {scan_type}. Must be a-q")

        #if we pass that, then get the scan type from dict and also the name 
        self.option = options_dictionary[scan_type]
        self.scan_name = self.option["name"]
        