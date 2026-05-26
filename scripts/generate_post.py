#!/usr/bin/env python3
"""
Auto-generates one Amazon affiliate blog post per run using Google Gemini (free tier).
Rotates through topic categories. Run via GitHub Actions every Tuesday.
"""

import google.generativeai as genai
import os
import datetime
import random
import re

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
TAG = os.environ.get("AMAZON_TAG", "fitnessguru23-21")
today = datetime.date.today()

# ── Topic rotation ────────────────────────────────────────────────────────────
# Add more tuples here to expand coverage. Format: (category_label, [products])
TOPICS = [
    ("kitchen gadgets", [
        "air fryer", "instant pot", "cast iron skillet", "immersion blender", "food processor"
    ]),
    ("home office setup", [
        "ergonomic chair", "standing desk converter", "monitor arm", "USB-C hub", "desk lamp"
    ]),
    ("fitness equipment", [
        "adjustable dumbbells", "resistance bands set", "pull-up bar", "yoga mat", "foam roller"
    ]),
    ("camping and hiking gear", [
        "ultralight tent", "sleeping bag", "trekking poles", "headlamp", "camp stove"
    ]),
    ("smart home devices", [
        "smart plug", "video doorbell", "robot vacuum", "smart thermostat", "air purifier"
    ]),
    ("kitchen knives and tools", [
        "chef knife", "knife sharpener", "cutting board", "kitchen scale", "mandoline slicer"
    ]),
    ("home gym equipment", [
        "barbell and weight set", "power rack", "gymnastic rings", "battle ropes", "ab wheel"
    ]),
    ("travel accessories", [
        "packing cubes", "travel pillow", "portable charger", "luggage scale", "RFID wallet"
    ]),
    ("pet supplies", [
        "dog crate", "automatic feeder", "pet camera", "dog harness", "cat tree"
    ]),
    ("baby and toddler gear", [
        "baby monitor", "convertible car seat", "diaper bag backpack", "baby carrier", "stroller"
    ]),
]

# Pick topic based on week number so it cycles predictably
week = today.isocalendar()[1]
category, products = TOPICS[week % len(TOPICS)]

# ── Prompt ────────────────────────────────────────────────────────────────────
prompt = f"""Write a detailed Amazon affiliate blog post reviewing the top 5 {category} products for 2026.
Products to cover: {', '.join(products)}.

CRITICAL RULES — follow all of these exactly:
1. Every product section must open with a COMPLETELY DIFFERENT sentence structure. No repeated phrases.
2. Each product description must explain specifically WHO this product is best for and WHY — not generic praise.
3. The Drawbacks section for each product must list REAL drawbacks specific to that product, not generic filler.
4. The Bottom Line for each product must be different and specific — never "Great value for money."
5. Use real, well-known products that exist on Amazon with plausible ASINs.
6. All Amazon links must include the affiliate tag: {TAG}
7. Link format: https://www.amazon.com/dp/ASIN?tag={TAG}
8. The comparison table must have columns: Product | Price | Best For (not just "Key Features").
9. Output raw markdown only. No commentary before or after. No code fences.

Frontmatter (include exactly this structure):
---
layout: post
title: "WRITE A SPECIFIC TITLE HERE"
date: {today} 09:00:00
categories: [{category.split()[0]}]
tags: [tag1, tag2, tag3]
description: "SEO meta description under 155 characters"
---

Structure:
- Intro paragraph (2-3 sentences, specific to the category)
- ## Quick Comparison Table
- ## Top 5 [Category] Picks
  - ### 1. [Product Name with link]
  - **Price:** X | **Rating:** X/5
  - Opening paragraph (unique, WHO it's for and WHY)
  - **Highlights:** (3 bullet points, specific)
  - **Drawbacks:** (2 bullet points, product-specific)
  - **Bottom Line:** (1 specific sentence + Amazon link)
  - Repeat for all 5 products
- ## Buying Guide: [Category-specific title]
  - 4 genuine decision factors with explanations
- ## Frequently Asked Questions
  - 4 questions and answers
- ## Final Thoughts
  - Name the top pick and explain why specifically
  - 2-3 sentences on who should choose alternatives
  - Final CTA with Amazon link
- Affiliate disclosure paragraph
"""

# ── Generate ──────────────────────────────────────────────────────────────────
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
content = response.text.strip()

# Strip markdown code fences if Gemini wraps output
if content.startswith("```"):
    content = "\n".join(content.split("\n")[1:])
if content.endswith("```"):
    content = "\n".join(content.split("\n")[:-1])
content = content.strip()

# ── Extract title for filename ────────────────────────────────────────────────
title_match = re.search(r'title:\s*["\'](.+?)["\']', content)
if title_match:
    title_slug = title_match.group(1).lower()
    title_slug = re.sub(r'[^a-z0-9\s-]', '', title_slug)
    title_slug = re.sub(r'\s+', '-', title_slug.strip())
    title_slug = title_slug[:60]
else:
    title_slug = f"best-{category.replace(' ', '-')}-{today.year}"

filename = f"_posts/{today}-{title_slug}.md"

os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Created: {filename}")
print(f"Category: {category}")
print(f"Products: {', '.join(products)}")
