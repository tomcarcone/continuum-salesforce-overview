#!/usr/bin/env python3
"""
Gordon James Realty - Full SEO Audit Update Script
Runs ALL audit-recommended changes via Webflow API v2:
  1. CMS alt text for Knowledge Hub + Neighborhoods
  2. Fix incorrectly assigned alt text (ice/winter substring bug)
  3. Service page meta descriptions (summary-text field)
  4. Static page meta descriptions
  5. Fix About Us typo
  6. Publish all changes
"""

import json
import urllib.request
import urllib.error
import time
import re
import sys

API_TOKEN = "fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6"
BASE_URL = "https://api.webflow.com/v2"
SITE_ID = "64c94b2afdeb6fdbaf3b2b58"
KNOWLEDGE_HUB_COLLECTION = "64c94b2afdeb6fdbaf3b2bd4"
NEIGHBORHOODS_COLLECTION = "64c94b2afdeb6fdbaf3b2bd0"
SERVICES_COLLECTION = "64c94b2afdeb6fdbaf3b2b7f"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json"
}

REQUEST_DELAY = 1.1
stats = {"api_calls": 0, "updates": 0, "skips": 0, "errors": 0}


def api_request(method, path, data=None):
    """Make an API request with retry logic."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    stats["api_calls"] += 1

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 2)
                print(f"    Rate limited, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                err = e.read().decode()[:200]
                print(f"    HTTP {e.code}: {err}", flush=True)
                stats["errors"] += 1
                return None
        except urllib.error.URLError as e:
            wait = 2 ** (attempt + 1)
            print(f"    Network error, retrying in {wait}s: {e}", flush=True)
            time.sleep(wait)
    stats["errors"] += 1
    return None


def get_all_items(collection_id):
    """Fetch all items from a collection with pagination."""
    items = []
    offset = 0
    while True:
        data = api_request("GET", f"/collections/{collection_id}/items?limit=100&offset={offset}")
        if not data or not data.get("items"):
            break
        items.extend(data["items"])
        total = data["pagination"]["total"]
        offset += len(data["items"])
        if offset >= total:
            break
        time.sleep(REQUEST_DELAY)
    return items


# ---------------------------------------------------------------------------
# STEP 1: Alt text generation (from batch_alt_update.py with fix_alt_text.py improvements)
# ---------------------------------------------------------------------------

def word_match(keyword, text):
    return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text))


def generate_kb_alt(title):
    """Generate alt text with proper word boundary matching."""
    t = title.lower()

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
    if any(k in t for k in ["hoa election", "hoa vote"]):
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


# ---------------------------------------------------------------------------
# STEP 3: Service page meta descriptions
# ---------------------------------------------------------------------------

SERVICE_META_DESCRIPTIONS = {
    "residential-property-management": "Professional residential property management in Washington DC, Virginia, and Maryland. Tenant screening, rent collection, maintenance coordination, and full-service landlord support from Gordon James Realty.",
    "commercial-property-management": "Expert commercial property management in the DC metro area. Maximize occupancy rates, streamline operations, and grow your portfolio with Gordon James Realty.",
    "community-association-management": "HOA and community association management in Washington DC, Virginia, and Maryland. Board support, financial oversight, and vendor management with 50+ years combined experience.",
    "buying-a-property": "Buy residential or commercial property in Washington DC, Virginia, or Maryland with Gordon James Realty. Expert buyer representation, neighborhood guides, and market insight.",
    "selling-a-property": "Sell your property faster with Gordon James Realty brokerage services in Washington DC. Professional marketing, pricing strategy, and full-service real estate representation.",
    "hoa": "Professional HOA management services in Washington DC, Virginia, and Maryland. Comprehensive board support, vendor management, and community governance from Gordon James Realty.",
    "hoa-2": "Professional HOA management services in Washington DC, Virginia, and Maryland. Comprehensive board support, vendor management, and community governance from Gordon James Realty.",
    "landlords-corner": "Resources and expert guidance for landlords in the DC metro area. Property management tips, legal compliance, and investment strategies from Gordon James Realty.",
    "federal-section-management": "Federal contracting and property management services from Gordon James Realty. Specialized government property management in Washington DC, Virginia, and Maryland.",
}


# ---------------------------------------------------------------------------
# STEP 4: Static page meta descriptions
# ---------------------------------------------------------------------------

PAGE_SEO_UPDATES = {
    # About Us - fix typo + improve description
    "64c94b2afdeb6fdbaf3b2b92": {
        "seo": {
            "title": "About Us | Gordon James Realty",
            "description": "Learn about Gordon James Realty and our mission to empower individuals to achieve their real estate goals through expert property management and brokerage in Washington DC, Virginia, and Maryland."
        }
    },
    # Homepage - strengthen description
    "64c94b2afdeb6fdbaf3b2b57": {
        "seo": {
            "title": "Property Management & Real Estate Services in Washington DC | Gordon James Realty",
            "description": "Gordon James Realty provides full-service property management and real estate brokerage in Washington DC, Virginia, and Maryland. Residential, commercial, and HOA management with 50+ years combined experience."
        }
    },
    # Software and Support Services - keep existing but improve
    "65c51d6775f89b0b0774ca91": {
        "seo": {
            "title": "Property Management Software & Support Services | Gordon James Realty",
            "description": "Property management software and support services powered by Salesforce, Stripe, and DocuSign. 15-minute average response time for residents and owners in Washington DC, Virginia, and Maryland."
        }
    },
}


# ======================== MAIN EXECUTION ========================

def step1_cms_alt_text():
    """Update alt text for Knowledge Hub and Neighborhood CMS items."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 1: CMS Alt Text Updates", flush=True)
    print("=" * 70, flush=True)

    # --- Knowledge Hub ---
    print("\n--- Knowledge Hub ---", flush=True)
    items = get_all_items(KNOWLEDGE_HUB_COLLECTION)
    needs_update = [i for i in items if i["fieldData"].get("main-image") and not i["fieldData"]["main-image"].get("alt")]
    print(f"Total: {len(items)} | Need alt text: {len(needs_update)} | Already done: {len(items) - len(needs_update)}", flush=True)

    for idx, item in enumerate(needs_update):
        title = item["fieldData"].get("name", "Unknown")
        image = item["fieldData"]["main-image"]
        alt = generate_kb_alt(title)
        data = {"fieldData": {"main-image": {"url": image["url"], "alt": alt}}}
        print(f"  [{idx+1}/{len(needs_update)}] {title[:50]} -> {alt[:50]}...", flush=True)
        result = api_request("PATCH", f"/collections/{KNOWLEDGE_HUB_COLLECTION}/items/{item['id']}", data)
        if result:
            stats["updates"] += 1
        else:
            stats["errors"] += 1
        time.sleep(REQUEST_DELAY)

    # --- Neighborhoods ---
    print("\n--- Neighborhoods ---", flush=True)
    items = get_all_items(NEIGHBORHOODS_COLLECTION)
    needs_update = [i for i in items if i["fieldData"].get("featured-header-image") and not i["fieldData"]["featured-header-image"].get("alt")]
    print(f"Total: {len(items)} | Need alt text: {len(needs_update)} | Already done: {len(items) - len(needs_update)}", flush=True)

    for idx, item in enumerate(needs_update):
        name = item["fieldData"].get("name", "Unknown")
        image = item["fieldData"]["featured-header-image"]
        alt = NEIGHBORHOOD_ALTS.get(name, f"Scenic view of {name} neighborhood in the Washington DC area")
        data = {"fieldData": {"featured-header-image": {"url": image["url"], "alt": alt}}}
        print(f"  [{idx+1}/{len(needs_update)}] {name} -> {alt[:55]}...", flush=True)
        result = api_request("PATCH", f"/collections/{NEIGHBORHOODS_COLLECTION}/items/{item['id']}", data)
        if result:
            stats["updates"] += 1
        else:
            stats["errors"] += 1
        time.sleep(REQUEST_DELAY)


