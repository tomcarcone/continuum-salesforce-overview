#!/usr/bin/env python3
"""
Batch alt text updater - processes items that still have null alt text.
Uses 1-second delay between requests to respect Webflow rate limits.
"""

import json
import urllib.request
import urllib.error
import time
import re
import sys

API_TOKEN = "fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6"
BASE_URL = "https://api.webflow.com/v2"
KNOWLEDGE_HUB_COLLECTION = "64c94b2afdeb6fdbaf3b2bd4"
NEIGHBORHOODS_COLLECTION = "64c94b2afdeb6fdbaf3b2bd0"

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
                wait = 2 ** (attempt + 2)
                print(f"    Rate limited on GET, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"    GET error {e.code}", flush=True)
                return None
        except Exception as e:
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
                wait = 2 ** (attempt + 2)
                print(f"    Rate limited on PATCH, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                err = e.read().decode()[:200]
                print(f"    PATCH error {e.code}: {err}", flush=True)
                return None
        except Exception as e:
            time.sleep(2)
    return None


def get_all_items(collection_id):
    items = []
    offset = 0
    while True:
        data = api_get(f"/collections/{collection_id}/items?limit=100&offset={offset}")
        if not data or not data.get("items"):
            break
        items.extend(data["items"])
        total = data["pagination"]["total"]
        offset += len(data["items"])
        if offset >= total:
            break
        time.sleep(1)
    return items


def generate_alt(title):
    """Generate alt text based on article title keywords."""
    t = title.lower()

    if any(k in t for k in ["hvac", "heating", "cooling", "air condition", "furnace"]):
        return "HVAC system maintenance and climate control equipment in a rental property"
    if any(k in t for k in ["pool", "swimming"]):
        return "Community swimming pool area managed by an HOA in a residential neighborhood"
    if any(k in t for k in ["roof", "gutter"]):
        return "Property roof inspection and maintenance on a residential rental home"
    if any(k in t for k in ["plumbing", "pipe", "water heater", "drain"]):
        return "Plumbing repair and water system maintenance in a managed rental property"
    if any(k in t for k in ["garage", "parking"]):
        return "Residential garage and parking area at a professionally managed property"
    if any(k in t for k in ["landscap", "lawn", "garden", "tree", "curb appeal"]):
        return "Professionally landscaped yard and curb appeal at a managed residential property"
    if any(k in t for k in ["snow", "winter", "freeze", "ice", "cold weather"]):
        return "Winter weather property maintenance and snow removal at a residential home"
    if any(k in t for k in ["storm", "hurricane", "weather", "disaster", "emergency", "flood"]):
        return "Emergency property damage assessment and storm preparation for rental homes"
    if any(k in t for k in ["fire", "smoke detector", "carbon monoxide", "safety"]):
        return "Fire safety equipment inspection and smoke detector in a rental property"
    if any(k in t for k in ["mold", "moisture", "water damage"]):
        return "Mold inspection and water damage assessment in a managed rental property"
    if any(k in t for k in ["pest", "bedbug", "bed bug", "termite", "roach", "rodent", "mice"]):
        return "Pest control inspection and treatment at a residential rental property"
    if any(k in t for k in ["electric", "wiring", "outlet", "lighting"]):
        return "Electrical system inspection and lighting upgrades in a rental property"
    if any(k in t for k in ["solar", "energy efficien", "green", "sustainability", "ev ", "electric vehicle"]):
        return "Energy-efficient upgrades and sustainable features in a modern rental property"
    if any(k in t for k in ["paint", "renovation", "remodel", "upgrade", "improvement", "flooring"]):
        return "Home renovation and interior upgrades at a residential rental property"
    if any(k in t for k in ["appliance", "washer", "dryer", "dishwasher", "refrigerator"]):
        return "Modern appliances in a well-maintained rental property kitchen"

    if any(k in t for k in ["hoa board", "board member", "board meeting"]):
        return "HOA board members discussing community governance at an association meeting"
    if any(k in t for k in ["hoa election", "hoa vote", "hoa ballot"]):
        return "HOA board election and community voting process at an association meeting"
    if "hoa budget" in t or "hoa financial" in t or "hoa reserve" in t or "reserve fund" in t or "special assessment" in t:
        return "HOA financial planning documents and community association budget analysis"
    if any(k in t for k in ["hoa vendor", "hoa contract"]):
        return "HOA board reviewing vendor proposals and service contracts for the community"
    if any(k in t for k in ["hoa rule", "hoa enforcement", "hoa violation", "hoa fine", "hoa compliance"]):
        return "Community association rule enforcement and compliance documentation"
    if any(k in t for k in ["hoa insurance", "hoa liability"]):
        return "HOA insurance policy review and community liability coverage documents"
    if any(k in t for k in ["hoa meeting", "annual meeting"]):
        return "Community residents attending an HOA annual meeting and governance session"
    if any(k in t for k in ["hoa social", "hoa event", "community event", "neighborhood event"]):
        return "Residents gathering at a community social event organized by the HOA"
    if any(k in t for k in ["hoa pet", "hoa animal"]):
        return "Pet policy signage in an HOA-managed residential community"
    if any(k in t for k in ["hoa management", "association management", "self-managed", "management company", "management contract"]):
        return "Professional community association management team serving an HOA"
    if any(k in t for k in ["hoa dues", "hoa collection", "delinquent", "hoa fee", "hoa assessment"]):
        return "HOA financial documents and assessment collection notices for community management"
    if any(k in t for k in ["hoa", "homeowner association", "community association", "condo association"]):
        return "Well-maintained community managed by a homeowners association in the DC area"

    if any(k in t for k in ["tenant screen", "background check", "credit check", "application"]):
        return "Tenant screening application and background check documents for property management"
    if any(k in t for k in ["tenant rights", "renter rights", "fair housing"]):
        return "Tenant rights documentation and fair housing compliance guidelines"
    if any(k in t for k in ["security deposit", "move-out", "move out"]):
        return "Security deposit documentation and property move-out inspection checklist"
    if any(k in t for k in ["evict", "eviction"]):
        return "Legal eviction process documentation for property management compliance"
    if any(k in t for k in ["noise", "complaint", "neighbor dispute"]):
        return "Property manager addressing tenant concerns and resolving rental disputes"
    if any(k in t for k in ["welcome packet", "move-in", "move in", "new tenant"]):
        return "New tenant welcome materials and move-in documentation for a rental property"
    if any(k in t for k in ["lease", "rental agreement", "rent increase", "renewal"]):
        return "Rental lease agreement documents reviewed by a professional property manager"
    if any(k in t for k in ["prorate", "rent calculation"]):
        return "Rental payment calculation and prorated rent documentation"
    if any(k in t for k in ["tenant", "renter"]):
        return "Professional property manager working with tenants at a managed rental"

    if any(k in t for k in ["tax", "1099", "deduction", "depreciation"]):
        return "Rental property tax documents and financial records for landlord tax preparation"
    if any(k in t for k in ["insurance", "liability", "coverage"]):
        return "Property insurance policy documents and coverage review for rental owners"
    if any(k in t for k in ["roi", "return on investment", "cash flow", "profit", "income"]):
        return "Investment property financial analysis showing rental income and ROI projections"
    if any(k in t for k in ["vacancy", "vacant", "marketing", "listing", "advertising"]):
        return "Rental property marketing and listing strategy to minimize vacancy"
    if any(k in t for k in ["property manager", "management company", "hire", "interview"]):
        return "Property owner meeting with a professional property management company"
    if any(k in t for k in ["landlord"]):
        return "Landlord reviewing property management documents with a professional advisor"

    if any(k in t for k in ["invest", "foreclosure", "flip", "wholesale", "portfolio"]):
        return "Real estate investment property analysis and financial evaluation documents"
    if any(k in t for k in ["commercial", "office", "retail", "industrial"]):
        return "Commercial property building managed by a professional management company"
    if any(k in t for k in ["buy", "buyer", "purchase", "closing cost", "first-time", "home search"]):
        return "Home buyer reviewing real estate purchase documents with a licensed realtor"
    if any(k in t for k in ["sell", "seller", "staging", "home value", "appraisal"]):
        return "Home seller preparing property for sale with staging and valuation"
    if any(k in t for k in ["condo", "condominium", "co-op", "townhouse"]):
        return "Condominium building in the Washington DC metropolitan area"

    if any(k in t for k in ["law", "legal", "regulation", "ordinance", "rent control", "code", "compliance"]):
        return "Legal compliance documents and regulatory guidelines for property management"
    if any(k in t for k in ["pet", "animal", "dog", "cat", "esa", "service animal"]):
        return "Pet-friendly rental property with pet policy guidelines for tenants"
    if any(k in t for k in ["technology", "smart home", "software", "app", "iot"]):
        return "Smart home technology and property management software in a modern rental"
    if any(k in t for k in ["vacation", "short-term", "airbnb", "vrbo"]):
        return "Short-term vacation rental property in the Washington DC metropolitan area"
    if any(k in t for k in ["subdivision", "subdivide", "zoning", "adu"]):
        return "Residential property with development and subdivision potential"
    if any(k in t for k in ["washington", " dc", "virginia", "maryland", "arlington", "bethesda"]):
        return "Residential neighborhood in the Washington DC metropolitan area"
    if any(k in t for k in ["market", "trend", "forecast", "report"]):
        return "Washington DC real estate market analysis and rental trend data"
    if any(k in t for k in ["maintenance", "repair", "handyman", "work order"]):
        return "Property maintenance technician performing repairs at a managed rental"

    # Descriptive fallback using the title
    short_title = title[:80] if len(title) <= 80 else title[:77] + "..."
    return f"Property management article illustration - {short_title}"


NEIGHBORHOOD_ALTS = {
    "Georgetown": "Historic Georgetown neighborhood with Federal-style townhouses and tree-lined cobblestone streets in Washington DC",
    "Capitol Hill": "Capitol Hill neighborhood featuring historic rowhouses near the United States Capitol building in Washington DC",
    "Logan Circle": "Victorian-era rowhouses surrounding Logan Circle park in Northwest Washington DC",
    "Kalorama": "Stately embassy residences and luxury homes in the Kalorama neighborhood of Washington DC",
    "U Street Corridor": "Vibrant U Street Corridor with historic music venues and colorful rowhouses in Washington DC",
    "Arlington": "Arlington Virginia skyline with residential neighborhoods near Washington DC",
    "Ballston": "Modern mixed-use development and residential buildings in Ballston Arlington Virginia",
    "Clarendon-Courthouse": "Walkable Clarendon-Courthouse neighborhood with shops and restaurants in Arlington Virginia",
    "Rosslyn": "Rosslyn Virginia skyline with high-rise buildings overlooking the Potomac River and Washington DC",
    "Barcroft": "Quiet residential streets with single-family homes in the Barcroft neighborhood of Arlington Virginia",
    "Seven Corners": "Seven Corners commercial and residential area at the crossroads of Falls Church and Arlington Virginia",
    "Shirlington": "Shirlington Village with pedestrian-friendly streets and local businesses in Arlington Virginia",
    "Falls Church": "Tree-lined residential streets with charming homes in Falls Church Virginia",
    "Alexandria Old Town": "Historic cobblestone streets and waterfront dining in Old Town Alexandria Virginia",
    "McLean": "Luxury estate homes and lush green landscapes in McLean Virginia",
    "Silver Spring": "Downtown Silver Spring Maryland with urban amenities and diverse dining options",
    "Bethesda": "Upscale Bethesda Maryland downtown with shops restaurants and residential high-rises",
    "Takoma Park": "Eclectic and colorful homes in the arts-friendly Takoma Park Maryland neighborhood",
    "Hyattsville": "Revitalized arts district and residential community in Hyattsville Maryland",
    "Penn Quarter-Chinatown": "Penn Quarter and Chinatown neighborhood with the Friendship Arch and cultural venues in Washington DC",
    "Dupont Circle": "Dupont Circle fountain surrounded by historic townhouses and embassies in Washington DC",
    "Tenleytown": "Family-friendly Tenleytown neighborhood with residential homes near American University in Washington DC",
    "Columbia Heights": "Diverse Columbia Heights neighborhood with colorful murals and urban living in Washington DC",
    "Adams Morgan": "Eclectic Adams Morgan neighborhood known for international dining and vibrant nightlife in Washington DC",
    "Southwest Waterfront Navy Yard": "The Wharf waterfront development and Navy Yard neighborhood along the Anacostia River in Washington DC",
    "H Street Corridor": "Revitalized H Street NE corridor with local shops and the DC Streetcar in Washington DC",
    "NoMa": "Modern NoMa neighborhood with new residential development north of Massachusetts Avenue in Washington DC"
}


def process_collection(collection_id, image_field, mode):
    """Process a collection, updating only items with null alt text."""
    print(f"\nFetching items...", flush=True)
    items = get_all_items(collection_id)
    needs_update = [i for i in items if i["fieldData"].get(image_field) and not i["fieldData"][image_field].get("alt")]
    print(f"Total: {len(items)} | Need update: {len(needs_update)} | Already done: {len(items) - len(needs_update)}", flush=True)

    success = 0
    failed = 0
    results = []

    for idx, item in enumerate(needs_update):
        title = item["fieldData"].get("name", "Unknown")
        image = item["fieldData"][image_field]

        if mode == "knowledge_hub":
            alt = generate_alt(title)
        else:
            alt = NEIGHBORHOOD_ALTS.get(title, f"Scenic view of {title} neighborhood in the Washington DC area")

        data = {"fieldData": {image_field: {"url": image["url"], "alt": alt}}}

        print(f"  [{idx+1}/{len(needs_update)}] {title[:55]} -> {alt[:55]}...", flush=True)

        result = api_patch(f"/collections/{collection_id}/items/{item['id']}", data)
        if result:
            success += 1
            results.append({"title": title, "alt": alt, "status": "ok"})
        else:
            failed += 1
            results.append({"title": title, "alt": alt, "status": "fail"})

        time.sleep(1.1)

    print(f"\nDone: {success} updated, {failed} failed", flush=True)
    return results


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "kb"):
        print("=" * 60, flush=True)
        print("KNOWLEDGE HUB - Alt Text Updates", flush=True)
        print("=" * 60, flush=True)
        kb_results = process_collection(KNOWLEDGE_HUB_COLLECTION, "main-image", "knowledge_hub")

    if mode in ("all", "nb"):
        print("\n" + "=" * 60, flush=True)
        print("NEIGHBORHOODS - Alt Text Updates", flush=True)
        print("=" * 60, flush=True)
        nb_results = process_collection(NEIGHBORHOODS_COLLECTION, "featured-header-image", "neighborhoods")

    if mode in ("all", "meta"):
        print("\n" + "=" * 60, flush=True)
        print("FIXING MISSING META DESCRIPTIONS", flush=True)
        print("=" * 60, flush=True)
        items = get_all_items(NEIGHBORHOODS_COLLECTION)
        fixes = {
            "Ballston": "Discover Ballston in Arlington, VA — a thriving urban village with modern apartments, top dining, and easy Metro access near Washington DC.",
            "Falls Church": "Explore Falls Church, VA — a charming small-city community with excellent schools, local shops, and easy access to Washington DC."
        }
        for item in items:
            name = item["fieldData"].get("name", "")
            if name in fixes and not item["fieldData"].get("summary-at-a-glance"):
                print(f"  Fixing: {name}", flush=True)
                result = api_patch(
                    f"/collections/{NEIGHBORHOODS_COLLECTION}/items/{item['id']}",
                    {"fieldData": {"summary-at-a-glance": fixes[name]}}
                )
                print(f"  -> {'SUCCESS' if result else 'FAILED'}", flush=True)
                time.sleep(1.1)

    print("\n\nALL COMPLETE!", flush=True)
