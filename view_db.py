#Lets us see whats in the db 


# Import sqllite so we can grab from db
import sqlite3

# conenct to OUR db
conn = sqlite3.connect('data/pennystalker.db')

#each row needs to be a dict not tuple
#we will do (row['ticker']) instead of index
conn.row_factory = sqlite3.Row

#Cursor object to run SQL commands
cursor = conn.cursor()

#Now getting a list of tables in db
#First list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# gewt all table names into a list
tables = cursor.fetchall()

#Print everything 
#"="*60 thats for broders
print("\n" + "="*60)
print("DATABASE CONTENTS")
print("="*60 + "\n")



#iterate through tables
for table in tables:
    # Get table name from the row dict
    table_name = table['name']
    
    # Select ALL rows from the current table
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # get all rows from this table
    rows = cursor.fetchall()
    
    # Print table name
    print(f"Table: {table_name}")
    
    # Print number of rows in table
    print(f"Rows: {len(rows)}")
    
    # If table has at least one row
    if rows:
        # Print column names using keys from the first row
        print(f"Columns: {list(rows[0].keys())}")
        print()
        
        # Loop through the first 5 rows only
        for i, row in enumerate(rows[:5], 1):
            # Convert sqlite Row object to normal dictionary and print it
            print(f"  Row {i}: {dict(row)}")
        
        # If there are more than 5 rows, mention how many are hidden
        if len(rows) > 5:
            print(f"{len(rows) - 5} more rows")
    print()

#close connection
conn.close()

# Print end border
print("="*60)
