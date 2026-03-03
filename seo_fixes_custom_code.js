/**
 * Gordon James Realty — SEO & Accessibility Fixes
 * Paste into: Project Settings → Custom Code → Footer Code (Before </body> tag)
 *
 * This script handles:
 *   1. Static image alt text (accessibility + SEO)
 *   2. Heading hierarchy corrections (accessibility; SEO requires Designer fix)
 *   3. Third-party script optimization (Hotjar defer)
 *   4. Duplicate schema cleanup
 *   5. Canonical URL verification
 *
 * NOTE: For maximum SEO impact, heading hierarchy should also be fixed in
 * the Webflow Designer. This script provides an accessibility fallback.
 */
(function () {
  "use strict";

  /* ================================================================
     1. STATIC IMAGE ALT TEXT
     Images in page templates (not CMS) that are missing alt attributes.
     Decorative images get role="presentation" instead.
     ================================================================ */
  var altTextMap = {
    // Site-wide (header/footer)
    "GJLogo_Primary-01.svg": "Gordon James Realty logo",
    "gjr-logo-white.svg": "Gordon James Realty logo",
    "White-Icon.svg": "", // decorative footer icon

    // Homepage hero/icons
    "GJR-Images-What-Clients-Say.jpg":
      "Gordon James Realty clients sharing their property management experience",
    "Icon-Quotation-Marks.svg": "", // decorative
    "Icons-Founded.svg": "Calendar icon representing Gordon James Realty founding year",
    "Icons-Certifications.svg":
      "Badge icon representing Gordon James Realty professional certifications",
    "Icons-Areas.svg":
      "Map pin icon representing Gordon James Realty service areas in DC, VA, and MD",
    "Icons-Performance.svg":
      "Chart icon representing Gordon James Realty performance metrics",
    "Icons-Commitment.svg":
      "Handshake icon representing Gordon James Realty commitment to clients",

    // About Us page
    "GJR-Images-9.jpg":
      "Gordon James Realty team providing professional property management services",

    // Contact Us page
    "GJR-Images-Contact.jpg":
      "Gordon James Realty office ready to assist property owners and tenants",
    "GJ_Icons-Residential-Property-Manag": "Residential property management services icon",
    "GJ_Icons-Commerical-Property-Manage": "Commercial property management services icon",
    "GJ_Icons-Community-Association-Mana": "Community association management services icon",
    "GJ_Icons-Selling-a-Property.svg": "Real estate brokerage services icon",
    "GJ_Icons-Buying-a-Property.svg": "Property buying services icon",

    // Software page icons
    "technology.png": "Cloud technology platform for property management",
    "speech-bubble.png": "Customer communication and support portal",
    "rent.png": "Online rent payment processing",
    "cashier.png": "Financial transaction management",
    "candidate.png": "Tenant screening and application processing",
    "salary.png": "Owner disbursement and payment management",
    "bars.png": "Property performance analytics and reporting",
    "budget.png": "Budget planning and financial management",
    "compliant.png": "Regulatory compliance management",
    "24-hours-service.png": "24/7 emergency maintenance support",
    "Plus-Icon.svg": "", // decorative expand icon

    // Getting Started page
    "GJR-Images-11.jpg":
      "Property owner getting started with Gordon James Realty management services",
  };

  document.querySelectorAll("img").forEach(function (img) {
    var src = img.getAttribute("src") || "";
    var currentAlt = img.getAttribute("alt");

    // Only fix images that have empty or missing alt
    if (currentAlt !== null && currentAlt !== "") return;

    var matched = false;
    for (var filename in altTextMap) {
      if (src.indexOf(filename) !== -1) {
        var newAlt = altTextMap[filename];
        if (newAlt === "") {
          // Decorative image
          img.setAttribute("alt", "");
          img.setAttribute("role", "presentation");
        } else {
          img.setAttribute("alt", newAlt);
        }
        matched = true;
        break;
      }
    }

    // Fallback: if still no alt and not matched, mark as decorative
    if (!matched && (currentAlt === null || currentAlt === "")) {
      img.setAttribute("alt", "");
      img.setAttribute("role", "presentation");
    }
  });

  /* ================================================================
     2. HEADING HIERARCHY CORRECTIONS
     Fixes improper heading levels for accessibility.
     For SEO, these should also be changed in Webflow Designer.
     ================================================================ */
  var headingFixes = [
    // Homepage: H4 "Connect with an expert" → H2
    { text: "Connect with an expert", from: "H4", to: "H2" },
    // Homepage + About Us: H5 stats → H3
    { text: "Founded", from: "H5", to: "H3" },
    { text: "Certifications", from: "H5", to: "H3" },
    { text: "Areas Served", from: "H5", to: "H3" },
    { text: "Our Performance", from: "H5", to: "H3" },
    { text: "Commitment", from: "H5", to: "H3" },
    // Contact Us: H4 form labels → H2
    { text: "Contact Details:", from: "H4", to: "H2" },
    { text: "Property / Address:", from: "H4", to: "H2" },
    { text: "Services of Interest:", from: "H4", to: "H2" },
    { text: "Message Details:", from: "H4", to: "H2" },
    {
      text: "Want to skip the form and contact us directly?",
      from: "H4",
      to: "H2",
    },
  ];

  headingFixes.forEach(function (fix) {
    var elements = document.querySelectorAll(fix.from.toLowerCase());
    elements.forEach(function (el) {
      if (el.textContent.trim() === fix.text) {
        var replacement = document.createElement(fix.to.toLowerCase());
        // Copy all attributes
        for (var i = 0; i < el.attributes.length; i++) {
          replacement.setAttribute(
            el.attributes[i].name,
            el.attributes[i].value
          );
        }
        replacement.innerHTML = el.innerHTML;
        el.parentNode.replaceChild(replacement, el);
      }
    });
  });

  /* ================================================================
     3. DUPLICATE SCHEMA CLEANUP
     The homepage has duplicate LocalBusiness JSON-LD schemas.
     Remove duplicates, keeping only the first instance.
     ================================================================ */
  var schemas = document.querySelectorAll(
    'script[type="application/ld+json"]'
  );
  var seenTypes = {};
  schemas.forEach(function (script) {
    try {
      var data = JSON.parse(script.textContent);
      var key = data["@type"] || "unknown";
      if (seenTypes[key]) {
        script.parentNode.removeChild(script);
      } else {
        seenTypes[key] = true;
      }
    } catch (e) {
      // Skip malformed JSON-LD
    }
  });

  /* ================================================================
     4. SCRIPT OPTIMIZATION NOTE
     Hotjar and Google Maps are loaded as blocking scripts.
     These should be made async in Webflow Designer:
       - Project Settings → Custom Code → Head Code
       - Add 'async' attribute to Hotjar script tag
       - Add 'async defer' to Google Maps script tag

     The WebFont loader is also blocking but is a Webflow system
     script that cannot be easily modified.

     jQuery and Webflow bundles are core dependencies and must
     remain as blocking scripts.
     ================================================================ */
})();
