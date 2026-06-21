# data.py
# Simulated price history for demo
# Real version: use ScraperAPI or Oxylabs

from datetime import datetime, timedelta
import random

PRODUCTS = [
    {
        "name": "boAt Airdopes 141",
        "category": "Earbuds",
        "image": "🎧",
        "base_price": 4999,
        "amazon_url": "https://amazon.in/dp/B09X4KXZQY"
    },
    {
        "name": "Noise ColorFit Pro 4",
        "category": "Smartwatch", 
        "image": "⌚",
        "base_price": 3999,
        "amazon_url": "https://amazon.in"
    },
    {
        "name": "Ambrane 20000mAh Powerbank",
        "category": "Powerbank",
        "image": "🔋",
        "base_price": 1299,
        "amazon_url": "https://amazon.in"
    },
    {
        "name": "Logitech M235 Mouse",
        "category": "Accessories",
        "image": "🖱️",
        "base_price": 1595,
        "amazon_url": "https://amazon.in"
    },
    {
        "name": "Kindle Paperwhite",
        "category": "E-reader",
        "image": "📖",
        "base_price": 13999,
        "amazon_url": "https://amazon.in"
    }
]

# Price multiplier by day of week
# This simulates real Amazon pricing patterns
DAY_MULTIPLIERS = {
    0: 1.05,   # Monday — slightly high
    1: 1.02,   # Tuesday
    2: 0.94,   # Wednesday — usually lowest
    3: 1.00,   # Thursday — average
    4: 0.97,   # Friday — weekend sale prep
    5: 1.08,   # Saturday — high demand
    6: 1.06,   # Sunday — high demand
}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", 
             "Thursday", "Friday", "Saturday", "Sunday"]

def generate_price_history(base_price, days=30):
    """
    Generates 30 days of realistic price history.
    Prices fluctuate by day of week + random noise.
    """
    history = []
    today = datetime.now()
    
    for i in range(days, 0, -1):
        date = today - timedelta(days=i)
        day_of_week = date.weekday()
        
        # Apply day multiplier + random noise (±3%)
        noise = random.uniform(-0.03, 0.03)
        multiplier = DAY_MULTIPLIERS[day_of_week] + noise
        price = round(base_price * multiplier, -1)  # Round to nearest 10
        
        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": DAY_NAMES[day_of_week],
            "price": price
        })
    
    return history

def get_best_day(history):
    """
    Finds which day of week has lowest average price.
    """
    import pandas as pd
    df = pd.DataFrame(history)
    avg_by_day = df.groupby("day")["price"].mean()
    best_day = avg_by_day.idxmin()
    return best_day, avg_by_day

def analyze_product(product):
    """
    Full analysis for one product.
    Returns everything needed for the dashboard.
    """
    history = generate_price_history(product["base_price"])
    best_day, avg_by_day = get_best_day(history)
    
    current_price = history[-1]["price"]
    lowest_price = min(h["price"] for h in history)
    highest_price = max(h["price"] for h in history)
    avg_price = sum(h["price"] for h in history) / len(history)
    
    # How much cheaper is best day vs average
    best_day_price = avg_by_day[best_day]
    avg_saving = round(avg_price - best_day_price)
    
    # Is now a good time to buy?
    today = DAY_NAMES[datetime.now().weekday()]
    price_vs_avg = ((current_price - avg_price) / avg_price) * 100
    
    if price_vs_avg <= -3:
        recommendation = "BUY NOW ✅"
        rec_color = "#1D9E75"
    elif price_vs_avg <= 3:
        recommendation = "DECENT TIME 🟡"
        rec_color = "#BA7517"
    else:
        recommendation = f"WAIT FOR {best_day.upper()} ⏳"
        rec_color = "#E24B4A"
    
    return {
        "product": product,
        "history": history,
        "best_day": best_day,
        "current_price": current_price,
        "lowest_price": lowest_price,
        "highest_price": highest_price,
        "avg_price": round(avg_price),
        "avg_saving": avg_saving,
        "recommendation": recommendation,
        "rec_color": rec_color,
        "price_vs_avg": round(price_vs_avg, 1)
    }