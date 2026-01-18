"""
This file will create unique IDS for insider transactions
Purpose: Prevent showing the same transaction twice

How it works:
    Take transaction data (ticekr, insider, date, value)
    Combine into one unique string
    This is going to be id for the transaction 

Args:
    Transaction : Dictionary with keys
        Ticker 
        insider name
        trade date
        value
Returns:
    string such as "TSLA_ELONMUSK_20250101_900000"

Example:
    transaction = {
        'ticker': 'TSLA',
        'insider_name': 'ELON MUSK',
        'trade_date': '2025-01-01',
        'value': 900000
    }
    
    Result: "TSLA_ELONMUSK_20250101_900000"
"""

#Type hint explanation transaction is a dict this functions returns a string
def generate_transaction_id(transaction : dict) -> str:
    #first get the stock ticekrs from transaction 
    #if ticker doesn't exists then use UNKNOWN
    ticker = transaction.get("ticker", "Unknown")

    #second get the insider name from transaction 
    #if insider name doesn't exist then use UNKNOWN
    #Remove the spaces from name and combine them
    insider_name = transaction.get("insider_name", "Unknown").replace(" ", "")

    #third get the trade date from tranasction 
    #if transaction doesn't exist then use UNKNOWN
    #replace the dash with empty and combine them
    trade_date = transaction.get("trade_date", "Unknown").replace("-", "")

    #fourth get the trade value from transaction 
    #if trade value doesn't exist then use 0
    #convert this number into an int
    #then convert this int into a str
    trade_value = str(int(transaction.get("trade_value", 0)))

    #combine to make the id
    transaction_id = f"{ticker}_{insider_name}_{trade_date}_{trade_value}"

    return transaction_id