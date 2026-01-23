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
    
    #these topions dont need 
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