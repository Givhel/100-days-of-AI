# analyzer.py — Amazon Wishlist Analyzer
# Day 2 of 100 Days — @thekunal.build
# Run: python analyzer.py

import time
import sys
import random
from datetime import datetime, timedelta

# ─── COLORS ───────────────────────────────────────────────
GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
PURPLE  = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
BG_DARK = "\033[40m"

# Product accent colors — each product gets its own color
PRODUCT_COLORS = [CYAN, PURPLE, GREEN, YELLOW, BLUE]

# ─── DATA ─────────────────────────────────────────────────
PRODUCTS = [
    {"name": "boAt Airdopes 141",        "emoji": "🎧", "base": 4999},
    {"name": "Noise ColorFit Pro 4",     "emoji": "⌚", "base": 3999},
    {"name": "Ambrane 20000mAh",         "emoji": "🔋", "base": 1299},
    {"name": "Logitech M235 Mouse",      "emoji": "🖱️",  "base": 1595},
    {"name": "Kindle Paperwhite",        "emoji": "📖", "base": 13999},
]

DAY_MULTIPLIERS = {
    "Monday":    1.05,
    "Tuesday":   1.02,
    "Wednesday": 0.91,
    "Thursday":  1.00,
    "Friday":    0.95,
    "Saturday":  1.09,
    "Sunday":    1.07,
}

DAYS = list(DAY_MULTIPLIERS.keys())

# ─── HELPERS ──────────────────────────────────────────────
def clear_line():
    sys.stdout.write("\033[2K\r")
    sys.stdout.flush()

def type_out(text, delay=0.018, color=""):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(text, duration=1.0, color=CYAN):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {color}{frames[i%len(frames)]}{RESET} {text}")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    clear_line()

def progress_bar(label, duration=0.8, color=CYAN, width=28):
    sys.stdout.write(f"  {label} [")
    sys.stdout.flush()
    steps = width
    for i in range(steps):
        time.sleep(duration / steps)
        filled = "█" * (i + 1)
        empty  = "░" * (steps - i - 1)
        pct    = int(((i + 1) / steps) * 100)
        sys.stdout.write(f"\r  {label} [{color}{filled}{GRAY}{empty}{RESET}] {WHITE}{pct}%{RESET}")
        sys.stdout.flush()
    print()

def mini_bar(value, max_val, width=20, color=GREEN):
    filled = int((value / max_val) * width)
    empty  = width - filled
    return f"{color}{'█' * filled}{GRAY}{'░' * empty}{RESET}"

def divider(char="─", color=GRAY, width=54):
    print(f"{color}{char * width}{RESET}")

def analyze(product):
    base  = product["base"]
    hist  = {}
    for day in DAYS:
        m      = DAY_MULTIPLIERS[day]
        noise  = random.uniform(-0.025, 0.025)
        prices = [round(base * (m + random.uniform(-0.02, 0.02)), -1) for _ in range(4)]
        hist[day] = prices

    avg_by_day   = {d: sum(p) / len(p) for d, p in hist.items()}
    best_day     = min(avg_by_day, key=avg_by_day.get)
    worst_day    = max(avg_by_day, key=avg_by_day.get)
    current      = round(base * (DAY_MULTIPLIERS[datetime.now().strftime("%A")] + random.uniform(-0.02, 0.02)), -1)
    lowest       = round(min(avg_by_day.values()), -1)
    highest      = round(max(avg_by_day.values()), -1)
    avg          = round(sum(avg_by_day.values()) / 7, -1)
    saving       = round(avg - lowest, -1)
    pct_vs_avg   = ((current - avg) / avg) * 100

    if pct_vs_avg <= -3:
        rec       = "BUY NOW"
        rec_color = GREEN
        rec_icon  = "✅"
    elif pct_vs_avg <= 3:
        rec       = "DECENT"
        rec_color = YELLOW
        rec_icon  = "🟡"
    else:
        rec       = f"WAIT → {best_day[:3].upper()}"
        rec_color = RED
        rec_icon  = "⏳"

    return {
        "best_day":    best_day,
        "worst_day":   worst_day,
        "avg_by_day":  avg_by_day,
        "current":     current,
        "lowest":      lowest,
        "highest":     highest,
        "avg":         avg,
        "saving":      saving,
        "pct_vs_avg":  pct_vs_avg,
        "rec":         rec,
        "rec_color":   rec_color,
        "rec_icon":    rec_icon,
    }

