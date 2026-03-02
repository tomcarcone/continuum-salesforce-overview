#!/usr/bin/env python3
"""Fix incorrectly assigned alt text (Winter weather bug from 'ice' substring matching)."""

import json
import urllib.request
import urllib.error
import time
import re

API_TOKEN = "fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6"
BASE_URL = "https://api.webflow.com/v2"
KNOWLEDGE_HUB_COLLECTION = "64c94b2afdeb6fdbaf3b2bd4"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json"
}


def api_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** (attempt + 2))
            else:
                return None
        except:
            time.sleep(2)
    return None


def api_patch(path, data):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="PATCH")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** (attempt + 2))
            else:
                return None
        except:
            time.sleep(2)
    return None


def generate_correct_alt(title):
    """Generate alt text with proper word boundary matching."""
    t = title.lower()
    
    # Use word boundary regex for short keywords that could match inside other words
    def word_match(keyword, text):
        return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text))
    
    if any(word_match(k, t) for k in ["hvac", "heating", "cooling", "air conditioning", "furnace"]):
        return "HVAC system maintenance and climate control equipment in a rental property"
    if any(word_match(k, t) for k in ["pool", "swimming"]):
        return "Community swimming pool area managed by an HOA in a residential neighborhood"
    if any(word_match(k, t) for k in ["roof", "gutter"]):
        return "Property roof inspection and maintenance on a residential rental home"
    if any(word_match(k, t) for k in ["plumbing", "pipe", "water heater", "drain"]):
        return "Plumbing repair and water system maintenance in a managed rental property"
    if any(word_match(k, t) for k in ["garage", "parking"]):
        return "Residential garage and parking area at a professionally managed property"
    if any(word_match(k, t) for k in ["landscap", "lawn", "garden", "tree", "curb appeal"]):
        return "Professionally landscaped yard and curb appeal at a managed residential property"
    # FIX: Use word boundaries for "ice" and "snow" to avoid matching "practice", "service", etc.
    if any(word_match(k, t) for k in ["snow", "winter", "freeze", "ice", "cold weather"]):
        return "Winter weather property maintenance and snow removal at a residential home"
    if any(word_match(k, t) for k in ["storm", "hurricane", "weather", "disaster", "emergency", "flood"]):
        return "Emergency property damage assessment and storm preparation for rental homes"
    if any(word_match(k, t) for k in ["fire", "smoke detector", "carbon monoxide", "safety"]):
        return "Fire safety equipment inspection and smoke detector in a rental property"
    if any(word_match(k, t) for k in ["mold", "moisture", "water damage"]):
        return "Mold inspection and water damage assessment in a managed rental property"
    if any(word_match(k, t) for k in ["pest", "bedbug", "bed bug", "termite", "roach", "rodent"]):
        return "Pest control inspection and treatment at a residential rental property"
    if any(word_match(k, t) for k in ["electric", "wiring", "outlet", "lighting"]):
        return "Electrical system inspection and lighting upgrades in a rental property"
    if any(word_match(k, t) for k in ["solar", "energy efficient", "green", "sustainability"]):
        return "Energy-efficient upgrades and sustainable features in a modern rental property"
    if any(word_match(k, t) for k in ["paint", "renovation", "remodel", "upgrade", "improvement", "flooring"]):
        return "Home renovation and interior upgrades at a residential rental property"
    if any(word_match(k, t) for k in ["appliance", "washer", "dryer", "dishwasher"]):
        return "Modern appliances in a well-maintained rental property kitchen"

    if any(k in t for k in ["hoa board", "board member"]):
        return "HOA board members discussing community governance at an association meeting"
    if any(k in t for k in ["hoa election", "hoa vote", "hoa ballot"]):
        return "HOA board election and community voting process at an association meeting"
    if any(k in t for k in ["hoa budget", "hoa financial", "hoa reserve", "reserve fund", "special assessment"]):
        return "HOA financial planning documents and community association budget analysis"
    if any(k in t for k in ["hoa vendor", "hoa contract"]):
        return "HOA board reviewing vendor proposals and service contracts for the community"
    if any(k in t for k in ["hoa rule", "hoa enforcement", "hoa violation", "hoa fine", "hoa compliance"]):
        return "Community association rule enforcement and compliance documentation"
    if any(k in t for k in ["hoa insurance", "hoa liability"]):
        return "HOA insurance policy review and community liability coverage documents"
    if any(k in t for k in ["hoa meeting", "annual meeting"]):
        return "Community residents attending an HOA annual meeting and governance session"
    if any(k in t for k in ["hoa social", "hoa event", "community event"]):
        return "Residents gathering at a community social event organized by the HOA"
    if any(k in t for k in ["hoa pet", "hoa animal"]):
        return "Pet policy signage in an HOA-managed residential community"
    if any(k in t for k in ["hoa management", "association management", "self-managed", "management company", "management contract"]):
        return "Professional community association management team serving an HOA"
    if any(k in t for k in ["hoa dues", "hoa collection", "delinquent", "hoa fee", "hoa assessment"]):
        return "HOA financial documents and assessment collection notices for community management"
    if any(k in t for k in ["violation", "notice"]):
        return "Property compliance notice and violation documentation for community management"
    if any(k in t for k in ["hoa", "homeowner association", "community association", "condo association"]):
        return "Well-maintained community managed by a homeowners association in the DC area"

    if any(k in t for k in ["tenant screen", "background check", "credit check", "application"]):
        return "Tenant screening application and background check documents for property management"
    if any(k in t for k in ["tenant rights", "renter rights", "fair housing"]):
        return "Tenant rights documentation and fair housing compliance guidelines"
    if any(k in t for k in ["security deposit", "move-out"]):
        return "Security deposit documentation and property move-out inspection checklist"
    if any(k in t for k in ["evict", "eviction"]):
        return "Legal eviction process documentation for property management compliance"
    if any(k in t for k in ["noise", "complaint", "neighbor dispute"]):
        return "Property manager addressing tenant concerns and resolving rental disputes"
    if any(k in t for k in ["welcome packet", "move-in", "new tenant"]):
        return "New tenant welcome materials and move-in documentation for a rental property"
    if any(k in t for k in ["lease", "rental agreement", "rent increase", "renewal"]):
        return "Rental lease agreement documents reviewed by a professional property manager"
    if any(k in t for k in ["tenant", "renter"]):
        return "Professional property manager working with tenants at a managed rental"

    if any(k in t for k in ["tax", "1099", "deduction", "depreciation"]):
        return "Rental property tax documents and financial records for landlord tax preparation"
    if any(k in t for k in ["insurance", "liability", "coverage"]):
        return "Property insurance policy documents and coverage review for rental owners"
    if any(k in t for k in ["roi", "return on investment", "cash flow", "profit"]):
        return "Investment property financial analysis showing rental income and ROI projections"
    if any(k in t for k in ["vacancy", "vacant", "marketing", "listing", "advertising"]):
        return "Rental property marketing and listing strategy to minimize vacancy"
    if any(k in t for k in ["license", "licensing", "permit"]):
        return "Rental property licensing and permit compliance documentation"
    if any(k in t for k in ["property manager", "hire", "interview"]):
        return "Property owner meeting with a professional property management company"
    if any(k in t for k in ["landlord"]):
        return "Landlord reviewing property management documents with a professional advisor"

    if any(k in t for k in ["invest", "foreclosure", "flip", "wholesale", "portfolio"]):
        return "Real estate investment property analysis and financial evaluation documents"
    if any(k in t for k in ["commercial", "office", "retail"]):
        return "Commercial property building managed by a professional management company"
    if any(k in t for k in ["buy", "buyer", "purchase", "closing cost", "first-time"]):
        return "Home buyer reviewing real estate purchase documents with a licensed realtor"
    if any(k in t for k in ["sell", "seller", "staging", "home value", "appraisal"]):
        return "Home seller preparing property for sale with staging and valuation"
    if any(k in t for k in ["condo", "condominium", "co-op", "townhouse"]):
        return "Condominium building in the Washington DC metropolitan area"
    if any(k in t for k in ["law", "legal", "regulation", "ordinance", "rent control", "compliance"]):
        return "Legal compliance documents and regulatory guidelines for property management"
    if any(k in t for k in ["pet", "animal", "dog", "cat", "esa"]):
        return "Pet-friendly rental property with pet policy guidelines for tenants"
    if any(k in t for k in ["technology", "smart home", "software", "app"]):
        return "Smart home technology and property management software in a modern rental"
    if any(k in t for k in ["vacation", "short-term", "airbnb"]):
        return "Short-term vacation rental property in the Washington DC metropolitan area"
    if any(k in t for k in ["subdivision", "subdivide", "zoning", "adu"]):
        return "Residential property with development and subdivision potential"
    if any(k in t for k in ["maintenance", "repair", "handyman", "work order", "support service"]):
        return "Property maintenance technician performing repairs at a managed rental"
    if any(k in t for k in ["washington", " dc", "virginia", "maryland"]):
        return "Residential neighborhood in the Washington DC metropolitan area"
    if any(k in t for k in ["market", "trend", "forecast", "report"]):
        return "Washington DC real estate market analysis and rental trend data"
    if "vice president" in t:
        return "HOA board vice president contributing to community association governance"

    short_title = title[:80] if len(title) <= 80 else title[:77] + "..."
    return f"Property management article illustration - {short_title}"


