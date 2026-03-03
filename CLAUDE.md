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

## Remaining SEO Items (require Webflow Designer or further API work)
- Heading hierarchy on homepage (H4s should be H2/H3)
- Static page hero/icon image alt tags (in page templates, not CMS)
- Canonical URL settings (check Project Settings → SEO)
- Third-party script defer/async optimization