def step2_fix_winter_bug():
    """Fix incorrectly assigned 'Winter weather' alt text from ice/service substring matching."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 2: Fix Incorrect Alt Text (Winter/Ice Bug)", flush=True)
    print("=" * 70, flush=True)

    items = get_all_items(KNOWLEDGE_HUB_COLLECTION)
    to_fix = []
    for item in items:
        img = item["fieldData"].get("main-image", {})
        if not img or not img.get("alt"):
            continue
        alt = img["alt"]
        title = item["fieldData"].get("name", "")
        t = title.lower()
        if "Winter weather" in alt:
            if not any(re.search(r'\b' + re.escape(k) + r'\b', t) for k in ["snow", "winter", "freeze", "ice", "cold weather", "winterize"]):
                correct_alt = generate_kb_alt(title)
                to_fix.append({"id": item["id"], "title": title, "correct_alt": correct_alt, "url": img["url"]})

    print(f"Found {len(to_fix)} items with incorrect winter alt text", flush=True)
    for idx, item in enumerate(to_fix):
        data = {"fieldData": {"main-image": {"url": item["url"], "alt": item["correct_alt"]}}}
        print(f"  [{idx+1}/{len(to_fix)}] FIX: {item['title'][:50]} -> {item['correct_alt'][:50]}...", flush=True)
        result = api_request("PATCH", f"/collections/{KNOWLEDGE_HUB_COLLECTION}/items/{item['id']}", data)
        if result:
            stats["updates"] += 1
        else:
            stats["errors"] += 1
        time.sleep(REQUEST_DELAY)


def step3_service_meta_descriptions():
    """Update service page meta descriptions via CMS summary-text field."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 3: Service Page Meta Descriptions", flush=True)
    print("=" * 70, flush=True)

    items = get_all_items(SERVICES_COLLECTION)
    for item in items:
        slug = item["fieldData"].get("slug", "")
        name = item["fieldData"].get("name", "?")
        current = item["fieldData"].get("summary-text", "")

        if slug in SERVICE_META_DESCRIPTIONS:
            new_desc = SERVICE_META_DESCRIPTIONS[slug]
            # Only update if missing or significantly shorter
            if not current or len(current.strip()) < 50:
                print(f"  UPDATE: {name} (/{slug})", flush=True)
                print(f"    New: {new_desc[:80]}...", flush=True)
                data = {"fieldData": {"summary-text": new_desc}}
                result = api_request("PATCH", f"/collections/{SERVICES_COLLECTION}/items/{item['id']}", data)
                if result:
                    stats["updates"] += 1
                else:
                    stats["errors"] += 1
                time.sleep(REQUEST_DELAY)
            else:
                print(f"  SKIP (has desc): {name}", flush=True)
                stats["skips"] += 1


