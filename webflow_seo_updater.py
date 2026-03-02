#!/usr/bin/env python3
"""
Gordon James Realty - Webflow CMS Image Alt Text Bulk Updater
Generates SEO-optimized alt text for all Knowledge Hub and Neighborhood images.
"""

import json
import urllib.request
import urllib.error
import time
import sys
import re

API_TOKEN = "fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6"
BASE_URL = "https://api.webflow.com/v2"
KNOWLEDGE_HUB_COLLECTION = "64c94b2afdeb6fdbaf3b2bd4"
NEIGHBORHOODS_COLLECTION = "64c94b2afdeb6fdbaf3b2bd0"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json"
}

# Rate limiting: Webflow allows 60 requests/minute
REQUEST_DELAY = 1.1  # seconds between requests


def api_request(method, path, data=None):
    """Make an API request with retry logic."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                error_body = e.read().decode()
                print(f"  HTTP {e.code}: {error_body[:200]}")
                raise
        except urllib.error.URLError as e:
            wait = 2 ** (attempt + 1)
            print(f"  Network error, retrying in {wait}s: {e}")
            time.sleep(wait)
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
        print(f"  Fetched {offset}/{total} items...")
        if offset >= total:
            break
        time.sleep(REQUEST_DELAY)
    return items


def generate_knowledge_hub_alt(item):
    """Generate descriptive alt text based on article title and content."""
    title = item["fieldData"].get("name", "")
    body = item["fieldData"].get("post-body", "")

    # Clean HTML from body for keyword extraction
    clean_body = re.sub(r'<[^>]+>', ' ', body).lower()

    # Determine the primary topic from the title
    title_lower = title.lower()

    # Property management topics
    if any(kw in title_lower for kw in ["hvac", "heating", "cooling", "air condition"]):
        return f"HVAC system maintenance and air filter replacement in a rental property - {title}"
    elif any(kw in title_lower for kw in ["hoa", "homeowner", "community association", "board"]):
        if "vendor" in title_lower:
            return f"HOA board members reviewing vendor proposals at a community association meeting"
        elif "budget" in title_lower or "financial" in title_lower or "dues" in title_lower:
            return f"Community association financial planning and budget documents for HOA management"
        elif "social" in title_lower or "event" in title_lower:
            return f"Community residents gathering at an HOA-organized neighborhood social event"
        elif "parking" in title_lower:
            return f"Residential community parking area managed under HOA parking regulations"
        elif "collection" in title_lower or "delinquent" in title_lower:
            return f"HOA financial documents and collection notices for delinquent community dues"
        elif "landscaping" in title_lower or "curb" in title_lower:
            return f"Well-maintained community landscaping and curb appeal in an HOA-managed neighborhood"
        elif "meeting" in title_lower:
            return f"HOA board members conducting a community association governance meeting"
        elif "insurance" in title_lower:
            return f"Insurance policy documents for community association and HOA coverage review"
        elif "reserve" in title_lower:
            return f"Financial reserve fund analysis documents for HOA long-term planning"
        elif "rule" in title_lower or "enforcement" in title_lower or "violation" in title_lower:
            return f"Community association rule enforcement documentation and HOA compliance guidelines"
        elif "election" in title_lower or "vote" in title_lower:
            return f"HOA board election and community voting process at an association meeting"
        elif "pet" in title_lower:
            return f"Pet policy signage in an HOA-managed residential community"
        else:
            return f"Community association management meeting for HOA governance and operations"
    elif any(kw in title_lower for kw in ["tenant", "renter", "lease", "rent"]):
        if "welcome" in title_lower or "move-in" in title_lower or "move in" in title_lower:
            return f"New tenant receiving welcome packet and move-in documentation at a rental property"
        elif "screen" in title_lower or "application" in title_lower:
            return f"Tenant screening and rental application review process for property management"
        elif "evict" in title_lower:
            return f"Legal eviction notice and tenant communication documents for property managers"
        elif "noise" in title_lower or "complaint" in title_lower:
            return f"Property manager addressing tenant noise complaints in a residential building"
        elif "repair" in title_lower or "maintenance" in title_lower:
            return f"Maintenance technician performing repairs at a tenant-occupied rental property"
        elif "rights" in title_lower:
            return f"Tenant rights documentation and landlord-tenant legal guidelines"
        elif "security deposit" in title_lower or "deposit" in title_lower:
            return f"Security deposit documentation and move-out inspection checklist"
        else:
            return f"Professional property manager reviewing tenant lease documents and rental agreements"
    elif any(kw in title_lower for kw in ["landlord", "property owner", "rental property"]):
        if "tax" in title_lower:
            return f"Rental property tax documents and financial records for landlord tax preparation"
        elif "insurance" in title_lower:
            return f"Landlord reviewing rental property insurance policy and coverage options"
        elif "maintenance" in title_lower or "repair" in title_lower:
            return f"Property maintenance worker performing repairs on a rental home"
        elif "roi" in title_lower or "return" in title_lower or "profit" in title_lower:
            return f"Investment property financial analysis showing rental income and ROI calculations"
        else:
            return f"Property owner reviewing rental management documents with a professional property manager"
    elif any(kw in title_lower for kw in ["invest", "foreclosure", "flip", "real estate invest"]):
        return f"Real estate investment property analysis and financial evaluation documents"
    elif any(kw in title_lower for kw in ["commercial", "office", "retail"]):
        return f"Commercial property building exterior managed by a professional management company"
    elif any(kw in title_lower for kw in ["buy", "sell", "closing", "home buyer", "first-time"]):
        return f"Home buyer reviewing real estate purchase documents with a licensed realtor"
    elif any(kw in title_lower for kw in ["condo", "condominium", "co-op"]):
        return f"Condominium building exterior in the Washington DC metropolitan area"
    elif any(kw in title_lower for kw in ["mold", "water damage", "flood", "leak"]):
        return f"Property inspector examining water damage and mold remediation in a rental property"
    elif any(kw in title_lower for kw in ["pest", "bedbug", "bed bug", "roach", "termite"]):
        return f"Professional pest control inspection and treatment at a residential rental property"
    elif any(kw in title_lower for kw in ["fire", "smoke", "safety", "carbon monoxide"]):
        return f"Fire safety equipment and smoke detector inspection in a managed rental property"
    elif any(kw in title_lower for kw in ["law", "legal", "regulation", "compliance", "rent control"]):
        return f"Legal compliance documents and regulatory guidelines for property management"
    elif any(kw in title_lower for kw in ["pet", "animal", "dog", "cat"]):
        return f"Pet-friendly rental property with pet policy guidelines and management documentation"
    elif any(kw in title_lower for kw in ["energy", "electric", "utility", "solar", "green"]):
        return f"Energy-efficient upgrades and utility management in a residential rental property"
    elif any(kw in title_lower for kw in ["renovation", "remodel", "upgrade", "improve"]):
        return f"Property renovation and home improvement project at a residential rental"
    elif any(kw in title_lower for kw in ["winter", "snow", "cold", "freeze"]):
        return f"Winter property maintenance and cold weather preparation for rental homes"
    elif any(kw in title_lower for kw in ["summer", "heat", "cooling"]):
        return f"Summer property maintenance and cooling system preparation for rental properties"
    elif any(kw in title_lower for kw in ["spring", "clean"]):
        return f"Spring cleaning and seasonal property maintenance checklist for rental homes"
    elif any(kw in title_lower for kw in ["market", "trend", "forecast"]):
        return f"Washington DC real estate market trends and rental market analysis chart"
    elif any(kw in title_lower for kw in ["technology", "smart home", "software", "app"]):
        return f"Property management technology and smart home systems in a modern rental"
    elif any(kw in title_lower for kw in ["vacation", "short-term", "airbnb"]):
        return f"Short-term vacation rental property managed in the Washington DC area"
    elif any(kw in title_lower for kw in ["subdivision", "subdivide", "single-family"]):
        return f"Single-family residential property with subdivision development potential"
    elif "washington" in title_lower or "dc" in title_lower or "virginia" in title_lower or "maryland" in title_lower:
        return f"Residential neighborhood in the Washington DC metropolitan area"
    else:
        # Generic but still descriptive fallback
        return f"Professional property management services in Washington DC - {title}"


def generate_neighborhood_alt(item):
    """Generate descriptive alt text for neighborhood guide images."""
    name = item["fieldData"].get("name", "")

    neighborhood_descriptions = {
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

    return neighborhood_descriptions.get(name,
        f"Scenic view of the {name} neighborhood in the Washington DC metropolitan area")


def update_item_alt_text(collection_id, item_id, image_url, alt_text):
    """Update the alt text for an item's image."""
    data = {
        "fieldData": {
            "main-image" if collection_id == KNOWLEDGE_HUB_COLLECTION else "featured-header-image": {
                "url": image_url,
                "alt": alt_text
            }
        }
    }
    return api_request("PATCH", f"/collections/{collection_id}/items/{item_id}", data)


