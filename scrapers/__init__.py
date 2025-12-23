"""
PennyStalker - Scrapers Package
Data collection from StockTitan and SEC Edgar
"""

from .stocktitan import StockTitanScraper
from .sec import SECScraper

__all__ = [
    'StockTitanScraper',
    'SECScraper',
]

__version__ = '1.0.0'