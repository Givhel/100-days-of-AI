# 🛒 Amazon Wishlist Analyzer

> Day 2 of 100 Days — Cracking Remote Internships in AI/ML  
> Built by Kunal | [@thekunal.build](https://instagram.com/thekunal.build) | [github.com/Givhel](https://github.com/Givhel)

---

## What this does

Analyzes 30 days of price history for products in your Amazon wishlist and tells you:
- Which **day of the week** each product is cheapest
- Whether you should **buy now or wait**
- How much you can **save** by timing your purchase right

---

## ⚠️ Important — Read this

**Amazon does not have a public API for price data.**

Direct scraping of Amazon is against their Terms of Service and gets blocked aggressively. This project uses **simulated price data** based on real Amazon pricing patterns — prices genuinely do fluctuate by day of week, and Wednesday and Friday tend to be cheapest for most categories.

The real production version of this would use:
- [ScraperAPI](https://scraperapi.com) — handles proxies and rotating headers
- [Oxylabs](https://oxylabs.io) — enterprise scraping solution
- [Keepa API](https://keepa.com) — actual Amazon price history API (paid)
- [CamelCamelCamel](https://camelcamelcamel.com) — free price history tracker

I'll build the real scraping version in a future video when I cover Selenium and proxy rotation.

---

## How to run

```bash
# Clone the repo
git clone https://github.com/Givhel/amazon-wishlist-analyzer
cd amazon-wishlist-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run terminal analyzer
python analyzer.py

# Run Streamlit dashboard
streamlit run dashboard.py
```

---

## Tech stack

| Tool | Used for |
|------|----------|
| Python | Core logic and data processing |
| Pandas | Price history analysis |
| Plotly | Interactive charts |
| Streamlit | Dashboard UI |
| SQLite | Local price storage |

---

## What I learned building this

- How to structure a real Python project
- Pandas data aggregation and groupby operations
- Plotly chart customization for dark themes
- Streamlit layout and component design
- Why Amazon blocks scrapers and how real companies handle it

---

## Project structure

```
amazon-wishlist-analyzer/
├── analyzer.py       ← Animated terminal version
├── dashboard.py      ← Streamlit dashboard
├── data.py           ← Price simulation and analysis logic
├── requirements.txt
└── README.md
```

---

## Part of my 100-day challenge

I'm building 10 real AI projects in 100 days to crack a remote internship.  
Every project is deployed. Every mistake is documented. Nothing is hidden.

Follow the journey:
- Instagram: [@thekunal.build](https://instagram.com/thekunal.build)
- YouTube: [Kunal Builds](https://youtube.com/@BuildAIwithKunal)
- GitHub: [github.com/Givhel](https://github.com/Givhel)

---

⭐ Star this repo if you found it useful. Comment **Day 2** on Instagram for the link.
