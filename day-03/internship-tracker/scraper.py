# scraper.py — Internshala Internship Tracker
# Day 3 of 100 Days — @thekunal.build
# Run: python scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# ─── COLORS ───────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
BOLD   = "\033[1m"
GRAY   = "\033[90m"
RESET  = "\033[0m"

COLORS = [CYAN, PURPLE, GREEN, YELLOW]

def spinner(text, duration=1.0, color=CYAN):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {color}{frames[i%len(frames)]}{RESET} {text}")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    sys.stdout.write(f"\r  {GREEN}✅{RESET} {text}\n")

def progress_bar(label, duration=0.6, color=CYAN, width=28):
    for i in range(width):
        time.sleep(duration / width)
        filled = "█" * (i + 1)
        empty  = "░" * (width - i - 1)
        pct    = int(((i + 1) / width) * 100)
        sys.stdout.write(
            f"\r  {label} [{color}{filled}{GRAY}{empty}{RESET}] {pct}%"
        )
        sys.stdout.flush()
    print()

def scrape_internshala(role="python developer", max_pages=2):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    role_slug = role.lower().replace(" ", "-")
    base_url  = f"https://internshala.com/internships/{role_slug}-internship"
    internships = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}/page-{page}" if page > 1 else base_url
        spinner(f"Scraping page {page}...", duration=1.2, color=CYAN)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup     = BeautifulSoup(response.text, "html.parser")
            cards    = soup.find_all("div", class_="individual_internship")

            for card in cards:
                try:
                    # Company name
                    company = card.find("p", class_="company-name")
                    company = company.text.strip() if company else "N/A"

                    # Job title
                    title = card.find("h3", class_="job-internship-name")
                    title = title.text.strip() if title else "N/A"

                    # Stipend
                    stipend = card.find("span", class_="stipend")
                    stipend = stipend.text.strip() if stipend else "Unpaid"

                    # Duration
                    duration_tag = card.find_all("div", class_="item_body")
                    duration = duration_tag[1].text.strip() if len(duration_tag) > 1 else "N/A"

                    # Location
                    location = card.find("p", class_="locations")
                    location = location.text.strip().replace("\n", "").replace(" ", "") if location else "Remote"

                    # Skills
                    skills_tag = card.find("div", class_="internship_other_details_container")
                    skills = skills_tag.text.strip() if skills_tag else "N/A"

                    # Apply link
                    link_tag = card.find("a", class_="view_detail_button")
                    link = "https://internshala.com" + link_tag["href"] if link_tag else "N/A"

                    internships.append({
                        "title":    title,
                        "company":  company,
                        "stipend":  stipend,
                        "duration": duration,
                        "location": location,
                        "skills":   skills,
                        "link":     link
                    })

                except Exception:
                    continue

            time.sleep(1)

        except Exception as e:
            print(f"  {YELLOW}⚠️ Error on page {page}: {e}{RESET}")
            continue

    return internships

def extract_skills(internships):
    """
    Extracts and counts skill frequency across all internships.
    """
    common_skills = [
        "python", "machine learning", "data analysis", "sql", "excel",
        "javascript", "react", "node", "django", "flask", "pandas",
        "numpy", "tensorflow", "pytorch", "nlp", "deep learning",
        "communication", "ms office", "java", "c++", "figma", "canva",
        "photoshop", "autocad", "r", "tableau", "power bi", "aws",
        "docker", "git", "mongodb", "mysql", "postgresql"
    ]

    skill_count = {skill: 0 for skill in common_skills}

    for intern in internships:
        text = (intern.get("skills", "") + " " + intern.get("title", "")).lower()
        for skill in common_skills:
            if skill in text:
                skill_count[skill] += 1

    # Remove zeros and sort
    skill_count = {k: v for k, v in skill_count.items() if v > 0}
    skill_count = dict(sorted(skill_count.items(), key=lambda x: x[1], reverse=True))
    return skill_count

def main():
    print()
    print(f"  {BOLD}{PURPLE}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"  {BOLD}{PURPLE}║   🔍  INTERNSHALA INTERNSHIP TRACKER            ║{RESET}")
    print(f"  {BOLD}{PURPLE}║   Built with Python + BeautifulSoup + Pandas    ║{RESET}")
    print(f"  {BOLD}{PURPLE}║   Day 3 of 100  |  @thekunal.build              ║{RESET}")
    print(f"  {BOLD}{PURPLE}╚══════════════════════════════════════════════════╝{RESET}")
    print()

    # Get role from user
    role = input(f"  {CYAN}Enter job role to search {GRAY}(e.g. python developer){RESET}: ").strip()
    if not role:
        role = "python developer"

    print()
    spinner("Connecting to Internshala...", 1.0, CYAN)
    spinner("Setting up scraper...", 0.8, PURPLE)
    print()

    print(f"  {BOLD}Scraping live internships for: {CYAN}{role}{RESET}")
    print()

    internships = scrape_internshala(role, max_pages=2)

    if not internships:
        print(f"\n  {YELLOW}⚠️  No results found. Try a different role.{RESET}\n")
        return

    print()
    print(f"  {GREEN}✅ Found {len(internships)} internships{RESET}")
    print()

    # Show results
    print(f"  {BOLD}{'─'*54}{RESET}")
    for i, intern in enumerate(internships[:10]):
        color = COLORS[i % len(COLORS)]
        print(f"\n  {color}{i+1:02d}. {intern['title']}{RESET}")
        print(f"      {GRAY}Company:{RESET}  {intern['company']}")
        print(f"      {GRAY}Stipend:{RESET}  {GREEN}{intern['stipend']}{RESET}")
        print(f"      {GRAY}Duration:{RESET} {intern['duration']}")
        print(f"      {GRAY}Location:{RESET} {intern['location']}")
        time.sleep(0.15)

    # Skills analysis
    print()
    print(f"  {'─'*54}")
    print(f"\n  {BOLD}{YELLOW}📊 TOP SKILLS COMPANIES ARE ASKING FOR:{RESET}\n")

    skills = extract_skills(internships)
    top_skills = list(skills.items())[:8]
    max_count  = top_skills[0][1] if top_skills else 1

    for skill, count in top_skills:
        bar_len  = int((count / max_count) * 24)
        bar      = "█" * bar_len + "░" * (24 - bar_len)
        pct      = int((count / len(internships)) * 100)
        color    = GREEN if pct > 50 else YELLOW if pct > 25 else GRAY
        print(f"  {color}{skill:<20}{RESET} {color}{bar}{RESET}  {pct}%")
        time.sleep(0.1)

    # Save to CSV
    print()
    df = pd.DataFrame(internships)
    df.to_csv("internships.csv", index=False)
    print(f"  {GREEN}✅ Saved to internships.csv{RESET}")

    print()
    print(f"  {'═'*54}")
    print(f"  {GRAY}Run dashboard: {CYAN}streamlit run dashboard.py{RESET}")
    print(f"  {GRAY}Code: {CYAN}github.com/Givhel{RESET}  |  Day 3 of 100")
    print(f"  {'═'*54}\n")

if __name__ == "__main__":
    main()