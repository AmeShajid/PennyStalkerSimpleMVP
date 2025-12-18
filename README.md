# PennyStalker MVP

**Find penny stocks with real catalysts before they blow up**

A Python-based research tool that scrapes financial news, validates catalysts against SEC filings, detects dilution risk, and ranks opportunities with transparent scoring.

---

## What This Does

PennyStalker MVP automates the tedious parts of penny stock research:

1. **Discovers** recent penny stock news from StockTitan
2. **Validates** catalysts against official SEC filings
3. **Detects** dilution risk (offerings, ATM programs, convertible notes)
4. **Scores** each ticker (0-100) based on catalyst strength, SEC confirmation, and risk factors
5. **Ranks** results so you can focus on the best candidates

**This is NOT:**
- A price prediction tool
- A trading bot
- Financial advice
- Chart analysis

**This IS:**
- A research filter that surfaces validated opportunities early
- A dilution detector that flags obvious traps
- A time-saver that automates manual SEC checking

---

## How It Works

### The Pipeline

```
News Scraping → Ticker Extraction → SEC Validation → Dilution Detection → Scoring → Ranking
```

### The Scoring System

**Catalyst Strength (0-40 points)**
- **Strong** (30-40): FDA approvals, acquisitions, government contracts with dollar amounts
- **Medium** (15-29): Partnerships, licensing deals, compliance milestones
- **Weak** (0-14): Vague PR, LOIs, "exploring options"

**SEC Confirmation Bonus (+20 points)**
- Recent 8-K filing matching the press release = bonus
- No SEC filing = no bonus
- Contradictory filing = penalty

**Dilution Penalty (-50 points max)**
- Active offering or ATM program = severe penalty
- Recent S-1, S-3, or 424B filing = moderate penalty
- "May offer and sell" language = caution flag

**Final Score = Catalyst + SEC Bonus - Dilution Penalty**

### Example Output

```
═══════════════════════════════════════════════════════════════
RANK 1: ABCD - Score: 85/100
═══════════════════════════════════════════════════════════════
Catalyst: FDA approval for Phase 2 trial (STRONG)
SEC Status: 8-K filed confirming announcement (+20)
Dilution Risk: NONE detected
Reasoning: Strong catalyst with SEC confirmation, no red flags

News: https://stocktitan.net/news/ABCD/...
Filing: https://sec.gov/cgi-bin/...

═══════════════════════════════════════════════════════════════
RANK 2: WXYZ - Score: 50/100
═══════════════════════════════════════════════════════════════
Catalyst: Partnership announcement (MEDIUM)
SEC Status: No recent 8-K found
Dilution Risk: HIGH - Active S-3 offering detected (-30)
Reasoning: Moderate catalyst but active dilution is a major red flag

News: https://stocktitan.net/news/WXYZ/...
Filing: https://sec.gov/cgi-bin/...
```

---

## Setup

### Requirements

- Python 3.8+
- Internet connection (for scraping)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pennystalker_mvp.git
   cd pennystalker_mvp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings** (optional)
   
   Edit `.env` to customize:
   ```
   LOG_LEVEL=INFO              # INFO or DEBUG
   MAX_CANDIDATES=20           # How many tickers to process
   TIME_WINDOW_HOURS=24        # Look back period for news
   MIN_SCORE_THRESHOLD=40      # Minimum score to display
   ```

---

## Usage

### Basic Run

```bash
python main.py
```

### What Happens

1. Scrapes last 24 hours of penny stock news from StockTitan
2. Extracts ticker symbols from headlines
3. For each ticker:
   - Fetches recent SEC filings
   - Classifies catalyst strength
   - Detects dilution language
   - Calculates score (0-100)
4. Ranks results by score
5. Displays top candidates in terminal
6. Saves full results to `output/scan_YYYYMMDD_HHMMSS.txt`

### Expected Runtime

- **Small scan** (5-10 tickers): 30-60 seconds
- **Medium scan** (10-20 tickers): 1-2 minutes
- **Large scan** (20+ tickers): 2-5 minutes

*Time varies based on SEC website response times*

---

## Understanding the Results

### Score Ranges

| Score | Interpretation |
|-------|----------------|
| 80-100 | Strong catalyst, SEC confirmed, no dilution red flags |
| 60-79 | Good catalyst with minor concerns (no SEC filing or minor dilution history) |
| 40-59 | Moderate catalyst OR strong catalyst with dilution concerns |
| 20-39 | Weak catalyst or significant dilution risk |
| 0-19 | Promotional PR or active offering detected |

### Red Flags to Watch

