"""
PennyStalker - SEC Edgar Scraper
Fetches SEC filings and filing text for dilution detection
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import re

from .base import BaseScraper
from config_files import DataSources, TimeWindows

logger = logging.getLogger(__name__)


class SECScraper(BaseScraper):
    """
    Scraper for SEC Edgar database
    Fetches recent filings and filing text content
    """
    
    def __init__(self):
        """Initialize SEC scraper"""
        super().__init__()
        
        # Override User-Agent - SEC requires identification
        self.session.headers.update({
            'User-Agent': 'PennyStalker MVP pennystalker@research.com'
        })
        
        self.search_url = DataSources.SEC_SEARCH
        self.base_url = DataSources.SEC_BASE
        
        logger.info("SEC Edgar scraper initialized")
    
    
    def get_filings(self, ticker: str) -> List[Dict]:
        """
        Fetch recent SEC filings for a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            List of dicts with keys: ticker, filing_type, filing_date, filing_url
        """
        logger.info(f"Fetching SEC filings for {ticker}...")
        
        filings = []
        
        # Build search URL
        url = f"{self.search_url}?action=getcompany&CIK={ticker}&type=&dateb=&owner=exclude&count=40"
        
        # Make request
        response = self.make_request(url)
        
        if not response:
            logger.error(f"Failed to fetch SEC page for {ticker}")
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find filing table
        filing_table = soup.find('table', class_='tableFile2')
        
        if not filing_table:
            logger.warning(f"No filings table found for {ticker} - may not be a valid ticker")
            return []
        
        # Parse rows
        rows = filing_table.find_all('tr')[1:]  # Skip header
        
        if not rows:
            logger.warning(f"No filing rows found for {ticker}")
            return []
        
        logger.info(f"Found {len(rows)} filing rows for {ticker}")
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=TimeWindows.FILING_LOOKBACK_DAYS)
        
        # Parse each row
        for row in rows:
            try:
                filing_data = self._parse_filing_row(row, ticker, cutoff_date)
                if filing_data:
                    filings.append(filing_data)
            except Exception as e:
                logger.debug(f"Error parsing filing row: {e}")
                continue
        
        logger.info(f"Extracted {len(filings)} recent filings for {ticker}")
        return filings
    
    
    def _parse_filing_row(self, row, ticker: str, cutoff_date: datetime) -> Optional[Dict]:
        """
        Parse a single filing table row
        
        Args:
            row: BeautifulSoup table row element
            ticker: Stock ticker
            cutoff_date: Ignore filings older than this
            
        Returns:
            Filing dict or None if invalid/too old
        """
        cols = row.find_all('td')
        
        if len(cols) < 4:
            return None
        
        # Extract filing type (e.g., "8-K", "10-Q")
        filing_type = cols[0].get_text(strip=True)
        
        # Extract filing date
        date_text = cols[3].get_text(strip=True)
        
        try:
            filing_date = datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            logger.debug(f"Could not parse date: {date_text}")
            return None
        
        # Skip if too old
        if filing_date < cutoff_date:
            return None
        
        # Extract document URL
        doc_link = cols[1].find('a', {'id': 'documentsbutton'})
        
        if not doc_link:
            return None
        
        filing_url = self.base_url + doc_link['href']
        
        logger.debug(f"Found {filing_type} for {ticker} dated {filing_date.date()}")
        
        return {
            'ticker': ticker.upper(),
            'filing_type': filing_type,
            'filing_date': filing_date,
            'filing_url': filing_url
        }
    
    
    def get_filing_text(self, filing_url: str) -> Optional[str]:
        """
        Download and extract text from an SEC filing
        
        Args:
            filing_url: URL to the filing documents page
            
        Returns:
            Extracted text content or None if failed
        """
        logger.debug(f"Downloading filing from {filing_url}")
        
        try:
            # Step 1: Get the filing documents page
            response = self.make_request(filing_url)
            
            if not response:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Step 2: Find the actual filing document link
            doc_table = soup.find('table', class_='tableFile')
            
            if not doc_table:
                logger.warning("No document table found in filing page")
                return None
            
            # Get first document (main filing)
            first_row = doc_table.find('tr')
            if not first_row:
                return None
            
            doc_link = first_row.find('a')
            if not doc_link:
                return None
            
            doc_url = self.base_url + doc_link['href']
            
            # Step 3: Download the actual filing document
            doc_response = self.make_request(doc_url)
            
            if not doc_response:
                return None
            
            # Step 4: Parse and extract text
            doc_soup = BeautifulSoup(doc_response.text, 'lxml')
            
            # Remove script and style elements
            for script in doc_soup(['script', 'style']):
                script.decompose()
            
            # Get text content
            text = doc_soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Limit size (filings can be huge)
            text = text[:50000]  # First 50k characters
            
            logger.debug(f"Extracted {len(text)} characters from filing")
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting filing text: {e}")
            return None
    
    
    def test_connection(self) -> bool:
        """Test if SEC Edgar is accessible"""
        logger.info("Testing SEC Edgar connection...")
        result = super().test_connection(self.base_url)
        if result:
            logger.info("✅ SEC Edgar is accessible")
        else:
            logger.error("❌ SEC Edgar connection failed")
        return result