#fourth we are going to have our catalust requirements
class CatalystRequirements:
        # Strong catalysts should have at least one of these
    CREDIBILITY_INDICATORS = [
        r'\$[\d,]+',  # Dollar amounts: $5M, $10,000
        r'\d+%',  # Percentages: 50%, 25%
        r'\d{4}',  # Years: 2024, 2025
        r'Q[1-4]',  # Quarters: Q1, Q2
        ]