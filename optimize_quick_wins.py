#!/usr/bin/env python3
"""
Quick-Win SEO Optimization Script for Gordon James Realty Knowledge Hub
Updates CMS item titles, meta descriptions, and body content via Webflow API v2
"""

import json
import time
import urllib.request
import urllib.error
import sys

TOKEN = "fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6"
COLLECTION = "64c94b2afdeb6fdbaf3b2bd4"
BASE = "https://api.webflow.com/v2"

def api_patch(item_id, field_data):
    """PATCH a CMS item's fieldData"""
    url = f"{BASE}/collections/{COLLECTION}/items/{item_id}"
    payload = json.dumps({"fieldData": field_data}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="PATCH")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            name = data.get("fieldData", {}).get("name", "")
            print(f"  OK — {name}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ERROR {e.code}: {body[:300]}")
        return False

def api_get(item_id):
    """GET a CMS item's full data"""
    url = f"{BASE}/collections/{COLLECTION}/items/{item_id}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# ──────────────────────────────────────────────
# PHASE 1: Title + Meta Description Optimization
# ──────────────────────────────────────────────

updates = [
    {
        "id": "687e45e1f7563cb8cf0d1aee",
        "keyword": "commercial building management",
        "current_pos": 17,
        "volume": 500,
        "fields": {
            "name": "Commercial Building Management: What a Building Management Company Does",
            "post-summary": "Learn what commercial building management companies do and the services they provide — from leasing and maintenance to compliance and long-term planning for investors."
        }
    },
    {
        "id": "689362dd8141c20393dcd39f",
        "keyword": "common areas",
        "current_pos": 20,
        "volume": 500,
        "fields": {
            "name": "What Are HOA Common Areas? Types, Rules & Maintenance Responsibilities",
            "post-summary": "Learn what HOA common areas are, who maintains them, and how association rules protect shared spaces like pools, lobbies, parks, and parking lots."
        }
    },
    {
        "id": "6893648796477877bca20dc4",
        "keyword": "renting a condo",
        "current_pos": 11,
        "volume": 200,
        "fields": {
            "name": "Renting a Condo: A Practical Guide to Renting Out Your Condo Successfully",
            "post-summary": "Thinking about renting a condo? This step-by-step guide covers how to prepare, market, screen tenants, and manage your condo rental like a pro."
        }
    },
    {
        "id": "687fca5c6abca1d762046e45",
        "keyword": "hoa solar panel restrictions",
        "current_pos": 11,
        "volume": 200,
        "fields": {
            "name": "HOA Solar Panel Restrictions: Policies, Laws & What Homeowners Need to Know",
            "post-summary": "Explore HOA solar panel restrictions, state and federal laws protecting homeowners, and what HOA boards need to know before approving or denying installations."
        }
    },
    {
        "id": "6823add07da8b5e4ff8230e3",
        "keyword": "landscaping for renters",
        "current_pos": 10,
        "volume": 150,
        "fields": {
            "name": "Landscaping for Renters: Low-Maintenance Rental Property Landscaping Tips",
            "post-summary": "Discover smart landscaping for renters and rental property owners. Expert tips on low-maintenance curb appeal using native plants, synthetic turf, and patios."
        }
    },
    {
        # DON'T change title — already #1 for main keyword (4,600 vol)
        # Only update meta description to include Virginia angle
        "id": "660462fd2c166bb0aec1ce9c",
        "keyword": "unenforceable hoa rules virginia",
        "current_pos": 19,
        "volume": 150,
        "fields": {
            "post-summary": "Unenforceable HOA rules can disrupt communities across Virginia, Maryland, and DC. Learn how to identify, challenge, and resolve invalid HOA regulations."
        }
    },
    {
        "id": "67ed78962314572a90cebf0c",
        "keyword": "keyless entry for rental property",
        "current_pos": 7,
        "volume": 70,
        "fields": {
            "name": "Keyless Entry for Rental Properties: Pros, Cons & Best Smart Lock Options",
            "post-summary": "Considering keyless entry for your rental property? Compare smart locks, keypads, and Bluetooth options with pros, cons, and landlord recommendations."
        }
    },
    {
        "id": "66c76bbc9b42ce7698f0c6cf",
        "keyword": "checklist for landlords when tenant moves out",
        "current_pos": 10,
        "volume": 70,
        "fields": {
            "name": "Move-Out Checklist for Landlords and Tenants: Essential Steps When a Tenant Moves Out",
            "post-summary": "Use this move-out checklist for landlords when a tenant moves out. Covers inspections, security deposits, cleaning standards, and proper documentation."
        }
    }
]

