# Gordon James Realty — Webflow SEO Project

## Webflow API Access
- **API Token**: `fd75e6aa4e9c948189335d155eb0aaf6df55f943c827aa6c4c90050ee0096fd6`
- **API Base URL**: `https://api.webflow.com/v2`
- **Site ID**: `64c94b2afdeb6fdbaf3b2b58`
- **Site URL**: `https://www.gordonjamesrealty.com`

## Domain IDs (required for publishing)
- `650491e183ec54565be05490` — www.gordonjamesrealty.com
- `650491e183ec54565be05479` — gordonjamesrealty.com

## Collection IDs
- **Knowledge Hub**: `64c94b2afdeb6fdbaf3b2bd4` (339 articles, image field: `main-image`)
- **Neighborhoods**: `64c94b2afdeb6fdbaf3b2bd0` (27 guides, image field: `featured-header-image`)
- **Services**: `64c94b2afdeb6fdbaf3b2b7f`
- **FAQs**: `64c94b2afdeb6fdbaf3b2b98`
- **Testimonials**: `64c94b2afdeb6fdbaf3b2bb1`
- **EBooks**: `64c94b2afdeb6fdbaf3b2bc5`
- **Software Services**: `65c53189364c6943ff05fd8f`

## Key Page IDs (for static page SEO updates)
- **Homepage**: `64c94b2afdeb6fdbaf3b2b57`
- **About Us**: `64c94b2afdeb6fdbaf3b2b92`
- **Contact Us**: `64c94b2afdeb6fdbaf3b2b95`
- **Software & Support**: `65c51d6775f89b0b0774ca91`
- **Knowledge Hub**: `64c94b2afdeb6fdbaf3b2bc1`
- **Neighborhood Guides**: `64c94b2afdeb6fdbaf3b2bc2`
- **FAQs**: `64c94b2afdeb6fdbaf3b2bc4`
- **Getting Started**: `64c94b2afdeb6fdbaf3b2bbf`
- **Testimonials**: `64c94b2afdeb6fdbaf3b2bce`
- **Our eBooks**: `64c94b2afdeb6fdbaf3b2bc3`

## Webflow API Rate Limits
- 60 requests/minute — use 1.1s delay between requests
- Publish endpoint needs `customDomains` array with domain IDs
- Use exponential backoff on 429 responses

## Completed SEO Work
- Schema markup (JSON-LD) added to all service pages via custom code injection
- CMS alt text: all 339 Knowledge Hub + 27 Neighborhood items complete
- Service page meta descriptions: all populated
- Static page meta descriptions: Homepage, About Us, Software updated
- About Us "out mission" typo fixed

## Remaining SEO Items — Audited March 3, 2026

### Status: Ready-to-paste code + Designer instructions created

**Files created:**
- `seo_fixes_custom_code.js` — JS injection for alt text, heading fixes, schema dedup (paste into Footer Code)
- `seo_head_code_optimizations.html` — Optimized GA/Hotjar/schema for Head Code
- `homepage_maps_async_fix.html` — Async Google Maps for homepage
- `SEO_Remaining_Items_Report.html` — Full audit report with Designer instructions

### 1. Heading Hierarchy (requires Webflow Designer)
- Homepage: H4 "Connect with an expert" → H2
- Homepage + About Us: H5 stats (Founded, Certifications, Areas Served, Our Performance, Commitment) → H3
- Contact Us: 5 H4 form labels → H2
- JS fallback included in `seo_fixes_custom_code.js`

### 2. Static Page Image Alt Text (requires Webflow Designer)
- 60+ images across 6 pages missing alt text
- 28 unique images need alt text; 3 decorative types need role="presentation"
- Software page worst (22/27 missing), Contact Us (8/13 missing)
- JS fallback with complete alt text map in `seo_fixes_custom_code.js`

### 3. Canonical URLs — COMPLETE (no action needed)
- All live pages already have correct canonical tags
- Webflow auto-generates them from published paths
- Verify: Project Settings → SEO → "Auto-generate canonical tag" enabled

### 4. Third-Party Script Optimization (requires Custom Code edit)
- Duplicate GA tags (×2) — remove one pair
- Duplicate LocalBusiness schema (×2) — remove one
- Hotjar blocking → async version in `seo_head_code_optimizations.html`
- Google Maps blocking → async version in `homepage_maps_async_fix.html`
- WebFont/jQuery/Webflow bundles are core and cannot be modified

## API Token Notes
- Current token is a **legacy site API token** (v1 format)
- Works for: Pages SEO, CMS items, Publishing
- Does NOT work for: Custom Code API endpoints (requires OAuth app token)
- Custom code changes must be done via Webflow Designer UI
