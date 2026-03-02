# Webflow Manual Paste Instructions

These are the exact code blocks you need to paste into specific locations in Webflow.
Each section tells you exactly where to paste and what to paste.

---

## 1. SITE-WIDE: LocalBusiness Schema (CRITICAL)

**Where to paste:** Project Settings → Custom Code → Head Code

**What this does:** Tells Google and AI systems that Gordon James Realty is a real estate business at a specific location. Enables local pack results, knowledge panel, and AI citations.

```html
<!-- Gordon James Realty - LocalBusiness Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Gordon James Realty",
  "image": "https://cdn.prod.website-files.com/64c94b2afdeb6fdbaf3b2b7c/64c94b2afdeb6fdbaf3b2c49_gjr-logo-white.svg",
  "url": "https://www.gordonjamesrealty.com",
  "telephone": "(202) 800-2610",
  "email": "contact@gordonjamesrealty.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1201 15th St NW #400",
    "addressLocality": "Washington",
    "addressRegion": "DC",
    "postalCode": "20005",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 38.905935,
    "longitude": -77.0362679
  },
  "areaServed": [
    {"@type": "AdministrativeArea", "name": "Washington, D.C."},
    {"@type": "AdministrativeArea", "name": "Northern Virginia"},
    {"@type": "AdministrativeArea", "name": "Maryland"}
  ],
  "priceRange": "$$",
  "openingHours": "Mo-Fr 09:00-17:00",
  "sameAs": [
    "https://www.facebook.com/gordonjamesrealty",
    "https://www.linkedin.com/company/gordon-james-realty",
    "https://twitter.com/gjrealty",
    "https://www.pinterest.com/gordonjamesrealty"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Property Management Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Residential Property Management", "url": "https://www.gordonjamesrealty.com/services/residential-property-management"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Commercial Property Management", "url": "https://www.gordonjamesrealty.com/services/commercial-property-management"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Community Association Management", "url": "https://www.gordonjamesrealty.com/services/community-association-management"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Real Estate Brokerage - Buying", "url": "https://www.gordonjamesrealty.com/services/buying-a-property"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Real Estate Brokerage - Selling", "url": "https://www.gordonjamesrealty.com/services/selling-a-property"}}
    ]
  },
  "memberOf": [
    {"@type": "Organization", "name": "National Association of Residential Property Managers (NARPM)"},
    {"@type": "Organization", "name": "National Association of Realtors (NAR)"},
    {"@type": "Organization", "name": "Community Association Managers International Certification Board (CAMICB)"},
    {"@type": "Organization", "name": "Better Business Bureau"}
  ]
}
</script>
```

---

## 2. FAQ PAGE: FAQPage Schema (CRITICAL)

**Where to paste:** Go to the FAQ page in Webflow Designer → Page Settings (gear icon) → Custom Code → Before </body> tag

**What this does:** Makes your 59 FAQs eligible for Google's FAQ rich results (expandable answers directly in search results). This is one of the highest-impact schema types.

**Note:** The full FAQPage schema with all 59 questions is in the file `schema_faq_page.json`. Wrap it in a script tag:

```html
<script type="application/ld+json">
[PASTE CONTENTS OF schema_faq_page.json HERE]
</script>
```

---

## 3. KNOWLEDGE HUB CMS TEMPLATE: BlogPosting Schema

**Where to paste:** In the Webflow Designer, go to your Knowledge Hub CMS Collection Page template → Add an Embed element at the bottom (or use Page Settings → Custom Code → Before </body>)

**What this does:** Tells Google each article is a blog post with a specific author, date, and topic. Enables article rich results in search.

**Important:** If using an Embed element, you can use Webflow's dynamic CMS field references. If using Page Custom Code, you'll need to use a generic version.

### Option A: Using Embed Element (Preferred - supports dynamic fields)

Add an HTML Embed element to the Knowledge Hub template page and insert this code. In Webflow, click the purple "Add Field" button to insert dynamic CMS references where indicated:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "INSERT_CMS_FIELD: Name / Title of the article",
  "description": "INSERT_CMS_FIELD: Post Summary (metadescription)",
  "datePublished": "INSERT_CMS_FIELD: Published Date",
  "dateModified": "INSERT_CMS_FIELD: Published Date",
  "author": {
    "@type": "Organization",
    "name": "Gordon James Realty",
    "url": "https://www.gordonjamesrealty.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Gordon James Realty",
    "logo": {
      "@type": "ImageObject",
      "url": "https://cdn.prod.website-files.com/64c94b2afdeb6fdbaf3b2b7c/64c94b2afdeb6fdbaf3b2c49_gjr-logo-white.svg"
    }
  },
  "image": "INSERT_CMS_FIELD: Main Image URL",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.gordonjamesrealty.com/resources/knowledge-hub/INSERT_CMS_FIELD: Slug"
  }
}
</script>
```

Replace each "INSERT_CMS_FIELD: ..." with the actual Webflow CMS dynamic field reference.

---

## 4. CMS SEO FIELD MAPPINGS (CRITICAL)

**Where:** In Webflow Designer → Knowledge Hub Collection Page → Page Settings (gear icon)

Make sure these mappings are set:

| Webflow Setting | Map To CMS Field |
|---|---|
| **SEO Title** | `Name / Title of the article` |
| **SEO Meta Description** | `Post Summary (metadescription)` |
| **Open Graph Title** | `Name / Title of the article` |
| **Open Graph Description** | `Post Summary (metadescription)` |
| **Open Graph Image** | `Main Image` |

Do the same for Neighborhoods Collection Page:

| Webflow Setting | Map To CMS Field |
|---|---|
| **SEO Title** | `Name` + " Neighborhood Guide | Gordon James Realty" |
| **SEO Meta Description** | `Summary: At a Glance` |
| **Open Graph Title** | `Name` + " DC Area Neighborhood Guide" |
| **Open Graph Description** | `Summary: At a Glance` |
| **Open Graph Image** | `Featured / Header Image` |

---

## 5. ROBOTS.TXT: Verify AI Crawler Access

**Where:** Project Settings → SEO → Sitemap/Robots settings

Make sure your robots.txt does NOT block these AI crawlers:
- `GPTBot` (ChatGPT/OpenAI)
- `Google-Extended` (Google AI/Gemini)
- `Claude-Web` (Claude/Anthropic)
- `CCBot` (Common Crawl, used by many AI systems)
- `Bytespider` (TikTok/ByteDance AI)

If there are any `Disallow` rules for these user agents, remove them.

---

## 6. STATE PAGES: Fix H1 Tags

**Where:** In the Webflow Designer, edit the States CMS Collection Page template

The current H1 on state pages shows "KNowledge Hub" (with the typo). Change it to dynamically display the state name, e.g.:
- H1 should be: `Property Management in [State Name]`

---

## Verification

After making these changes:
1. Publish the site in Webflow
2. Visit https://search.google.com/test/rich-results and test your homepage, FAQ page, and a blog post
3. Visit https://validator.schema.org/ to validate your JSON-LD
4. Check that pages shared on social media show proper previews (use https://developers.facebook.com/tools/debug/)
