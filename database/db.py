"""
This file is our sqlite connection
This connects to the database, creates tables, and handles transactions 
"""
#first import sqllite because thats our storage
import sqlite3
#second import os because we are going to be creating folders
import os
#thrid import our schemas from models.py
from .models import ALL_SCHEMAS

class Database:
    """
    This is going to manage our connection to Sqlite and intialize it
    This class:
        connects to teh sqllite db file
        creates tables if they dont exist
        provides methods to execute queries
        proper closing connections
    """
    def __init__(self, db_path: str = "data/insiderscanner.db"):
        """
        Initalizing connection 
        Arg:
            db_path = Path to our sql lite db file
        """
        #store the db path
        self.db_path = db_path

        #get the directory path from the full file path
        db_dir = os.path.dirname(db_path)

        #if dir path is not empty (file in a folder)
        if db_path:
            #create the dir if it doesn't exist
            #exist_ok=True means dont error if it already exists
            os.makedirs(db_dir, exist_ok=True)

        #connect to the sqllite db create file if it doesn't exist
        # check_same_thread=False allows use from different threads (safer)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        
        # Set row factory to return rows as dictionaries (easier to work with)
        # Without this: row is tuple like (1, 'LSAK', 'Lesaka Technologies')
        # With this: row is dict like {'id': 1, 'ticker': 'LSAK', 'company_name': 'Lesaka Technologies'}
        self.connection.row_factory = sqlite3.Row

        #the cursor object is used to execute sql commanbds
        self.cursor = self.connection.cursor()

        #initalize the schema creates tables if tehy dont exist
        self.initialize_schema()

    #create all tables and index if they dont exist
    def initialize_schema(self):
        """
        This runs when the db connection is just created 

        """
        #iterate through each schema in models
        for schema in ALL_SCHEMAS:
            #executre teh create table or index statement 
            self.cursor.execute(schema)
        #save changes
        self.connection.commit()
    
    #this will execute one sql query 
    def execute(self, query: str, params: tuple = ()): 
        """
        Args:
            query: SQL statement to execute ( "SELECT * FROM insider_transactions")
            params: Parameters for the query (used with ? placeholders)
            
        Returns:
            Cursor object with results
        """
        #this will execute the sql query with params 
        #using ? placeholders to prevent sql attacks for future
        return self.cursor.execute(query, params)
    

    #this will execute teh same query multiple times with diff params
    def executemany(self, query: str, params_list: list):
        """
        Args:
            query: SQL statement to execute
            params_list: List of parameter tuples
        """
        #execture the query once for each set of paramets
        return self.cursor.executemany(query, params_list)

    #this will save all changes to the db file
    def commit(self):
        """
        Changes are not permanent until commit() is called.
        Think of it like clicking "Save" button.
        """
        #commits everything
        self.connection.commit()
    
    #Undo all changes since last commit.
    def rollback(self):
        """
        when something goes wrong and you want to cancel changes.
        """
        #undo all changes since last commit
        self.connection.rollback()
    
    #Close the database connection.
    def close(self):
        """
        Always close connections when done to free resources.
        """
        # Close the database connection
        self.connection.close()
    



    ## KEY UNDERSTANDING
        #Enter and exit are both dunder bnecause they let us use enter and exit with the WITH key word example I put below
    #Runs at the start of the with block and returns the db object
    #also lets us use the WITH statement 
    def __enter__(self):
        """
        Allows:
            with Database() as db:
                db.execute("SELECT ...")
            # Connection automatically closed
        
        Returns:
            Self (the Database instance)
        """
        # Return self so 'with' statement can use this instance
        return self
    
    #this is for exiting after entering
    #Automatically closes connection and commits/rollbacks as needed.
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Args:
            exc_type: Exception type (if error occurred)
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        
        # If an exception occurred in the 'with' block
        if exc_type is not None:
            # Rollback any uncommitted changes (cancel them)
            self.rollback()
        else:
            #commit changes (save them)
            self.commit()
        
        # Always close the connection
        self.close()