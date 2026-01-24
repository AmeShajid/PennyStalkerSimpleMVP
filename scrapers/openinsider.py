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
# URLs use {fd} as placeholder for filing days: 14 for 2 weeks, 30 for 1 month
options_dictionary = {
    # these options need a timeframe
    'a': {
        'name': 'Latest Cluster Buys',
        'url': 'http://openinsider.com/screener?s=&o=&pl=3&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=6&daysago=&xp=1&vl=25&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=2&nfl=&nfh=&nil=2&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'b': {
        'name': 'Latest Penny Stock Buys',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=5&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=25&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'c': {
        'name': 'Latest Insider Trading (all filings)',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'd': {
        'name': 'Latest Insider Purchases',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'e': {
        'name': 'Latest Insider Purchases $25k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=25&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'f': {
        'name': 'Latest Officer Purchases $25k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=25&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=2&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'g': {
        'name': 'Latest CEO/CFO Purchases $25k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=25&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=1&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'h': {
        'name': 'Latest Insider Sales',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'i': {
        'name': 'Latest Insider Sales $100k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=100&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'j': {
        'name': 'Latest Officer Sales $100k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=100&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=2&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    'k': {
        'name': 'Latest CEO/CFO Sales $100k+',
        'url': 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd={fd}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=100&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=1&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1',
        'needs_timeframe': True
    },
    
    # Don't need timeframe
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

    #this will build the url for the scan
    def build_url(self) -> str:
        """
        Takes the base URL from config and replaces {fd} placeholder with days
        
        Returns:
            str: Complete URL to scrape
        """
        #first get the irl 
        url = self.option["url"]

        #if the scan needs a tf replace fd with timeframe
        if self.option["needs_timeframe"] and self.timeframe:
            #we need to have our map
            days_dict = {
                "2weeks":14, 
                "month": 30
            }

            #get the num of dayus for the tf
            days = days_dict.get(self.timeframe, 14)

            #replcae fd with the number of dayus
            url = url.replace("{fd}", str(days))

        return url 
    
    #