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