def main():
    print("Scanning for incorrectly assigned alt text...", flush=True)
    
    # Get all items
    items = []
    offset = 0
    while True:
        data = api_get(f"/collections/{KNOWLEDGE_HUB_COLLECTION}/items?limit=100&offset={offset}")
        if not data or not data.get("items"):
            break
        items.extend(data["items"])
        total = data["pagination"]["total"]
        offset += len(data["items"])
        if offset >= total:
            break
        time.sleep(1)
    
    print(f"Total items: {len(items)}", flush=True)
    
    # Find items with incorrect "Winter weather" alt text
    to_fix = []
    for item in items:
        img = item["fieldData"].get("main-image", {})
        if not img or not img.get("alt"):
            continue
        alt = img["alt"]
        title = item["fieldData"].get("name", "")
        t = title.lower()
        
        # Check if "Winter weather" was incorrectly assigned
        if "Winter weather" in alt:
            # Only correct if the title doesn't actually contain winter-related words
            if not any(re.search(r'\b' + re.escape(k) + r'\b', t) for k in ["snow", "winter", "freeze", "ice", "cold weather", "winterize"]):
                correct_alt = generate_correct_alt(title)
                to_fix.append({
                    "id": item["id"],
                    "title": title,
                    "current_alt": alt,
                    "correct_alt": correct_alt,
                    "url": img["url"]
                })
    
    print(f"\nFound {len(to_fix)} items to fix:", flush=True)
    for item in to_fix:
        print(f"  {item['title'][:60]}", flush=True)
        print(f"    Current: {item['current_alt'][:60]}", flush=True)
        print(f"    Fix to:  {item['correct_alt'][:60]}", flush=True)
    
    if not to_fix:
        print("Nothing to fix!", flush=True)
        return
    
    print(f"\nApplying fixes...", flush=True)
    for idx, item in enumerate(to_fix):
        data = {
            "fieldData": {
                "main-image": {
                    "url": item["url"],
                    "alt": item["correct_alt"]
                }
            }
        }
        result = api_patch(f"/collections/{KNOWLEDGE_HUB_COLLECTION}/items/{item['id']}", data)
        status = "OK" if result else "FAIL"
        print(f"  [{idx+1}/{len(to_fix)}] {status}: {item['title'][:50]}", flush=True)
        time.sleep(1.1)
    
    print("\nFix complete!", flush=True)


if __name__ == "__main__":
    main()
