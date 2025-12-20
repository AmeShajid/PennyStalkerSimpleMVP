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