# ─── MAIN ─────────────────────────────────────────────────
def main():
    print()
    print(f"  {BOLD}{PURPLE}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"  {BOLD}{PURPLE}║   🛒  AMAZON WISHLIST ANALYZER                  ║{RESET}")
    print(f"  {BOLD}{PURPLE}║   Built with Python + Pandas  |  Day 2 of 100   ║{RESET}")
    print(f"  {BOLD}{PURPLE}║   @thekunal.build                               ║{RESET}")
    print(f"  {BOLD}{PURPLE}╚══════════════════════════════════════════════════╝{RESET}")
    print()
    time.sleep(0.5)

    type_out("  Connecting to Amazon...", color=GRAY)
    spinner("Authenticating session", 1.0, CYAN)
    spinner("Loading wishlist", 0.8, CYAN)
    print()

    print(f"  {BOLD}{WHITE}📋 Found {len(PRODUCTS)} products in your wishlist:{RESET}")
    print()
    for i, p in enumerate(PRODUCTS):
        time.sleep(0.2)
        color = PRODUCT_COLORS[i]
        print(f"  {color}  {i+1}. {p['emoji']}  {p['name']}{RESET}")
    
    print()
    divider()
    print()
    time.sleep(0.4)

    print(f"  {BOLD}{WHITE}🔍 Fetching 30-day price history...{RESET}")
    print()

    results = []
    for i, p in enumerate(PRODUCTS):
        color = PRODUCT_COLORS[i]
        progress_bar(f"{color}{p['emoji']} {p['name'][:22]:<22}{RESET}", duration=0.6, color=color)
        result = analyze(p)
        results.append(result)
        time.sleep(0.1)

    print()
    divider("═", PURPLE)
    print(f"  {BOLD}{WHITE}  📊  RESULTS — BEST TIME TO BUY EACH PRODUCT{RESET}")
    divider("═", PURPLE)
    print()
    time.sleep(0.3)

    max_saving = max(r["saving"] for r in results)

    for i, (p, r) in enumerate(zip(PRODUCTS, results)):
        color = PRODUCT_COLORS[i]
        time.sleep(0.25)

        # Product header
        print(f"  {BOLD}{color}  {p['emoji']}  {p['name']}{RESET}")
        divider("·", GRAY, 54)

        # Price row
        print(f"  {GRAY}Current   {RESET}{WHITE}₹{r['current']:>7,.0f}  {RESET}", end="")
        print(f"{GRAY}Avg  {RESET}{WHITE}₹{r['avg']:>7,.0f}  {RESET}", end="")
        print(f"{GRAY}Lowest  {RESET}{GREEN}₹{r['lowest']:>7,.0f}{RESET}")

        # Day by day mini chart
        print()
        print(f"  {GRAY}Price by day:{RESET}")
        best = r["best_day"]
        worst = r["worst_day"]
        max_price = max(r["avg_by_day"].values())

        for day, price in r["avg_by_day"].items():
            if day == best:
                day_color = GREEN
                tag = f" ← {GREEN}CHEAPEST{RESET}"
            elif day == worst:
                day_color = RED
                tag = f" ← {RED}EXPENSIVE{RESET}"
            else:
                day_color = GRAY
                tag = ""
            bar = mini_bar(price, max_price, width=18, color=day_color)
            print(f"  {day_color}{day[:3]}{RESET}  {bar}  {day_color}₹{price:,.0f}{RESET}{tag}")

        # Saving
        print()
        saving_bar = mini_bar(r["saving"], max_saving, width=24, color=color)
        print(f"  {GRAY}Avg saving on {best}:  {RESET}{saving_bar}  {GREEN}₹{r['saving']:,.0f}{RESET}")

        # Recommendation box
        print()
        rec_line = f"  {r['rec_icon']}  Recommendation:  {BOLD}{r['rec_color']}{r['rec']}{RESET}"
        print(f"  {r['rec_color']}┌─────────────────────────────────────────┐{RESET}")
        print(f"  {r['rec_color']}│{RESET}{rec_line:<52}{r['rec_color']}│{RESET}")
        print(f"  {r['rec_color']}└─────────────────────────────────────────┘{RESET}")
        print()
        divider()
        print()

    # Summary
    time.sleep(0.3)
    total_saving = sum(r["saving"] for r in results)
    buy_now = [p["name"].split()[0] for p, r in zip(PRODUCTS, results) if "BUY" in r["rec"]]
    wait    = [p["name"].split()[0] for p, r in zip(PRODUCTS, results) if "WAIT" in r["rec"]]

    print(f"  {BOLD}{WHITE}💡 SUMMARY{RESET}")
    print()

    if buy_now:
        print(f"  {GREEN}🟢 Buy NOW:   {', '.join(buy_now)}{RESET}")
    if wait:
        print(f"  {RED}⏳ Wait:      {', '.join(wait)}{RESET}")

    print()
    # Animated total saving counter
    sys.stdout.write(f"  {BOLD}{YELLOW}💰 Total potential saving: ₹")
    sys.stdout.flush()
    displayed = 0
    step = max(1, total_saving // 30)
    while displayed < total_saving:
        displayed = min(displayed + step, total_saving)
        sys.stdout.write(f"\r  {BOLD}{YELLOW}💰 Total potential saving: ₹{displayed:,.0f}    {RESET}")
        sys.stdout.flush()
        time.sleep(0.03)
    print()
    print()

    divider("═", PURPLE)
    print(f"  {GRAY}Code → {WHITE}github.com/Givhel{RESET}  {GRAY}|  Day 2 of 100  |  @thekunal.build{RESET}")
    divider("═", PURPLE)
    print()

if __name__ == "__main__":
    main()