def process_knowledge_hub():
    """Process all Knowledge Hub items."""
    print("\n" + "="*70)
    print("PROCESSING KNOWLEDGE HUB (339 articles)")
    print("="*70)

    items = get_all_items(KNOWLEDGE_HUB_COLLECTION)
    print(f"\nTotal items to process: {len(items)}")

    results = {"success": 0, "skipped": 0, "failed": 0, "details": []}

    for idx, item in enumerate(items):
        item_id = item["id"]
        title = item["fieldData"].get("name", "Unknown")
        image = item["fieldData"].get("main-image", {})

        if not image or not image.get("url"):
            print(f"  [{idx+1}/{len(items)}] SKIP (no image): {title[:60]}")
            results["skipped"] += 1
            continue

        if image.get("alt"):
            print(f"  [{idx+1}/{len(items)}] SKIP (has alt): {title[:60]}")
            results["skipped"] += 1
            continue

        alt_text = generate_knowledge_hub_alt(item)

        print(f"  [{idx+1}/{len(items)}] Updating: {title[:50]}...")
        print(f"           Alt: {alt_text[:70]}...")

        try:
            result = update_item_alt_text(
                KNOWLEDGE_HUB_COLLECTION, item_id, image["url"], alt_text
            )
            if result:
                results["success"] += 1
                results["details"].append({
                    "id": item_id,
                    "title": title,
                    "alt": alt_text,
                    "status": "success"
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "id": item_id,
                    "title": title,
                    "alt": alt_text,
                    "status": "failed"
                })
        except Exception as e:
            print(f"           ERROR: {e}")
            results["failed"] += 1
            results["details"].append({
                "id": item_id,
                "title": title,
                "alt": alt_text,
                "status": f"error: {e}"
            })

        time.sleep(REQUEST_DELAY)

    return results


