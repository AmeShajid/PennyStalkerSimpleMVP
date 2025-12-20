from config_files.CatalystKeywords import CatalystKeywords
from config_files.DilutionKeywords import DilutionKeywords
from config_files.FilingTypes import FilingTypes

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
