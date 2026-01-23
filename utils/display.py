"""
This file handles the terminal output
Purpose : Make the terminal output clean, organized, and easy to read

Class OOP:
    This will group all the terminal display methods together
"""

class TerminalDisplay:

    def __init__(self):
        #this is going to the border for top and bottom sections
        self.border_char = "="
        #this is going to be the item seperator 
        self.separator_char = "-"
        #this is the width of the display 
        self.width = 60

    #creating a border line using the border charcter
    def create_border(self) -> str:
        # This creates a line like "═══════════════════════════"
        return self.border_char * self.width
    
    #creating a separator character by the width
    def create_separator(self) -> str:
        # This creates a line like "───────────────────────────"
        return self.separator_char * self.width
    
    #asking for what timeframe they want to choose 
    def show_timeframe_menu(self) -> str:
        #returns 2 weeks or month
        # Print menu
        print("\n" + self.create_border())
        print("Select Timeframe:")
        print(self.create_border())
        print()
        print("1) Last 2 Weeks")
        print("2) Last Month")
        print()

        #so now while is true
        while True:
            choice =  input("Enter 1 or 2 : ").strip()
            if choice == "1":
                return "2weeks"
            elif choice == "2":
                return "month"
            else:
                print("invalid choice.. choose either 1 or 2")
                    
    #this is going to show the menu and also get the user's choice 
    def show_menu(self) -> str:
        #make a 2 line clear screen 
        print("\n" * 2)

        #make the top border
        print(self.create_border())
        #this is the title 
        print("PennyStalker - Insider Trading Scanner".center(self.width))
        #this is the bottom border
        print(self.create_border())

        #extra space
        print()

        #asking user what they want
        print("What would you like too see")

        #extra space
        print()
        
        #these are the LATEST trades
        print("LATEST Insider Trades:")

        #these are the different options
        print("a) Latest Cluster Buys")
        print("b) Latest Penny Stock Buys")
        print("c) Latest Insider Trading (all filings)")
        print("d) Latest Insider Purchases")
        print("e) Latest Insider Purchases $25k+")
        print("f) Latest Officer Purchases $25k+")
        print("g) Latest CEO/CFO Purchases $25k+")
        print("h) Latest Insider Sales")
        print("i) Latest Insider Sales $100k+")
        print("j) Latest Officer Sales $100+")
        print("k) Latest CEO/CFO Sales $100k+")


        #extra space
        print()

        # Print the TOP trades
        print("TOP Insider Trades:")
        
        #these are the different options
        print("l) Top Officer Purchases Today")
        print("m) Top Officer Purchases Past Week")
        print("n) Top Insider Purchases Today")
        print("o) Top Insider Purchases Past Week")
        print("p) Top Insider Sales Today")
        print("q) Top Insider Sales Past Week")

        #extra space
        print()

        #loop until we have a proper input
        while True:
            #ask user for input and normalize input
            choice = input("Enter your choice (a-t): ").strip().lower()
            #check if the choice is valid 
            if choice in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', "n", "o", "p", "q"]:
                #this is a valid choice
                return choice 
            else:
                #invalid choice 
                print("Invalid choice, Enter a letter from a to q")
        
    #this is going to display the header when starting a scan 
    def display_scan_header(self, scan_name: str):
        #extra space
        print()

        #this is the top of the broder
        print(self.create_border())
        #print the scan name
        print(f"Scanning : {scan_name}")
        #print the timeframe
        print(f"Timeframe : Last 2 weeks")
        #this is the bottom of the border
        print(self.create_border())

        #extra space
        print()

    #this is going to display a message while processing transactions
    def display_processing_message(self, num_transaction: int):
        #printing number of transactions
        print(f"Processing {num_transaction} transaction...")
        
    #this is going to display each transaction in a specific order
    def display_transaction(self, transaction: dict, rank: int):
        #starting of border
        print(self.create_border())

        #print the rank ticker and company name
        print(f"#{rank} : {transaction['ticker']} - {transaction['company_name']}")

        #print the bottom border
        print(self.create_border())
        
        #extra space
        print()

        #Insider transaction info
        print("INSIDER TRANSACTION:")

        #insider name and title
        print(f"Insider: {transaction['insider_name']}")
        print(f"Title: {transaction['insider_title']}")

        #print filing date
        print(f"Filing Date: {transaction['filing_date']}")

        #print trade date
        print(f"Trade Date: {transaction['trade_date']}")

        #extra space
        print()

        #print Transaction Details
        print("TRANSACTION DETAILS:")
        
        #print price per share
        print(f"Price: ${transaction['price']:.2f}")

        #print the quantity (comma is for thousands)
        quantity_formatted = f"{transaction['quantity']:,}"
        print(f"Quantity: +{quantity_formatted} shares")

        #the total value
        value_formatted = f"{transaction['value']:,.0f}"

        #star emoji for values over 1m
        if transaction['value'] >= 1000000:
            print(f"  Total Value: ${value_formatted} ⭐")
        else:
            print(f"  Total Value: ${value_formatted}")
        
        #total shares owned after purchase
        owned_formatted = f"{transaction['owned']:,}"
        print(f"Now Owns: {owned_formatted} shares")

        # Print percentage change in ownership
        delta_own = transaction['delta_own_pct']

        # Rocket emoji if ownership increased by 50% or more (strong signal)
        if delta_own >= 50:
            print(f"Change: +{delta_own:.1f}% 🚀")
        else:
            print(f"Change: +{delta_own:.1f}%")
        
        #Extra Space
        print()

    #Summary statistics after scan completes
    def display_summary(self, total_scraped: int, num_new: int, num_duplicates: int, highest_value: float):
        # Print start of border
        print(self.create_border())
        #scan complete
        print("SCAN COMPLETE")
        #print end of border
        print(self.create_border())
        
        #extra space
        print()
        
        # Print summary header
        print("Summary:")
        
        # Print total transactions scraped
        print(f"• Total scraped: {total_scraped} transactions")
        
        # Print number of new transactions found
        print(f"• New transactions: {num_new}")
        
        # Print number of duplicates skipped
        print(f"• Already in DB: {num_duplicates}")
        
        # Print highest value found
        highest_formatted = f"{highest_value:,.0f}"
        print(f"• Highest value: ${highest_formatted}")
        
        #extra space
        print()
        
        # Print database location
        print("Results saved to database: pennystalker.db")
        
        #extra space
        print()

    #Display message when no new transactions are found
    def display_no_new_transactions(self):
        #extra space
        print()
        print("No new transactions found.")
        print("All scraped transactions were already in the database.")
        print()
        print("Tip: Try a different scan type or check back later.")
        #extra space
        print()

    #Error for when we cant display properly
    def display_error(self, error_message: str):
        #extra space
        print()
        print(self.create_separator())
        print(f"ERROR: {error_message}")
        print(self.create_separator())
        #extra space
        print()