🚨 **HIGH DILUTION RISK** - Active offering or recent S-1 filing
⚠️ **CAUTION** - Recent dilution activity or no SEC confirmation
✅ **CLEAN** - Strong catalyst with SEC confirmation, no dilution detected

---

## Data Sources

- **News**: [StockTitan Live News](https://www.stocktitan.net/news/live.html)
- **SEC Filings**: [SEC Edgar Database](https://www.sec.gov/search-filings)
- **Insider Activity**: [OpenInsider](http://openinsider.com/) *(future feature)*

---

## Project Structure

```
pennystalker_mvp/
├── .env                    # Runtime configuration
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── config.py             # Constants, keywords, scoring weights
├── scraper.py            # Web scraping functions
├── analyzer.py           # Catalyst classification, dilution detection, scoring
├── main.py               # Orchestrates the pipeline
│
└── output/               # Scan results saved here
    └── .gitkeep
```

---

## Limitations & Disclaimers

### What This Tool Cannot Do

❌ Predict price movements
❌ Guarantee profitable trades
❌ Detect all forms of dilution (some are hidden or announced after-hours)
❌ Replace human judgment and due diligence
❌ Account for liquidity issues, halts, or market conditions

### Known Limitations

- **Scraping fragility**: If StockTitan or SEC changes their HTML, scraping may break
- **False positives**: Promotional press releases can score high if SEC filing exists for unrelated reasons
- **False negatives**: Not all legitimate catalysts result in press releases
- **Delayed filings**: SEC filings can lag news by days
- **Rate limits**: Aggressive scanning may trigger rate limits

### Risk Warning

**Penny stocks are extremely risky and volatile.** Most penny stocks fail. This tool helps identify potential opportunities but cannot eliminate risk.

**This tool does NOT provide investment advice.** All results are for informational and educational purposes only. You are solely responsible for your own investment decisions.

Always conduct your own research and never invest money you cannot afford to lose.

---

## How Scoring Works (Technical Details)

### Catalyst Classification

**Strong Catalysts** (30-40 points) must have:
- Specific dollar amounts OR specific dates OR named counterparties
- Substantive events (FDA approval, acquisition, government contract)

**Medium Catalysts** (15-29 points):
- Partnerships without dollar amounts
- Compliance achievements
- Product launches

**Weak Catalysts** (0-14 points):
- Vague press releases
- "Exploring strategic alternatives"
- Letters of intent without binding terms

### Dilution Detection

High-risk indicators:
- Filing types: S-1, S-3, 424B3, 424B5
- Keywords: "may offer and sell", "from time to time", "at-the-market", "convertible notes"
- Recent history: Multiple offerings in past 6 months

### Scoring Formula

```
Base Score = Catalyst Points (0-40)

+ SEC Confirmation Bonus (0-20):
  • 8-K filed within 3 days of news: +20
  • Other recent filings: +10
  • No filings: 0

- Dilution Penalty (0-50):
  • Active offering: -50
  • Recent S-1/S-3: -30
  • Offering keywords: -15
  • Historical diluter: -10

Final Score = max(0, min(100, Base + Bonus - Penalty))
```

---

## Troubleshooting

### "No results found"
- StockTitan may have no penny stock news in the time window
- Try increasing `TIME_WINDOW_HOURS` in `.env`
- Check if StockTitan website is accessible

### "SEC request failed"
- SEC Edgar may be temporarily unavailable
- You may have hit rate limits (wait 10 minutes)
- Check your internet connection

### "ModuleNotFoundError"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Scraping returns empty data
- Website HTML structure may have changed
- Open an issue on GitHub with the error message

---

## Future Enhancements (V2 Roadmap)

- [ ] Database storage for historical tracking
- [ ] Insider trading signals integration
- [ ] Email/SMS alerts for high-scoring candidates
- [ ] Web interface
- [ ] Backtesting framework
- [ ] Additional news sources
- [ ] Options flow data
- [ ] Social sentiment analysis

---

## Contributing

This is a personal research tool, but suggestions are welcome:

1. Open an issue describing the enhancement
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## Disclaimer

**FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

This software is provided "as is" without warranty of any kind. The author is not a financial advisor and this tool does not provide investment advice.

Trading penny stocks involves substantial risk of loss. Past performance does not indicate future results. Always do your own research and consult with a qualified financial advisor before making investment decisions.

The author assumes no liability for any financial losses incurred through use of this software.

---

## Acknowledgments

Data sources:
- [StockTitan](https://www.stocktitan.net/) for news aggregation
- [SEC Edgar](https://www.sec.gov/) for official filings
- [OpenInsider](http://openinsider.com/) for insider activity

Built with Python, BeautifulSoup, and the requests library.

---

**Remember: The best trade is often the one you don't make.**