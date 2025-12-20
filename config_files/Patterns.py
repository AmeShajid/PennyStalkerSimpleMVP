import re

#eleventh we need our regex patterns 
class Patterns:
    # Ticker extraction: $AAPL, (NASDAQ: AAPL), AAPL:, etc.
    TICKER = re.compile(r'\b[A-Z]{1,5}\b(?=\s|$|:|\))')
    TICKER_WITH_DOLLAR = re.compile(r'\$([A-Z]{1,5})\b')
    TICKER_IN_PARENS = re.compile(r'\(([A-Z]+):\s*([A-Z]{1,5})\)')
    
    # Money amounts: $5M, $10,000, $5.2 million
    MONEY = re.compile(r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|M|B))?', re.IGNORECASE)
    
    # Percentages: 50%, 25.5%
    PERCENTAGE = re.compile(r'\d+(?:\.\d+)?%')
    
    # Dates: 2024, Q1 2024, December 2024
    YEAR = re.compile(r'\b20\d{2}\b')
    QUARTER = re.compile(r'\bQ[1-4]\s*20\d{2}\b')