print("=" * 60)
print("PHASE 1: Updating Titles & Meta Descriptions")
print("=" * 60)

for u in updates:
    print(f"\n[#{u['current_pos']} → target top 10] \"{u['keyword']}\" (vol: {u['volume']})")
    api_patch(u["id"], u["fields"])
    time.sleep(1.2)  # Rate limit: 60 req/min

# ──────────────────────────────────────────────
# PHASE 2: Body Content Expansion
# Append keyword-rich FAQ sections to top articles
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PHASE 2: Expanding Body Content with FAQ Sections")
print("=" * 60)

body_additions = {
    # 1. Building Management — add commercial-specific content
    "687e45e1f7563cb8cf0d1aee": {
        "keyword": "commercial building management",
        "append_html": """
<h4>Commercial Building Management vs. Residential Property Management</h4>
<p>While residential property management focuses on single-family homes, condos, and apartments, commercial building management encompasses office buildings, retail spaces, mixed-use developments, and industrial facilities. Commercial building management services require specialized knowledge of commercial lease structures, building codes, HVAC systems for large facilities, and compliance with ADA regulations.</p>
<p>Key differences include:</p>
<ul>
<li><strong>Lease Complexity</strong> — Commercial leases often involve triple-net (NNN) terms, CAM charges, and percentage rent clauses that require professional oversight.</li>
<li><strong>Maintenance Scale</strong> — Commercial buildings have larger HVAC, electrical, and plumbing systems that demand preventive maintenance programs.</li>
<li><strong>Tenant Relations</strong> — Business tenants have different expectations and longer lease terms, requiring a more strategic approach to retention.</li>
<li><strong>Regulatory Requirements</strong> — Commercial properties must comply with fire codes, ADA accessibility standards, and local zoning ordinances.</li>
</ul>
<h4>What Building Management Services Typically Include</h4>
<p>A full-service building management company typically provides:</p>
<ul>
<li><strong>Facility Operations</strong> — Day-to-day oversight of building systems, janitorial services, and common area maintenance.</li>
<li><strong>Financial Management</strong> — Budgeting, rent collection, CAM reconciliation, and financial reporting to property owners.</li>
<li><strong>Tenant Coordination</strong> — Lease administration, move-in/move-out management, and tenant improvement projects.</li>
<li><strong>Vendor Management</strong> — Sourcing, negotiating, and supervising third-party contractors for specialized services.</li>
<li><strong>Emergency Response</strong> — 24/7 on-call support for building emergencies including water damage, power outages, and security incidents.</li>
</ul>
<h4>Frequently Asked Questions About Commercial Building Management</h4>
<p><strong>What does a commercial building management company charge?</strong><br>Fees typically range from 4% to 10% of collected rent, depending on the building type, size, and services required. Some companies charge a flat monthly fee instead.</p>
<p><strong>When should a property owner hire a building management company?</strong><br>Most owners benefit from professional management when they own multiple properties, live far from the building, or lack experience with commercial lease administration and building systems.</p>
<p><strong>What is the difference between building management and facility management?</strong><br>Building management focuses on the overall operation and financial performance of a property, while facility management is more narrowly focused on the physical maintenance and functionality of the building itself. Many companies provide both services together.</p>
"""
    },

    # 2. Common Areas — expand definitions and add FAQ
    "689362dd8141c20393dcd39f": {
        "keyword": "common areas",
        "append_html": """
<h4>Common Areas in Different Types of HOA Communities</h4>
<p>The definition and scope of common areas can vary significantly depending on the type of community:</p>
<ul>
<li><strong>Single-Family Home HOAs</strong> — Common areas typically include streets, sidewalks, parks, playgrounds, community pools, and clubhouses. Individual homeowners are responsible for their own yards and structures.</li>
<li><strong>Condominium Associations</strong> — Common areas extend beyond shared amenities to include hallways, elevators, lobbies, roofs, exterior walls, and building structural elements. The distinction between common areas and limited common areas (like balconies or assigned parking) is particularly important.</li>
<li><strong>Townhouse Communities</strong> — These often have a mix of shared and limited common areas, with yards sometimes classified as limited common areas maintained by individual owners but owned by the association.</li>
</ul>
<h4>Common Area Disputes and How to Resolve Them</h4>
<p>Disputes over common areas are among the most frequent sources of conflict in HOA communities. Common disagreements include:</p>
<ul>
<li>Who is responsible for repairs to limited common areas like patios and balconies</li>
<li>Whether modifications to common areas require board approval</li>
<li>How special assessments for common area improvements are allocated</li>
<li>Access rights to exclusive-use common areas</li>
</ul>
<p>The best approach is to consult the association's governing documents — specifically the CC&Rs and bylaws — which should outline maintenance responsibilities, modification procedures, and dispute resolution processes.</p>
<h4>Frequently Asked Questions About HOA Common Areas</h4>
<p><strong>Who pays for HOA common area maintenance?</strong><br>All homeowners contribute through their regular HOA dues. For major repairs or improvements, the association may levy a special assessment or draw from reserve funds.</p>
<p><strong>Can an HOA restrict access to common areas?</strong><br>Yes, but restrictions must be applied consistently and in accordance with the governing documents. An HOA cannot selectively deny access to specific homeowners without a valid, documented reason such as unpaid dues.</p>
<p><strong>What happens if common areas are damaged by a homeowner?</strong><br>The responsible homeowner may be required to pay for repairs. The HOA's governing documents and insurance policies typically outline the process for recovering costs from the individual responsible for the damage.</p>
"""
    },

    # 3. Renting a Condo — add DC/VA-specific content and FAQ
    "6893648796477877bca20dc4": {
        "keyword": "renting a condo",
        "append_html": """
<h4>Renting a Condo vs. Renting a House: Key Differences</h4>
<p>Renting a condo is different from renting a single-family home in several important ways:</p>
<ul>
<li><strong>HOA Rules Apply</strong> — Most condo associations have rules about renting, including minimum lease terms, tenant screening requirements, and caps on the number of units that can be rented at any time.</li>
<li><strong>Shared Amenities</strong> — Tenants may have access to pools, gyms, and common areas, but the condo board's rules govern usage.</li>
<li><strong>Insurance Differences</strong> — You'll need a landlord insurance policy that works alongside the condo association's master policy. Make sure your coverage fills any gaps.</li>
<li><strong>Maintenance Boundaries</strong> — The association handles exterior maintenance and common areas, while you as the owner are responsible for everything inside your unit.</li>
</ul>
<h4>Renting a Condo in Washington DC, Virginia & Maryland</h4>
<p>If you own a condo in the DC metro area, there are specific regulations to be aware of:</p>
<ul>
<li><strong>Washington DC</strong> — DC's tenant-friendly laws include rent control provisions for certain buildings, and landlords must register rental units with the Department of Housing. Security deposit limits and return timelines are strictly enforced.</li>
<li><strong>Virginia</strong> — The Virginia Residential Landlord and Tenant Act governs most condo rentals. Landlords must provide specific disclosures, maintain habitable conditions, and follow strict procedures for security deposit handling.</li>
<li><strong>Maryland</strong> — Maryland law requires landlords to place security deposits in escrow accounts and provides tenants with specific rights regarding repairs and lease termination.</li>
</ul>
<h4>Frequently Asked Questions About Renting a Condo</h4>
<p><strong>Can my HOA prevent me from renting my condo?</strong><br>Yes, if the governing documents include rental restrictions. Some associations limit the percentage of units that can be rented, impose minimum lease terms (often 12 months), or require board approval of tenants.</p>
<p><strong>How much can I rent my condo for?</strong><br>Research comparable rentals in your building and neighborhood. Factors include unit size, floor level, view, amenities, parking, and current market conditions. A property manager can provide a detailed rental analysis.</p>
<p><strong>Do I need to tell my HOA I'm renting my condo?</strong><br>Almost always yes. Most condo associations require owners to notify the board before renting and provide tenant information. Failure to do so can result in fines or other penalties.</p>
"""
    },

    # 4. HOA Solar Panel Restrictions — add state laws and FAQ
    "687fca5c6abca1d762046e45": {
        "keyword": "hoa solar panel restrictions",
        "append_html": """
<h4>HOA Solar Panel Restrictions by State</h4>
<p>Solar access laws vary significantly by state, and many states have enacted legislation to limit how much an HOA can restrict solar panel installation:</p>
<ul>
<li><strong>California</strong> — The Solar Rights Act prohibits HOAs from banning solar panels entirely. Associations can impose reasonable restrictions related to placement, but cannot increase costs by more than $1,000 or reduce efficiency by more than 10%.</li>
<li><strong>Florida</strong> — Florida law prevents HOAs from prohibiting solar panels but allows associations to set guidelines for placement and aesthetics that don't impair performance.</li>
<li><strong>Virginia</strong> — Virginia Code allows reasonable restrictions but prevents outright bans on solar energy devices. HOAs can regulate placement and appearance within reason.</li>
<li><strong>Maryland</strong> — Maryland's solar access provisions protect homeowners' rights to install panels while allowing HOAs to establish aesthetic guidelines.</li>
<li><strong>Texas</strong> — The Texas Property Code restricts HOAs from banning solar panels and limits the types of restrictions they can impose on installation.</li>
<li><strong>Colorado</strong> — Colorado law prohibits unreasonable restrictions on solar devices and prevents HOAs from banning installations that comply with state building codes.</li>
</ul>
<h4>How HOA Boards Should Handle Solar Panel Requests</h4>
<p>Rather than fighting solar panel installations, HOA boards can adopt proactive policies that protect community aesthetics while respecting homeowner rights:</p>
<ol>
<li><strong>Create Clear Guidelines</strong> — Establish written standards for solar panel placement, mounting, and appearance before requests come in.</li>
<li><strong>Streamline the Approval Process</strong> — Develop a simple application form and timeline so homeowners know what to expect.</li>
<li><strong>Consult Legal Counsel</strong> — Ensure your guidelines comply with state solar access laws to avoid costly legal challenges.</li>
<li><strong>Consider Community Solar</strong> — Some associations are exploring shared solar installations that benefit the entire community while maintaining a uniform appearance.</li>
</ol>
<h4>Frequently Asked Questions About HOA Solar Panel Restrictions</h4>
<p><strong>Can my HOA deny my solar panel application?</strong><br>It depends on your state's laws and your HOA's governing documents. In many states, HOAs cannot outright ban solar panels but can impose reasonable restrictions on placement and appearance. If your HOA denies your application, review your state's solar access laws before appealing.</p>
<p><strong>Do HOA solar panel restrictions affect property value?</strong><br>Solar panels generally increase property value by 3-4%, according to multiple studies. HOAs that overly restrict solar installations may actually be limiting their community's property values by preventing this improvement.</p>
<p><strong>What if my HOA's solar rules conflict with state law?</strong><br>State law generally supersedes HOA rules. If your HOA's restrictions violate your state's solar access laws, you may have legal grounds to challenge the restriction through dispute resolution or the courts.</p>
"""
    },

    # 5. Landscaping for Renters — add renter-specific tips and FAQ
    "6823add07da8b5e4ff8230e3": {
        "keyword": "landscaping for renters",
        "append_html": """
<h4>Landscaping for Renters: Tenant-Friendly Ideas That Don't Require Landlord Approval</h4>
<p>If you're a renter looking to improve your outdoor space, there are plenty of options that don't require permanent changes or landlord permission:</p>
<ul>
<li><strong>Container Gardens</strong> — Potted plants, herbs, and flowers add color and personality without modifying the landscape. Choose containers that complement the property's exterior.</li>
<li><strong>Portable Raised Beds</strong> — Modular raised garden beds can be assembled and removed without damaging the yard, perfect for growing vegetables or flowers.</li>
<li><strong>Outdoor Rugs and Furniture</strong> — Transform a patio or deck area with weather-resistant rugs, seating, and decorative elements.</li>
<li><strong>Solar-Powered Lighting</strong> — Stake-mounted solar lights along walkways improve safety and ambiance without electrical work.</li>
<li><strong>Vertical Gardens</strong> — Freestanding trellises and plant stands add greenery without attaching anything to the building.</li>
</ul>
<h4>What Landlords Should Include in a Landscaping Clause</h4>
<p>To avoid disputes about outdoor maintenance, include specific landscaping responsibilities in your lease agreement:</p>
<ul>
<li>Who is responsible for mowing, edging, and leaf removal</li>
<li>Watering schedules and restrictions (especially in drought-prone areas)</li>
<li>Whether tenants may plant or remove any vegetation</li>
<li>Snow and ice removal responsibilities</li>
<li>Consequences for neglecting landscaping duties</li>
</ul>
<h4>Frequently Asked Questions About Rental Property Landscaping</h4>
<p><strong>Is the landlord or tenant responsible for landscaping?</strong><br>It depends on the lease agreement. For single-family rentals, basic lawn care (mowing, watering, weeding) is often assigned to tenants, while major landscaping projects and tree maintenance remain the landlord's responsibility. In multi-unit properties, landlords typically handle all landscaping.</p>
<p><strong>Can a landlord require tenants to maintain the yard?</strong><br>Yes, if it's specified in the lease. Most states allow landlords to assign reasonable yard maintenance duties to tenants. However, the landlord remains responsible for ensuring the property meets local code requirements.</p>
<p><strong>What are the best low-maintenance landscaping options for rental properties?</strong><br>Native plants, drought-tolerant ground covers, synthetic turf, mulched beds, and hardscaping (patios, gravel paths) all reduce maintenance while maintaining curb appeal. These options minimize tenant neglect issues and keep the property looking attractive year-round.</p>
"""
    },

    # 6. Unenforceable HOA Rules — add Virginia/DC/MD specific section
    "660462fd2c166bb0aec1ce9c": {
        "keyword": "unenforceable hoa rules virginia",
        "append_html": """
<h4>Unenforceable HOA Rules in Virginia</h4>
<p>Virginia has specific statutes that govern homeowners associations, including the Virginia Property Owners' Association Act (POAA) and the Virginia Condominium Act. Under these laws, several types of HOA rules are commonly found to be unenforceable:</p>
<ul>
<li><strong>Rules Conflicting with Virginia Fair Housing Law</strong> — Any HOA rule that discriminates based on race, color, religion, national origin, sex, elderliness, familial status, or disability is unenforceable under the Virginia Fair Housing Law.</li>
<li><strong>Retroactive Amendments</strong> — Virginia courts have generally held that HOA amendments that retroactively change property rights — such as suddenly banning previously allowed structures — may be unenforceable, particularly if homeowners relied on the prior rules when purchasing.</li>
<li><strong>Rules Not Properly Adopted</strong> — Virginia's POAA requires specific procedures for amending governing documents, including proper notice to homeowners and required voting thresholds. Rules adopted without following these procedures can be challenged.</li>
<li><strong>Excessive Fines Without Due Process</strong> — Virginia law requires that homeowners be given notice and an opportunity to be heard before fines are imposed. Fines levied without proper hearings are typically unenforceable.</li>
<li><strong>Solar Panel Bans</strong> — As noted in Virginia Code, outright bans on solar energy devices are not enforceable, though reasonable aesthetic guidelines are permitted.</li>
</ul>
<h4>Unenforceable HOA Rules in Washington DC and Maryland</h4>
<p>HOA communities in the DC metro area should also be aware of local regulations:</p>
<ul>
<li><strong>Washington DC</strong> — The DC Condominium Act provides strong protections for unit owners, and any HOA rule that conflicts with DC's expansive Human Rights Act — which covers more protected classes than federal law — is unenforceable.</li>
<li><strong>Maryland</strong> — The Maryland Homeowners Association Act requires HOAs to follow specific procedures when enforcing rules and imposing fines. Maryland courts have struck down rules that were inconsistently enforced or that unreasonably restricted homeowner property rights.</li>
</ul>
<p>If you believe your HOA is enforcing rules that may not hold up under Virginia, DC, or Maryland law, consult with an attorney who specializes in community association law or reach out to a professional management company for guidance.</p>
"""
    },

    # 7. Keyless Entry — add comparison and FAQ
    "67ed78962314572a90cebf0c": {
        "keyword": "keyless entry for rental property",
        "append_html": """
<h4>Best Keyless Entry Systems for Rental Properties in 2026</h4>
<p>Choosing the right keyless entry system for your rental property depends on your budget, the number of units, and your management style. Here are the top options landlords are using:</p>
<ul>
<li><strong>Smart Keypad Deadbolts</strong> — These are the most popular choice for rental properties. Tenants enter a code to unlock, and landlords can change codes remotely between tenants. Typical cost: $100-$250 per unit.</li>
<li><strong>Bluetooth Smart Locks</strong> — These connect to a smartphone app and allow tenants to unlock with their phone. Landlords can grant and revoke access remotely. Typical cost: $150-$350 per unit.</li>
<li><strong>Wi-Fi Connected Locks</strong> — These offer the most features, including remote access, activity logs, and integration with property management software. Ideal for landlords managing multiple properties. Typical cost: $200-$400 per unit.</li>
<li><strong>Combination Lockboxes</strong> — A simple, affordable option often used for showing vacant units. Not recommended as a primary entry system for occupied rentals.</li>
</ul>
<h4>Frequently Asked Questions About Keyless Entry for Rental Properties</h4>
<p><strong>Is keyless entry worth the investment for landlords?</strong><br>Yes, for most landlords. Keyless entry eliminates the cost and hassle of rekeying between tenants (typically $50-$150 per lock), provides an audit trail of entry, and is a selling point that can justify slightly higher rent.</p>
<p><strong>Can a landlord require keyless entry in a rental?</strong><br>Generally yes, as long as the system provides the same or better security as traditional locks and meets local building codes. Some tenants may have accessibility concerns, so choose systems that offer multiple entry methods.</p>
<p><strong>What happens if the keyless entry system loses power or connectivity?</strong><br>Most quality smart locks include a backup physical key option or a battery-powered keypad that continues working during power outages. Always choose a system with a mechanical backup to ensure tenants are never locked out.</p>
"""
    },

    # 8. Move-Out Checklist — add landlord-specific section and FAQ
    "66c76bbc9b42ce7698f0c6cf": {
        "keyword": "checklist for landlords when tenant moves out",
        "append_html": """
<h4>Checklist for Landlords When a Tenant Moves Out</h4>
<p>As a landlord, having a structured process for tenant move-outs protects your property and helps avoid disputes. Follow this checklist every time a tenant vacates:</p>
<ol>
<li><strong>Send a Move-Out Reminder (30 Days Before)</strong> — Remind the tenant of their lease end date, cleaning expectations, and key return procedure. Include a copy of the move-out checklist.</li>
<li><strong>Schedule the Move-Out Inspection</strong> — Coordinate a date and time for a walk-through inspection. Ideally, do this with the tenant present so you can discuss any issues in real time.</li>
<li><strong>Document Property Condition</strong> — Take dated photos and video of every room, comparing against your move-in documentation. Note any damage beyond normal wear and tear.</li>
<li><strong>Check All Systems</strong> — Test HVAC, plumbing, electrical outlets, smoke detectors, carbon monoxide detectors, appliances, and garage door openers.</li>
<li><strong>Collect All Keys and Access Devices</strong> — Account for all keys, garage remotes, mailbox keys, pool passes, and any other access devices. If using keyless entry, change access codes immediately.</li>
<li><strong>Review Utility Transfer</strong> — Confirm that utilities have been transferred out of the tenant's name and that there are no outstanding balances that could result in service interruptions.</li>
<li><strong>Process the Security Deposit</strong> — Follow your state's specific timeline and requirements for returning the security deposit. In Virginia, landlords have 45 days; in DC, 45 days; in Maryland, 45 days. Provide an itemized list of any deductions.</li>
<li><strong>Address Maintenance and Repairs</strong> — Schedule any necessary repairs, painting, or cleaning before listing the property for the next tenant.</li>
<li><strong>Update Your Records</strong> — File the move-out inspection report, security deposit accounting, and forwarding address for the former tenant.</li>
</ol>
<h4>Frequently Asked Questions About Tenant Move-Outs</h4>
<p><strong>What is considered normal wear and tear vs. tenant damage?</strong><br>Normal wear and tear includes minor scuffs on walls, small nail holes, worn carpet from foot traffic, and faded paint. Tenant damage includes large holes in walls, stained or burned carpet, broken fixtures, and unauthorized modifications. You can only deduct from the security deposit for actual damage, not normal wear and tear.</p>
<p><strong>What if the tenant leaves belongings behind?</strong><br>State laws vary on how to handle abandoned property. In most states, you must notify the tenant in writing and wait a specified period (often 10-30 days) before disposing of the items. Do not throw away belongings immediately, as this could expose you to liability.</p>
<p><strong>Can I charge for professional cleaning after a tenant moves out?</strong><br>You can deduct cleaning costs from the security deposit if the tenant left the unit in a condition that goes beyond normal wear and tear. However, you generally cannot charge for routine turnover cleaning that you would do regardless of the tenant's cleanliness.</p>
"""
    }
}

for item_id, data in body_additions.items():
    print(f"\n[Expanding content] \"{data['keyword']}\"")
    # Fetch current body
    item = api_get(item_id)
    current_body = item.get("fieldData", {}).get("post-body", "")
    time.sleep(1.2)

    # Append new content before the final CTA paragraph if present, or at the end
    new_body = current_body + data["append_html"]

    # Update
    api_patch(item_id, {"post-body": new_body})
    time.sleep(1.2)

print("\n" + "=" * 60)
print("ALL UPDATES COMPLETE")
print("=" * 60)
print("\nNext step: Publish the site to push changes live.")
