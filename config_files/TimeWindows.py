import os

#ninth we need to handle our timewindow how far back to we go
class TimeWindows:
    # News freshness (from .env or defaults)
    NEWS_LOOKBACK_HOURS = int(os.getenv('TIME_WINDOW_HOURS', '24'))
    
    # SEC filing freshness
    FILING_LOOKBACK_DAYS = 30  # Look back 30 days for filings
    FILING_CONFIRMATION_DAYS = 3  # Filing within 3 days = confirmation
    
    # Dilution history window
    DILUTION_HISTORY_DAYS = 180  # 6 months of dilution history
