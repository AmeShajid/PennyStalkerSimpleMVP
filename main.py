"""
1. Initializes everythign 
2. Grab user input
3. Get data from opensinder 
4. Deduplicate transactions 
5. display results
6. record scan histryo 
7. clean up

everythign in this code will be in try and except because we are scarping information from a web 
we need eerythign to work so even if somethign fails we wil know whats happening, and not everythign will immediatlery crash
"""

#load everything 
from utils.display import TerminalDisplay
from utils.hash_utils import generate_transaction_hash
from database.db import Database
from database.repository import TransactionRepository, ScanHistoryRepository
from scrapers.openinsider import OpenInsiderScraper, options_dictionary
import sys
import os
from dotenv import load_dotenv


#load everythign from env also validate things keeping things prof
def load_env():
    """    
    Returns:
        dict: with keys DB_PATH, SCRAPER_RATE_LIMIT, REQUEST_TIMEOUT
        
    Raises:
        ValueError: If nums is invalid
    """
    #first load from env
    load_dotenv()

    try:
        #grab path, limit, and timeout 
        db_path = os.getenv("DB_PATH", "data/pennystalker.db")
        rate_limit = float(os.getenv("SCRAPER_RATE_LIMIT", "2.0"))
        timeout = int(os.getenv("REQUEST_TIMEOUT", "10"))

        #valid and make sure the nums are valid
        if rate_limit < 0:
            raise ValueError("SCRAPER_RATE_LIMIT must be >= 0")
        if timeout <= 0:
            raise ValueError("REQUEST_TIMEOUT must be > 0")
        
        #if its valid return in a dict
        return { 
            'DB_PATH': db_path,
            'SCRAPER_RATE_LIMIT': rate_limit,
            'REQUEST_TIMEOUT': timeout
        }
    except ValueError as e: 
        raise ValueError(f"ENV error : {e}") 

#so now we can try pulling from above
try: 
    env_file_stuff = load_env()
    DB_PATH = env_file_stuff['DB_PATH']
    SCRAPER_RATE_LIMIT = env_file_stuff['SCRAPER_RATE_LIMIT']
    REQUEST_TIMEOUT = env_file_stuff['REQUEST_TIMEOUT']
except ValueError as e:
    print(f"This failed: {e}")
    sys.exit(1)


#we need to intialize all of our stuff we will use 
def initalize_erverything(): 
    """    
    Returns:
        tuple: (display, db, transaction_repo, scan_history_repo)
        
    Raises:
        Exception: If database connection fails (fatal)
    """
    try: 
        #first lets start up the program 
        display = TerminalDisplay() 

        #start up db 
        #if this fails nothign workings lol 
        try: 
            db = Database(DB_PATH) 
        except Exception as e:
            display.display_error(f"Database Connection Failed : {e}")
            display.display_error("Cant continue without this rip")
            sys.exit(1)
        
        #startup repos
        transaction_repo = TransactionRepository(db) 
        scan_history_repo = ScanHistoryRepository(db) 

        return display, db, transaction_repo, scan_history_repo 
    except Exception as e: 
        print(f"Intializaion failed: {e}") 
        sys.exit(1) 


#nwo we need to get the scan tyhpe and time frame from user
def get_user_choice(display: TerminalDisplay): 
    """
    Returns:
        tuple: (choice, scan_name, timeframe)
    """
    #first show the menuy 
    choice = display.show_menu() 
    scan_name = options_dictionary[choice]["name"] 

    #now we need to check if the chocie they have needs a tf
    if options_dictionary[choice]["needs_timeframe"]:
        timeframe = display.show_timeframe_menu() 
    else:
        timeframe = None 

    return choice, scan_name, timeframe 


#Now here comes the scraping 
def scrape_data(choice: str, timeframe: str, display: TerminalDisplay): 
    """    
    Args:
        choice: Options a-q
        timeframe: "2weeks" or "month"
        display: TerminalDisplay instance
        
    Returns:
        tuple: (scraper, transactions)
               transactions is None if scrape failed
               transactions is [] if no data found
               transactions is [dicts] if success
    """
    try: 
        #intialziign scraper for scan type
        scraper = OpenInsiderScraper(choice, timeframe, rate_limit_delay=SCRAPER_RATE_LIMIT)
        #show its working
        print("Fetching from OpenInsider")
        #scarpe website
        transactions = scraper.scrape()

        #check if it failed
        if transactions is None: 
            display.display_error("Failed to get from OpenInsider.")
            display.display_error("The site may be down, or your connection timed out.")
            display.display_error("Try again later or check your internet connection.")
            return scraper, None
        
        #if it worked
        print(f"Parsed {len(transactions)} transaction from HTML")
        return scraper, transactions
    
    except Exception as e:
        display.display_error(f"Scraper Error : {e}")
        return None, None
    

