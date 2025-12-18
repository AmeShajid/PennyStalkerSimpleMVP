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

#second we are going to do our catalyst keywords we will seperate it into strong medium weak and pump lanuage
class CatalystKeywords:
    # Strong catalysts - Substantive events with clear value
    STRONG = [
        'fda approval', 'fda approved', 'phase 3', 'phase 2 results',
        'acquisition', 'acquired', 'buyout', 'merger agreement',
        'contract awarded', 'government contract', 'defense contract',
        'patent granted', 'patent issued',
        'earnings beat', 'revenue growth',
        'bankruptcy exit', 'chapter 11 exit',
        'uplist', 'uplisting to nasdaq', 'uplisting to nyse'
    ]
    
    # Medium catalysts - Positive but less definitive
    MEDIUM = [
        'partnership', 'strategic partnership', 'collaboration',
        'licensing agreement', 'license agreement',
        'phase 1', 'clinical trial', 'trial enrollment',
        'product launch', 'new product',
        'compliance', 'regained compliance',
        'expanded facility', 'new facility',
        'board appointment', 'executive hire'
    ]
    
    # Weak/Promotional - Vague or non-committal
    WEAK = [
        'exploring', 'considering', 'evaluating',
        'potential', 'possible', 'may pursue',
        'strategic alternatives', 'exploring options',
        'letter of intent', 'loi', 'non-binding',
        'preliminary', 'initial discussions',
        'corporate update', 'shareholder update'
    ]
    
    # Promotional red flags - Often pump language
    PROMOTIONAL = [
        'exciting opportunity', 'ground floor',
        'next big thing', 'revolutionary',
        'game changer', 'disruptive technology',
        'to the moon', 'massive potential',
        'dont miss', 'limited time'
    ]

#third the diff catalyst types
class CatalystTypes:
    FDA = ['fda', 'approval', 'phase', 'clinical', 'trial', 'drug']
    CONTRACT = ['contract', 'awarded', 'government', 'defense', 'purchase order']
    ACQUISITION = ['acquisition', 'merger', 'buyout', 'acquired', 'takeover']
    PARTNERSHIP = ['partnership', 'collaboration', 'joint venture', 'alliance']
    FINANCIAL = ['earnings', 'revenue', 'profit', 'guidance', 'beat estimates']
    REGULATORY = ['compliance', 'sec', 'nasdaq', 'nyse', 'uplist']
    PRODUCT = ['launch', 'product', 'release', 'shipping', 'commercialize']

#fourth we are going to have our catalust requirements
class CatalystRequirements:
        # Strong catalysts should have at least one of these
    CREDIBILITY_INDICATORS = [
        r'\$[\d,]+',  # Dollar amounts: $5M, $10,000
        r'\d+%',  # Percentages: 50%, 25%
        r'\d{4}',  # Years: 2024, 2025
        r'Q[1-4]',  # Quarters: Q1, Q2
        ]
    
#fifth Phrases that indicate dilution risk in SEC filings
class DilutionKeywords:    
    # Critical red flags - Active or imminent offerings
    CRITICAL = [
        'may offer and sell',
        'from time to time',
        'at-the-market',
        'atm offering',
        'registered direct offering',
        'commitment to purchase',
        'we are offering',
        'this prospectus'
    ]
    
    # High risk - Dilutive instruments
    HIGH = [
        'convertible notes',
        'convertible debentures',
        'warrants exercisable',
        'warrant exercise',
        'preferred stock conversion',
        'stock options granted',
        'reset provision'
    ]
    
    # Medium risk - Potential dilution
    MEDIUM = [
        'shelf registration',
        'registered shares',
        'registration statement',
        'selling stockholders',
        'authorized shares increase'
    ]

#sixth we need SEC filing classifications
class FilingTypes:
    # Filings that confirm catalysts
    CONFIRMATION = ['8-K', '8-K/A']
    
    # Filings that indicate dilution risk
    DILUTION_CRITICAL = [
        'S-1', 'S-1/A',  # IPO or new registration
        'S-3', 'S-3/A',  # Shelf registration
        '424B3', '424B5',  # Prospectus supplements (active offerings)
    ]
    
    DILUTION_HIGH = [
        'S-8',  # Employee stock plans
        'POS AM',  # Post-effective amendment
    ]
    
    # Routine filings (neutral)
    ROUTINE = [
        '10-Q', '10-K',  # Quarterly/Annual reports
        '10-Q/A', '10-K/A',
        'DEF 14A',  # Proxy statement
    ]


