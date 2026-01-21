"""
This file will contain all the sql database query methods 
So this will seperate sql quereies from the business logic we have

Classes:
    TransactionRepository = All queries for insider transactions table
    ScanHistoryRespository = All queries for scan history talbe
"""

#import the db we just created from database
from .db import Database

class TransactionRepository:
    """
    This class will handle the database operations for the insider transactions table
    It will have methods for:
        Inserting a transaction 
        Check if transaction already exists
        Search transactions by ticker
        Get the most recent transaction 
    """
    def __init__(self, db: Database):
        #initalizing the database connection
        self.db = db

    #inserting one transaction into the databse
    #If everything goes right it will tell us true or false
    def insert_transaction(self, transaction: dict) -> bool:
        """
        Args:
            transaction: Dictionary with all transaction fields
            
        Returns:
            True if successful, False if failed
        """
        try:
            #sql INSERT statement, also filling with ? for placeholders 
            query = """
                INSERT INTO insider_transactions (
                    ticker, company_name, filing_date, trade_date,
                    insider_name, insider_title, trade_type,
                    price, quantity, owned, delta_own_pct, value,
                    scan_type, transaction_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            # Get values from  dictionary in same order as query
            params = (
                transaction.get('ticker'),
                transaction.get('company_name'),
                transaction.get('filing_date'),
                transaction.get('trade_date'),
                transaction.get('insider_name'),
                transaction.get('insider_title'),
                transaction.get('trade_type'),
                transaction.get('price'),
                transaction.get('quantity'),
                transaction.get('owned'),
                transaction.get('delta_own_pct'),
                transaction.get('value'),
                transaction.get('scan_type'),
                transaction.get('transaction_hash')
            )
        
            #execute the insert statemnt
            self.db.execute(query, params)
            #commit the change
            self.db.commit()
            #if it worked return true
            return True
        except Exception as e:
            #if it failed 
            print(f"Error inserting : {e}")
            return False
        
    #if the transaction with these hash values alreayd exists
    def transaction_exists(self, transaction_hash: str) -> bool:
        """         
        Args:
            transaction_hash: Unique ID (e.g., "LSAK_MazanderaniAli_20251231_9000000")
            
        Returns:
            True if exists, False if new
        """
        #sql query to check if the hash already exists
        query = """
            SELECT 1 FROM insider_transactions 
            WHERE transaction_hash = ?
            LIMIT 1
        """
        #execute the query 
        cursor = self.db.execute(query, (transaction_hash,))
        
        #fetch one result 
        result = cursor.fetchone()

        # If a row was found, return True
        if result != None:
            return True
        else:
            return False
        
    #Get all transactions for a specifric ticker 
    def get_transactions_by_ticker(self, ticker: str) -> str:
        """        
        Args:
            ticker: Stock symbol (e.g., "LSAK")
            
        Returns:
            List of transaction dictionaries (newest first)
        """
        query = """
            SELECT * FROM insider_transactions 
            WHERE ticker = ?
            ORDER BY trade_date DESC
        """

        #execute the query 
        cursor = self.db.execute(query, (ticker, ))

        #fetch all rows
        rows = cursor.fetchall()

        #empty list to store transactions
        transactions = []

        #iterate through 
        for row in rows:
            #convert the row to a dict
            row_dict = dict(row)
            #add dict to list
            transactions.append(row_dict)
        #return transactions 
        return transactions
    
    #to get transactions from N days
    def get_recent_transactions(self, days: int = 30) -> list:
        """
         Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            List of transaction dictionaries sorted by value (highest first)
        """
        #query to get transactions from last N days sorted by value
        query = """
            SELECT * FROM insider_transactions 
            WHERE trade_date >= date('now', '-{} days')
            ORDER BY value DESC
        """.format(days)
        
        # Execute query
        cursor = self.db.execute(query)
        
        # Fetch all results
        rows = cursor.fetchall()
        
        #empty list to store transactions
        transactions = []

        #iterate through 
        for row in rows:
            #convert the row to a dict
            row_dict = dict(row)
            #add dict to list
            transactions.append(row_dict)

        #return transactions 
        return transactions

    #to get all transactions from the database
    def get_all_transactions(self) -> list:
        """        
        Returns:
            List of all transaction dictionaries
        """
        # SQL query to get everything
        query = "SELECT * FROM insider_transactions ORDER BY trade_date DESC"
        
        # Execute query
        cursor = self.db.execute(query)
        
        # Fetch all results
        rows = cursor.fetchall()
        
        #empty list to store transactions
        transactions = []

        #iterate through 
        for row in rows:
            #convert the row to a dict
            row_dict = dict(row)
            #add dict to list
            transactions.append(row_dict)

        #return transactions 
        return transactions

class ScanHistoryRepository:
    """
    Handles all database operations for scan_history table.
    
    methods:
    - Record each scan
    - View scan history
    """

    #initialize repo with db connection
    def __init__(self, db: Database):
        self.db = db
    
    #Recprd the data about the scan we just did
    def insert_scan(self, scan_type: str, num_transactions: int, num_new: int, num_duplicates: int, highest_value: float) -> bool:
        """
        Args:
            scan_type: What was scanned (e.g., "Latest Cluster Buys")
            num_transactions: Total transactions found
            num_new: How many were new
            num_duplicates: How many were already in database
            highest_value: Largest transaction value
            
        Returns:
            True if successful, False if failed
        """
        try:
            #sql insert 
            query = """INSERT INTO scan_history (
                    scan_type, num_transactions, num_new, 
                    num_duplicates, highest_value
                ) VALUES (?, ?, ?, ?, ?)
            """
            
            #get the params
            params = (
                scan_type, 
                num_transactions, 
                num_new, 
                num_duplicates, 
                highest_value
            )

            #execute
            self.db.execute(query, params)

            #commit
            self.db.commit()
            
            #if it worked
            return True
        except Exception as e: 
            #if fail false
            print(f"Error inserting: {e}")
            return False 

    #get the scan history for most recent
    def get_scan_history(self, limit: int=10) -> list: 
        """
        Args:
            limit: Number of scans to return (default: 10)
            
        Returns:
            List of scan dictionaries (newest first)
        """
        #query to get recent scans
        query = """
            SELECT * FROM scan_history 
            ORDER BY scan_timestamp DESC 
            LIMIT ?
        """

        # Execute
        cursor = self.db.execute(query, (limit,))
        
        # Fetch
        rows = cursor.fetchall()

        #empty list to store transactions
        scans = []

        #iterate through 
        for row in rows:
            #convert the row to a dict
            row_dict = dict(row)
            #add dict to list
            scans.append(row_dict)

        #return transactions 
        return scans