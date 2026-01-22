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
        #this is how many seconds we wait between req
        self.rate_limit_delay = rate_limit_delay

        #creaet the req sessions 
        self.session = requests.Session()

        #setting up headers for the actual browser, also headers are extra info sent with our http req
        #this also helps with not getting blocked as a bot
        self.headers = {
            #first the user agent this is telling them we are chrome running on a windows computer 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            #The accept is telling the server we accept html pages and related web formats with what we put
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #This tells the server we prefor englihs
            'Accept-Language': 'en-US,en;q=0.5',
            #this tell sthe server to keep the connection open 
            'Connection': 'keep-alive',
        }

        #Retry strategy is basically if a request fail;s it automatically tries again based on our factors
        retry_strategy = Retry( 
            #This means it tries up to a toal of 3 times after our first try that failed
            total = 3, 
            #this controls how long we wait between tries, so first try is wait 1 sec then long then longer
            backoff_factor= 1, 
            #These are HTTP status codes that trigger retries.
                #What each one means:
                #429 = “Too many requests” (rate limited)
                #500 = server error (server is broken)
                #502 = bad gateway (server connection issue)
                #503 = service unavailable (server overloaded/down)
                #504 = gateway timeout (server too slow)
            status_forcelist=[429, 500, 502, 503, 504],
            #this tells us to only try get request because post can cause some duplicate issues
            allowed_methods= ["GET"]
        )

        #this is attaching the retry to our session
        #basically says use this retry for req
        adapater = HTTPAdapter(max_retries=retry_strategy)
        #these two say for every url starting with http use the above adaptor
        #ALSO look its not the same its http and https 
        self.session.mount("http://", adapater)
        self.session.mount("https://", adapater)

    #fetch a url with our rate limit and also debugging logs
    def fetch(self, url : str) -> str:
        """
        Args:
            url (str): The URL to fetch
            
        Returns:
            str: HTML content of the page, or None if request failed
        """
        #first print log of what we are fetching
        print(f"fetching {url}")
        #wait couple before sending next req
        time.sleep(self.rate_limit_delay)

        #try and except to catch proper errosr
        try: 
            #start our get req with our headers and timeout
            #get url, for headers use the self headers, and wait 10 sec for a response
            requests = self.session.get(url, headers=self.headers, timeout=10)

            #if req was succesfull (200)
            if requests.status_code == 200:
                print ("Succesfully fetched")
                #return what we fetched the html
                return requests.text
            #elif we failed and its either 429 or 404
            elif requests.status_code == 429:
                #too many req at once we are being rate limited
                print("Failed status code 429 - rate limited")
                print("Increase rate limit or wait")
                return None 
            elif requests.status_code == 404: 
                print("Failed status code 404 - page not found")
                return None
            #else its some other error
            else:
                print(f"Failed status code {requests.status_code}")
                return None 
        
        #if req take too long (which means over 10 sec)
        except requests.exceptions.Timeout:
            # Request took too long (exceeded 10 second timeout)
            print("Timeout after 10 seconds - Server took too long to respond")
            return None
        
        #Could not connect to the server
        except requests.exceptions.ConnectionError:
            print("Connection Error - Could not connect to server")
            print("Check your internet connection or if the URL is correct")
            return None
        
        # Some other request error
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
            return None
        #Unexpected error
        except Exception as e:
            print(f"Unexpected error while fetching: {str(e)}")
            return None

        
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