def process_neighborhoods():
    """Process all Neighborhood items."""
    print("\n" + "="*70)
    print("PROCESSING NEIGHBORHOODS (27 guides)")
    print("="*70)

    items = get_all_items(NEIGHBORHOODS_COLLECTION)
    print(f"\nTotal items to process: {len(items)}")

    results = {"success": 0, "skipped": 0, "failed": 0, "details": []}

    for idx, item in enumerate(items):
        item_id = item["id"]
        name = item["fieldData"].get("name", "Unknown")
        image = item["fieldData"].get("featured-header-image", {})

        if not image or not image.get("url"):
            print(f"  [{idx+1}/{len(items)}] SKIP (no image): {name}")
            results["skipped"] += 1
            continue

        if image.get("alt"):
            print(f"  [{idx+1}/{len(items)}] SKIP (has alt): {name}")
            results["skipped"] += 1
            continue

        alt_text = generate_neighborhood_alt(item)

        print(f"  [{idx+1}/{len(items)}] Updating: {name}")
        print(f"           Alt: {alt_text[:70]}...")

        try:
            result = update_item_alt_text(
                NEIGHBORHOODS_COLLECTION, item_id, image["url"], alt_text
            )
            if result:
                results["success"] += 1
                results["details"].append({
                    "id": item_id,
                    "name": name,
                    "alt": alt_text,
                    "status": "success"
                })
            else:
                results["failed"] += 1
        except Exception as e:
            print(f"           ERROR: {e}")
            results["failed"] += 1

        time.sleep(REQUEST_DELAY)

    return results


def fix_missing_meta_descriptions():
    """Fix missing meta descriptions for Ballston and Falls Church."""
    print("\n" + "="*70)
    print("FIXING MISSING META DESCRIPTIONS")
    print("="*70)

    items = get_all_items(NEIGHBORHOODS_COLLECTION)
    fixes = {
        "Ballston": "Discover Ballston in Arlington, VA — a thriving urban village with modern apartments, top dining, and easy Metro access near Washington DC.",
        "Falls Church": "Explore Falls Church, VA — a charming small-city community with excellent schools, local shops, and easy access to Washington DC."
    }

    for item in items:
        name = item["fieldData"].get("name", "")
        if name in fixes and not item["fieldData"].get("summary-at-a-glance"):
            print(f"  Fixing meta description for: {name}")
            data = {
                "fieldData": {
                    "summary-at-a-glance": fixes[name]
                }
            }
            result = api_request("PATCH", f"/collections/{NEIGHBORHOODS_COLLECTION}/items/{item['id']}", data)
            if result:
                print(f"  SUCCESS: {name} meta description updated")
            else:
                print(f"  FAILED: {name}")
            time.sleep(REQUEST_DELAY)


if __name__ == "__main__":
    print("Gordon James Realty - Webflow CMS SEO Bulk Updater")
    print("=" * 70)

    # Process Knowledge Hub
    kb_results = process_knowledge_hub()
    print(f"\nKnowledge Hub Results: {kb_results['success']} updated, {kb_results['skipped']} skipped, {kb_results['failed']} failed")

    # Process Neighborhoods
    nb_results = process_neighborhoods()
    print(f"\nNeighborhood Results: {nb_results['success']} updated, {nb_results['skipped']} skipped, {nb_results['failed']} failed")

    # Fix missing meta descriptions
    fix_missing_meta_descriptions()

    # Save results log
    all_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "knowledge_hub": kb_results,
        "neighborhoods": nb_results
    }
    with open("/home/user/continuum-salesforce-overview/seo_update_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "="*70)
    print("ALL DONE!")
    print(f"Total updated: {kb_results['success'] + nb_results['success']}")
    print(f"Results saved to seo_update_results.json")
    print("="*70)
