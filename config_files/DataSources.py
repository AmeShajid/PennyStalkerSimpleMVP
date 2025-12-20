"""
In this file we are going to have everything related to our key terms and words.
We are going to put all key words in their respectful classes so when we scale its a lot easier to handle
"""
#os so we can actually grab the items
import os
#this is so we can load our env stuff
from dotenv import load_dotenv

#first load our var from .env file
load_dotenv()

#first handling our data sources 
class DataSources:
    #these are going to be our urls 
    STOCKTITAN_NEWS = os.getenv('STOCKTITAN_NEWS_URL', 'https://www.stocktitan.net/news/live.html')
    SEC_SEARCH = os.getenv('SEC_SEARCH_URL', 'https://www.sec.gov/cgi-bin/browse-edgar')
    SEC_BASE = os.getenv('SEC_BASE_URL', 'https://www.sec.gov')