#so now processing and hashing these transaction bascially deduplicating and inserting
def process_transactions(transactions: list, transaction_repo: TransactionRepository, display: TerminalDisplay):
    """
    Loop through transactions:
    - Generate hash
    - Check if already in database
    - If new: insert and track
    - If duplicate: skip
    
    Returns:
        dict: {
            'new_transactions': [list of new ones],
            'num_duplicates': count,
            'num_insert_success': count,
            'num_insert_failed': count,
            'highest_value': float
        }
    """
    new_transactions = []
    num_duplicates = 0
    num_insert_success = 0
    num_insert_failed = 0
    highest_value = 0
    
    # Show progress
    print(f"Processing {len(transactions)} transactions")
    
    # Loop through each transaction
    for transaction in transactions:
        #Generate  hash id
        hash_value = generate_transaction_hash(transaction)
        transaction['transaction_hash'] = hash_value
        
        # Check if transaction already exists
        if transaction_repo.transaction_exists(hash_value):
            num_duplicates += 1
            continue
        
        #NEW transaction
        try:
            # Insert into database
            transaction_repo.insert_transaction(transaction)
            num_insert_success += 1
            
            # Track for display
            new_transactions.append(transaction)
            
            # Track highest value
            if transaction['value'] > highest_value:
                highest_value = transaction['value']
        
        except Exception as e:
            # If insert fails, skip transaction and continue
            print(f"Failed to insert {transaction.get('ticker', 'UNKNOWN')}: {e}")
            num_insert_failed += 1
    
    # Showprocessing
    print(f"Done: {num_insert_success} new, {num_duplicates} duplicates")
    if num_insert_failed > 0:
        print(f"{num_insert_failed} transactions failed to insert)")
    
    return {
        'new_transactions': new_transactions,
        'num_duplicates': num_duplicates,
        'num_insert_success': num_insert_success,
        'num_insert_failed': num_insert_failed,
        'highest_value': highest_value
    }


#so now we need to disply results
def display_results(display: TerminalDisplay, process_results: dict, scan_name: str, total_scraped: int):
    """
    Args:
        display: TerminalDisplay instance
        process_results: Dict from process_transactions()
        scan_name: Name of the scan
        total_scraped: Total transactions scraped
    """
    num_insert_success = process_results['num_insert_success']
    num_duplicates = process_results['num_duplicates']
    highest_value = process_results['highest_value']
    new_transactions = process_results['new_transactions']
    
    # Check if we found any new transactions
    if num_insert_success == 0:
        display.display_no_new_transactions()
        return
    
    # Display header
    display.display_scan_header(scan_name)
    
    # Sort by value
    def get_transaction_value(transaction):
        return transaction['value']
    
    new_transactions.sort(key=get_transaction_value, reverse=True)
    
    # Display each transaction with rank
    for idx, transaction in enumerate(new_transactions, start=1):
        display.display_transaction(transaction, rank=idx)
    
    # Display
    display.display_summary(
        total_scraped=total_scraped,
        num_new=num_insert_success,
        num_duplicates=num_duplicates,
        highest_value=highest_value
    )


#now we need to recrods the scan and insert this 
def record_scan_history(scan_history_repo: ScanHistoryRepository, scan_name: str, total_scraped: int, num_insert_success: int, num_duplicates: int, highest_value: float):
    try:
        scan_history_repo.insert_scan(
            scan_type=scan_name,
            num_transactions=total_scraped,
            num_new=num_insert_success, 
            num_duplicates=num_duplicates,
            highest_value=highest_value
        )
    except Exception as e:
        print(f"Failed to record scan history: {e}")


#we need to close everything 
def cleanup_resources(scraper, db):
    if scraper:
        try:
            scraper.close()
        except:
            pass
    
    if db:
        try:
            db.close()
        except:
            pass
    
    print("Done")


#Main 
def main():
    """
    1. Initialize resources
    2. Get user input
    3. Scrape data
    4. Deduplicate & insert
    5. Display results
    6. Record history
    7. Cleanup
    """
    display = None
    db = None
    scraper = None
    
    try:
        #part 1 initialize
        display, db, transaction_repo, scan_history_repo = initalize_erverything()
        
        #inpout
        choice, scan_name, timeframe = get_user_choice(display)
        
        #scrape
        scraper, transactions = scrape_data(choice, timeframe, display)
        
        #if failed except 
        if transactions is None:
            return
        
        # If no transactions found reutrn 
        if len(transactions) == 0:
            display.display_no_new_transactions()
            return
        
        #insert and hash id 
        process_results = process_transactions(transactions, transaction_repo, display)
        
        #diaply 
        display_results(display, process_results, scan_name, len(transactions))
        
        #record scan 
        record_scan_history(
            scan_history_repo,
            scan_name,
            total_scraped=len(transactions),
            num_insert_success=process_results['num_insert_success'],
            num_duplicates=process_results['num_duplicates'],
            highest_value=process_results['highest_value']
        )
    
    except KeyboardInterrupt:
        #ctrl + c is quit 
        print("\n Scan cancelled by user.")
    
    except Exception as e:
        # Unexpected error
        if display:
            display.display_error(f"Unexpected error: {e}")
        else:
            print(f"Unexpected error: {e}")
    
    finally:
        cleanup_resources(scraper, db)

if __name__ == "__main__":
    main()