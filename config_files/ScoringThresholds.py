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
