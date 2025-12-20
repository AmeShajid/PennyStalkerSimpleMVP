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