#seventh we need our scoring system weights 
class ScoringWeights:
    # Base catalyst scores (0-40 points)
    CATALYST_STRONG = 40
    CATALYST_MEDIUM = 25
    CATALYST_WEAK = 10
    CATALYST_PROMOTIONAL = 0  # No points for promotional fluff
    
    # SEC confirmation bonus (0-20 points)
    SEC_CONFIRMATION_8K = 20  # Perfect match: news + 8-K
    SEC_CONFIRMATION_OTHER = 10  # Some filing exists
    SEC_NO_CONFIRMATION = 0
    
    # Dilution penalties (0 to -50 points)
    DILUTION_CRITICAL = -50  # Active offering
    DILUTION_HIGH = -30  # Recent S-1/S-3
    DILUTION_MEDIUM = -15  # Dilution keywords present
    DILUTION_LOW = -5  # Minor historical dilution
    
    # Insider activity adjustments (±10 points) - Future feature
    INSIDER_BUY_SIGNIFICANT = 10
    INSIDER_BUY_SMALL = 5
    INSIDER_SELL_SMALL = -5
    INSIDER_SELL_SIGNIFICANT = -10
    
    # Time decay (0 to -15 points)
    TIME_DECAY_FRESH = 0  # < 24 hours
    TIME_DECAY_RECENT = -5  # 24-48 hours
    TIME_DECAY_OLD = -10  # 48-72 hours
    TIME_DECAY_STALE = -15  # > 72 hours

#eight we need our threholds for the scoring 
class ScoringThresholds:
    # Score ranges for confidence tiers
    HIGH_CONFIDENCE = 70  # 70-100: Strong candidates
    MEDIUM_CONFIDENCE = 50  # 50-69: Worth watching
    LOW_CONFIDENCE = 30  # 30-49: Risky/speculative
    FILTERED = 30  # Below 30: Don't show
    
    # Mandatory caps (override scores)
    MAX_SCORE_WITH_CRITICAL_DILUTION = 40  # Active offering caps score
    MAX_SCORE_PR_ONLY = 50  # No SEC confirmation caps score
    MAX_SCORE_PROMOTIONAL = 20  # Promotional language caps score

#ninth we need to handle our timewindow how far back to we go
class TimeWindows:
    # News freshness (from .env or defaults)
    NEWS_LOOKBACK_HOURS = int(os.getenv('TIME_WINDOW_HOURS', '24'))
    
    # SEC filing freshness
    FILING_LOOKBACK_DAYS = 30  # Look back 30 days for filings
    FILING_CONFIRMATION_DAYS = 3  # Filing within 3 days = confirmation
    
    # Dilution history window
    DILUTION_HISTORY_DAYS = 180  # 6 months of dilution history


#tenth we need to do our parameters for our search
class ScanParameters:
    # From .env or defaults
    MAX_CANDIDATES = int(os.getenv('MAX_CANDIDATES', '20'))
    MIN_SCORE_THRESHOLD = int(os.getenv('MIN_SCORE_THRESHOLD', '30'))
    
    # Request behavior
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', '1.0'))
    
    # Output settings
    SAVE_OUTPUT = os.getenv('SAVE_OUTPUT', 'true').lower() == 'true'
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


#eleventh we need our regex patterns 
class Patterns:
    import re
    
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


#these are going to be our helper functions 
def get_all_catalyst_keywords():
    """Combines all catalyst tiers into one master list."""
    all_keywords = (
        CatalystKeywords.STRONG +
        CatalystKeywords.MEDIUM +
        CatalystKeywords.WEAK +
        CatalystKeywords.PROMOTIONAL
    )
    return all_keywords


def get_all_dilution_keywords():
    """Combines all dilution tiers into one master list."""
    all_dilution = (
        DilutionKeywords.CRITICAL +
        DilutionKeywords.HIGH +
        DilutionKeywords.MEDIUM
    )
    return all_dilution

def is_dilution_filing(filing_type):
    """Checks if a specific filing type is associated with dilution."""
    # 1. Clean the input
    clean_type = filing_type.upper().strip()
    
    # 2. Define what we are looking for
    risky_types = FilingTypes.DILUTION_CRITICAL + FilingTypes.DILUTION_HIGH
    
    # 3. Explicit logic check
    if clean_type in risky_types:
        return True
    else:
        return False


def is_confirmation_filing(filing_type):
    """Checks if a filing confirms news (usually an 8-K)."""
    # 1. Clean the input
    clean_type = filing_type.upper().strip()
    
    # 2. Explicit logic check
    if clean_type in FilingTypes.CONFIRMATION:
        return True
    else:
        return False