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
    
    #this is going to the main scrapnng methjod
    def scrape(self) -> list: 
        """    
        Returns:
            list: List of transaction dictionaries
        """

        #get the full url 
        url = self.build_url() 
        #print the curr url 
        print(f"Built url: {url}")

        #we need to get the html using our fetch
        html = self.fetch(url) 

        #if the fetch failed just return emtpy list
        if html is None:
            print("Failed to fetch html, returning empty list")
            return [] 
        
        #parse html and get transactison
        transactions = self.parse_html(html) 
        print(f"Parsed {len(transactions)} transactions from html")
        return transactions 
    
    #prase the html and get transactionsdata from table 
    def parse_html(self, html: str) -> list : 
        """
        Uses BeautifulSoup to find the transaction table and loop through rows
        
        Args:
            html (str): HTML content of the page
            
        Returns:
            list: List of transaction dictionaries
        """
        #create a bs object to parse html 
        soup = BeautifulSoup(html, "html.parser")

        #find the main table elemtn 
        #we do this because it uses a table 
        table = soup.find("table")

        #if no table is found return empty list
        if table is None: 
            print("No table is found in HTML")
            return [] 

        #get the rows from table 
        rows = table.find_all("tr")
        print(f"Found {len(rows)} in table")

        # Get the first row to extract headers
        if len(rows) == 0:
            print("No rows found in table")
            return []

        # Extract header row (first row with <th> elements)
        header_row = rows[0]
        column_dict = self.build_column_dict(header_row)

        # If we couldn't build column dict, return empty list
        if column_dict is None or len(column_dict) == 0:
            print("Could not get column headers from table")
            return []
        
        print(f"Column dict: {column_dict}")

        #we need a list to stroe all transactions 
        transactions = [] 

        #iterate through rows starting from 1 because thats header
        for row in rows[1:]: 
            #get the calls = td in the row 
            tds = row.find_all("td") 
            #skip if the row has no cells prolly header or empty
            if len(tds) == 0: 
                continue 
            #skip if the row doesnt have enough cells because we want all of them 
            if len(tds) < len(column_dict): 
                continue 
            #get the trans data from row
            #it also create it into a dict
            transaction = self.extract_transaction_row(tds, column_dict) 

            #if extracting was good add it to list 
            if transaction is not None: 
                #this tags every trans with what type of scan name it is
                transaction["scan_type"] = self.scan_name 
                #append to our transactison 
                transactions.append(transaction)
        return transactions
    
    #build a dict of colum names to index from header row
    def build_column_dict(self, header_row) -> dict : 
        """
        Reads the <th> elements from the header row and creates a dictionary
        that maps column names to their position in the table
        
        Args:
            header_row: The <tr> element containing headers
            
        Returns:
            dict: Mapping of column name to index (e.g., {'Ticker': 2, 'Price': 8})
        """
        #get all the haeder cells 
        header_cells = header_row.find_all("th") 
        #if no headers found return dmepty dict 
        if len(header_cells) == 0: 
            return {} 
        
        #create column dict 
        column_dict = {}

        #iterate with enumerate 
        for index, header_cell in enumerate(header_cells): 
            #get the text from header
            header_text = header_cell.get_text(strip = True) 
            #store col name and index 
            column_dict[header_text] = index 
        return column_dict
    
    #get transaction data from a single table row
    def extract_transaction_row(self, tds: list, column_dict: dict) -> dict:
        """
        Uses column_dict to find the correct index for each field
        This makes the scraper dynamic it adapts if OpenInsider changes column order
        
        Args:
            tds (list): List of <td> elements from a row
            column_dict (dict): Mapping of column names to indexes
            
        Returns:
            dict: Transaction dictionary with all fields, or None if we failed
        """
        try:
            # get data using column_dict to find the correct column index
            #every column follows
            #get the text
            #if it doesnt exist
                #retunr None
            #if it does, get this text and strip it

            #for the ones with currency and other symbols we are just cleaning the line and thats it getting rid of useless shi
            
            # Get Filing Date
            filing_date_index = column_dict.get('Filing Date')
            if filing_date_index is None:
                return None
            filing_date = tds[filing_date_index].get_text(strip=True)
            
            # Get Trade Date
            trade_date_index = column_dict.get('Trade Date')
            if trade_date_index is None:
                return None
            trade_date = tds[trade_date_index].get_text(strip=True)
            
            # Get Ticker
            ticker_index = column_dict.get('Ticker')
            if ticker_index is None:
                return None
            ticker = tds[ticker_index].get_text(strip=True)
            
            # Get Company Name
            company_name_index = column_dict.get('Company Name')
            if company_name_index is None:
                return None
            company_name = tds[company_name_index].get_text(strip=True)
            
            # Get Insider Name
            insider_name_index = column_dict.get('Insider Name')
            if insider_name_index is None:
                return None
            insider_name = tds[insider_name_index].get_text(strip=True)
            
            # Get Insider Title
            title_index = column_dict.get('Title')
            if title_index is None:
                return None
            insider_title = tds[title_index].get_text(strip=True)
            
            # Get Trade Type
            trade_type_index = column_dict.get('Trade Type')
            if trade_type_index is None:
                return None
            trade_type = tds[trade_type_index].get_text(strip=True)
            
            # Get Price
            price_index = column_dict.get('Price')
            if price_index is None:
                return None
            price_str = tds[price_index].get_text(strip=True)
            price = self.clean_number(price_str, is_currency=True)
            
            # Get Quantity
            qty_index = column_dict.get('Qty')
            if qty_index is None:
                return None
            quantity_str = tds[qty_index].get_text(strip=True)
            quantity = self.clean_number(quantity_str, is_integer=True)
            
            # Get shares owned
            owned_index = column_dict.get('Owned')
            if owned_index is None:
                return None
            owned_str = tds[owned_index].get_text(strip=True)
            owned = self.clean_number(owned_str, is_integer=True)
            
            # Get delta Own Value (contains both percentage and dollar value)
            delta_value_index = column_dict.get('ΔOwn Value')
            if delta_value_index is None:
                return None
            delta_value_text = tds[delta_value_index].get_text(strip=True)
            
            # Extract percentage and value from delta iwn Value column
            delta_own_pct = self.extract_percentage(delta_value_text)
            value = self.extract_currency(delta_value_text)
            
            # Create transaction dictionary with all fields
            transaction = {
                'ticker': ticker,
                'company_name': company_name,
                'filing_date': filing_date,
                'trade_date': trade_date,
                'insider_name': insider_name,
                'insider_title': insider_title,
                'trade_type': trade_type,
                'price': price,
                'quantity': quantity,
                'owned': owned,
                'delta_own_pct': delta_own_pct,
                'value': value
            }
            
            return transaction
        
        except Exception as e:
            # If something goes wrong extracting this row, log it and return None
            print(f"Error extracting row: {e}")
            return None
    
    #cleaning a number string and convert to a proper data type
    def clean_number(self, value_str: str, is_currency: bool = False, is_integer: bool = False) -> float:
        """
        Removes currency symbols, commas, and converts to float or int
        
        Args:
            value_str (str): String containing a number ($1,234.56)
            is_currency (bool): If True its a currency and return float
            is_integer (bool): If True return as integer
            
        Returns:
            float or int: Cleaned number
        """
        # Remove spaces
        value_str = value_str.strip()
        
        # Remove currency symbol ($)
        value_str = value_str.replace('$', '')
        
        # Remove commas
        value_str = value_str.replace(',', '')
        
        # Handle "New" value (for shares owned)
        if value_str.lower() == 'new':
            return 0
        
        # Handle empty or invalid values
        if not value_str or value_str == '-':
            return 0
        
        try:
            # Convert to float first
            number = float(value_str)
            
            # If integer requested, convert to int
            if is_integer:
                return int(number)
            
            return number
        
        except ValueError:
            # If conversion fails, return 0
            print(f"Could not convert '{value_str}' to number")
            return 0
    
    #get the percentage from text
    def extract_percentage(self, text: str) -> float:
        """
        Handles formats like "+343%", "-15%"
        
        Args:
            text (str): Text with percentage
            
        Returns:
            float: Percentage value
        """
        # Remove spaces
        text = text.strip()
        
        # Find the % symbol
        percent_index = text.find('%')
        
        if percent_index == -1:
            # No % found, return 0
            return 0.0
        
        # Get text before the % sign
        percent_str = text[:percent_index]
        
        # Remove + and spaces
        percent_str = percent_str.replace('+', '').strip()
        
        try:
            return float(percent_str)
        except ValueError:
            return 0.0
    
    #get currency value from text
    def extract_currency(self, text: str) -> float:
        """        
        Handles formats like "$21,868,640", "-$500,000"
        
        Args:
            text (str): Text containing currency symnbol
            
        Returns:
            float: Currency value (21868640.0)
        """
        # Remove spaces
        text = text.strip()
        
        # Find the $ symbol
        dollar_index = text.find('$')
        
        if dollar_index == -1:
            # No $ found, return 0
            return 0.0
        
        # Get everything after the $ sign
        currency_str = text[dollar_index+1:]
        
        # Use clean_number to handle the rest
        return self.clean_number(currency_str, is_currency=True)