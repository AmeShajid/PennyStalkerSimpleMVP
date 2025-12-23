"""
PennyStalker - StockTitan News Scraper
Fetches penny stock news from StockTitan
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import re

from .base import BaseScraper
from config_files import DataSources, TimeWindows, Patterns

logger = logging.getLogger(__name__)


class StockTitanScraper(BaseScraper):
    """
    Scraper for StockTitan live news
    Extracts recent penny stock headlines with tickers
    """
    
    def __init__(self):
        """Initialize StockTitan scraper"""
        super().__init__()
        self.news_url = DataSources.STOCKTITAN_NEWS
        logger.info("StockTitan scraper initialized")
    
    
    def get_recent_news(self) -> List[Dict]:
        """
        Fetch recent penny stock news from StockTitan
        
        Returns:
            List of dicts with keys: ticker, headline, url, published_time, source
        """
        logger.info("Fetching news from StockTitan...")
        
        news_items = []
        
        # Make request using base class method
        response = self.make_request(self.news_url)
        
        if not response:
            logger.error("Failed to fetch StockTitan page")
            return []
        
        logger.info(f"StockTitan responded with status {response.status_code}")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find news entries - StockTitan uses <div class="link-block">
        news_entries = soup.find_all('div', class_='link-block')
        
        if not news_entries:
            logger.warning("No news entries found - HTML structure may have changed")
            # Try alternative selector
            news_entries = soup.find_all('a', href=re.compile(r'/news/'))
        
        logger.info(f"Found {len(news_entries)} potential news entries")
        
        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(hours=TimeWindows.NEWS_LOOKBACK_HOURS)
        
        # Parse each entry
        for entry in news_entries[:50]:  # Limit to first 50
            try:
                news_data = self._parse_news_entry(entry, cutoff_time)
                if news_data:
                    news_items.extend(news_data)
            except Exception as e:
                logger.debug(f"Error parsing entry: {e}")
                continue
        
        logger.info(f"Successfully extracted {len(news_items)} news items with tickers")
        return news_items
    
    
    def _parse_news_entry(self, entry, cutoff_time: datetime) -> List[Dict]:
        """
        Parse a single news entry element
        
        Args:
            entry: BeautifulSoup element
            cutoff_time: Ignore news older than this
            
        Returns:
            List of news item dicts (one per ticker found)
        """
        news_items = []
        
        # Extract headline
        headline_elem = entry.find('div', class_='title') or entry.find('h3') or entry
        headline = headline_elem.get_text(strip=True) if headline_elem else ""
        
        if not headline or len(headline) < 10:
            return []
        
        # Extract URL
        url = entry.get('href', '')
        if url and not url.startswith('http'):
            url = f"https://www.stocktitan.net{url}"
        
        # Extract timestamp
        time_elem = entry.find('time') or entry.find('span', class_='time')
        published_time = None
        
        if time_elem:
            time_text = time_elem.get_text(strip=True)
            published_time = self._parse_time(time_text)
        
        # Default to now if no timestamp
        if not published_time:
            published_time = datetime.now()
        
        # Skip if too old
        if published_time < cutoff_time:
            return []
        
        # Extract tickers from headline
        tickers = self._extract_tickers(headline)
        
        if not tickers:
            logger.debug(f"No tickers found in: {headline[:60]}...")
            return []
        
        # Create news item for each ticker
        for ticker in tickers:
            news_item = {
                'ticker': ticker.upper(),
                'headline': headline,
                'url': url,
                'published_time': published_time,
                'source': 'StockTitan'
            }
            news_items.append(news_item)
            logger.debug(f"Found news for {ticker}: {headline[:50]}...")
        
        return news_items
    
    
    def _parse_time(self, time_text: str) -> datetime:
        """
        Parse StockTitan's time format
        Handles: "2 hours ago", "5 minutes ago", "today", "yesterday", actual dates
        
        Args:
            time_text: Time string from StockTitan
            
        Returns:
            datetime object
        """
        time_text = time_text.lower().strip()
        now = datetime.now()
        
        try:
            # Relative times
            if 'minute' in time_text:
                match = re.search(r'(\d+)', time_text)
                if match:
                    minutes = int(match.group(1))
                    return now - timedelta(minutes=minutes)
            
            elif 'hour' in time_text:
                match = re.search(r'(\d+)', time_text)
                if match:
                    hours = int(match.group(1))
                    return now - timedelta(hours=hours)
            
            elif 'day' in time_text and 'yesterday' not in time_text:
                match = re.search(r'(\d+)', time_text)
                if match:
                    days = int(match.group(1))
                    return now - timedelta(days=days)
            
            elif 'today' in time_text:
                return now
            
            elif 'yesterday' in time_text:
                return now - timedelta(days=1)
            
            # TODO: Add actual date parsing if needed (e.g., "Dec 17, 2024")
            # For now, assume recent if we can't parse
            return now
            
        except Exception as e:
            logger.debug(f"Error parsing time '{time_text}': {e}")
            return now
    
    
    def _extract_tickers(self, text: str) -> List[str]:
        """
        Extract ticker symbols from text using multiple patterns
        
        Args:
            text: Text to search for tickers
            
        Returns:
            List of unique ticker symbols
        """
        tickers = set()
        
        # Pattern 1: $TICKER format (most reliable)
        dollar_tickers = Patterns.TICKER_WITH_DOLLAR.findall(text)
        tickers.update(dollar_tickers)
        
        # Pattern 2: (NASDAQ: TICKER) or (NYSE: TICKER) format
        paren_matches = Patterns.TICKER_IN_PARENS.findall(text)
        tickers.update([match[1] for match in paren_matches])
        
        # Pattern 3: Standalone uppercase words (more prone to false positives)
        # Only use if no tickers found yet
        if not tickers:
            potential_tickers = Patterns.TICKER.findall(text)
            
            # Filter out common false positives
            false_positives = {
                'THE', 'AND', 'FOR', 'INC', 'LLC', 'USA', 'CEO', 'CFO', 
                'FDA', 'SEC', 'IPO', 'NYSE', 'NASDAQ', 'OTC', 'ETF',
                'NEWS', 'STOCK', 'MARKET', 'ABOUT', 'WILL', 'HAVE'
            }
            
            # Only keep if 1-5 chars and not a false positive
            valid_tickers = [
                t for t in potential_tickers 
                if t not in false_positives and 1 <= len(t) <= 5
            ]
            tickers.update(valid_tickers)
        
        return list(tickers)
    
    
    def test_connection(self) -> bool:
        """Test if StockTitan is accessible"""
        logger.info("Testing StockTitan connection...")
        result = super().test_connection(self.news_url)
        if result:
            logger.info("✅ StockTitan is accessible")
        else:
            logger.error("❌ StockTitan connection failed")
        return result