def step4_static_page_seo():
    """Update static page SEO titles and descriptions."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 4: Static Page SEO Updates", flush=True)
    print("=" * 70, flush=True)

    for page_id, update_data in PAGE_SEO_UPDATES.items():
        print(f"  Updating page {page_id}...", flush=True)
        print(f"    Title: {update_data['seo']['title']}", flush=True)
        print(f"    Desc: {update_data['seo']['description'][:80]}...", flush=True)
        result = api_request("PUT", f"/pages/{page_id}", update_data)
        if result:
            stats["updates"] += 1
            print(f"    SUCCESS", flush=True)
        else:
            stats["errors"] += 1
            print(f"    FAILED", flush=True)
        time.sleep(REQUEST_DELAY)


def step5_neighborhood_meta_fixes():
    """Fix missing meta descriptions for Ballston and Falls Church."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 5: Neighborhood Meta Description Fixes", flush=True)
    print("=" * 70, flush=True)

    items = get_all_items(NEIGHBORHOODS_COLLECTION)
    fixes = {
        "Ballston": "Discover Ballston in Arlington, VA — a thriving urban village with modern apartments, top dining, and easy Metro access near Washington DC.",
        "Falls Church": "Explore Falls Church, VA — a charming small-city community with excellent schools, local shops, and easy access to Washington DC."
    }

    for item in items:
        name = item["fieldData"].get("name", "")
        current_summary = item["fieldData"].get("summary-at-a-glance", "")
        if name in fixes and (not current_summary or len(str(current_summary).strip()) < 20):
            print(f"  Fixing: {name}", flush=True)
            data = {"fieldData": {"summary-at-a-glance": fixes[name]}}
            result = api_request("PATCH", f"/collections/{NEIGHBORHOODS_COLLECTION}/items/{item['id']}", data)
            if result:
                stats["updates"] += 1
                print(f"    SUCCESS", flush=True)
            else:
                stats["errors"] += 1
                print(f"    FAILED", flush=True)
            time.sleep(REQUEST_DELAY)
        elif name in fixes:
            print(f"  SKIP (has desc): {name}", flush=True)
            stats["skips"] += 1


def step6_publish():
    """Publish all changes to live site."""
    print("\n" + "=" * 70, flush=True)
    print("STEP 6: Publishing All Changes", flush=True)
    print("=" * 70, flush=True)

    # Webflow requires domain IDs to publish
    DOMAIN_IDS = ["650491e183ec54565be05490", "650491e183ec54565be05479"]

    print("  Publishing to gordonjamesrealty.com + www...", flush=True)
    data = {"customDomains": DOMAIN_IDS}
    result = api_request("POST", f"/sites/{SITE_ID}/publish", data)
    if result:
        print(f"  PUBLISHED SUCCESSFULLY!", flush=True)
        stats["updates"] += 1
    else:
        print(f"  Publish may have failed - check Webflow dashboard", flush=True)
        stats["errors"] += 1


if __name__ == "__main__":
    print("=" * 70, flush=True)
    print("GORDON JAMES REALTY - FULL SEO AUDIT UPDATE", flush=True)
    print("=" * 70, flush=True)
    print(f"Site: {SITE_ID}", flush=True)
    print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

    step1_cms_alt_text()
    step2_fix_winter_bug()
    step3_service_meta_descriptions()
    step4_static_page_seo()
    step5_neighborhood_meta_fixes()
    step6_publish()

    print("\n" + "=" * 70, flush=True)
    print("AUDIT UPDATE COMPLETE", flush=True)
    print("=" * 70, flush=True)
    print(f"API calls made: {stats['api_calls']}", flush=True)
    print(f"Items updated:  {stats['updates']}", flush=True)
    print(f"Items skipped:  {stats['skips']}", flush=True)
    print(f"Errors:         {stats['errors']}", flush=True)
    print(f"Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

    # Save results
    with open("/home/user/continuum-salesforce-overview/full_audit_results.json", "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats
        }, f, indent=2)
    print("Results saved to full_audit_results.json", flush=True)
