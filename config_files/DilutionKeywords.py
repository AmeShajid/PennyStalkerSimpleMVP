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