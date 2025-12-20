import os

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
