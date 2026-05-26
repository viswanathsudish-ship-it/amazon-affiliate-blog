#!/usr/bin/env python3
"""
Auto-generates one Amazon affiliate blog post per run using Google Gemini (free tier).
Rotates through 30 specific low-competition long-tail topics.
Run via GitHub Actions Mon/Wed/Fri.
"""

import google.generativeai as genai
import os
import datetime
import re

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
TAG = os.environ.get("AMAZON_TAG", "fitnessguru23-21")
today = datetime.date.today()

# ── 30 specific long-tail topics — low competition, high buyer intent ──────────
# Format: (category_slug, commission_tier, search_query, [5 specific products])
# High-commission categories prioritised: furniture 8%, home-improvement 8%,
# lawn-garden 8%, luxury-beauty 10%, musical-instruments 6%, kitchen 4.5%

TOPICS = [
    # ── HOME IMPROVEMENT — 8% commission ─────────────────────────────────────
    ("home-improvement", "8%", "best cordless drill for home renovation beginners",
     ["DeWalt 20V MAX Cordless Drill", "BLACK+DECKER 20V Drill Driver", "Ryobi One+ 18V Drill",
      "Milwaukee M12 Compact Drill", "Makita 18V LXT Drill"]),

    ("home-improvement", "8%", "best LED under cabinet lighting for kitchen counters",
     ["Brilliant Evolution Wireless LED Puck Lights", "Kichler Direct-Wire LED Strip",
      "Litever LED Strip Light Kit", "Wobane Under Cabinet Lighting", "BarineCraft LED Tape Light"]),

    ("home-improvement", "8%", "best weatherstripping for drafty old windows and doors",
     ["M-D Building Products Door Seal", "Frost King Door Weatherstrip", "KELIIYO Weather Stripping",
      "SugarBoo Door Draft Stopper", "Duck Brand Self-Adhesive Foam"]),

    ("home-improvement", "8%", "best tile grout sealer for shower walls and floors",
     ["Aqua Mix Sealer's Choice Gold", "Miracle Sealants 511 Impregnator", "Black Diamond Ultimate Grout Sealer",
      "Tuff Duck Granite Grout Sealer", "StoneTech BulletProof Sealer"]),

    ("home-improvement", "8%", "best paint roller for smooth walls without texture",
     ["Purdy White Dove Roller Cover", "Wooster Brush Roller", "Shur-Line Paint Roller",
      "ArroWorthy Microfiber Roller", "Hyde Tools 9-Inch Roller Frame"]),

    ("home-improvement", "8%", "best caulk gun for bathroom and kitchen sealing",
     ["Newborn 930-GTD Caulking Gun", "Milwaukee 2441-20 M12 Caulk Gun",
      "Ryobi PCL540B Cordless Caulk Gun", "DRIPLESS ETS2000 Caulking Gun",
      "Cox 41004 Professional Caulking Gun"]),

    # ── FURNITURE — 8% commission ─────────────────────────────────────────────
    ("furniture", "8%", "best office chair for lower back pain under 300 dollars",
     ["Humanscale Freedom Chair", "HON Ignition 2.0 Task Chair", "Serta Big and Tall Executive Chair",
      "Modway Articulate Ergonomic Chair", "Flash Furniture Ergonomic Mesh Chair"]),

    ("furniture", "8%", "best bookshelf for small bedroom with lots of books",
     ["VASAGLE Industrial Ladder Shelf", "Prepac Elite Bookcase", "Sauder Beginnings 5-Shelf Bookcase",
      "Furinno 5-Tier Bookcase", "Better Homes Cube Organizer"]),

    ("furniture", "8%", "best bed frame for heavy person that does not squeak",
     ["Zinus SmartBase Steel Bed Frame", "Olee Sleep T-3000 Steel Slat", "DHP Manila Metal Bed Frame",
      "LINENSPA Metal Platform Bed Frame", "Modway Aveline Bed Frame"]),

    ("furniture", "8%", "best outdoor patio chairs for heavy people that last",
     ["Lifetime Convertible Folding Chair", "Flash Furniture Hercules Folding Chair",
      "Melnor Heavy Duty Adirondack Chair", "Adams Manufacturing Big Easy Chair",
      "PORTAL Heavy Duty Camping Chair"]),

    # ── LAWN AND GARDEN — 8% commission ──────────────────────────────────────
    ("lawn-garden", "8%", "best cordless lawn mower for small yard under quarter acre",
     ["Greenworks 40V Cordless Lawn Mower", "EGO Power+ 21-Inch Mower", "Ryobi 40V Brushless Mower",
      "Sun Joe MJ401E Electric Mower", "BLACK+DECKER 36V Cordless Mower"]),

    ("lawn-garden", "8%", "best raised garden bed kit for beginners in small backyard",
     ["Vego Garden 17-In Tall Raised Bed", "FOYUEE Galvanized Raised Garden Bed", "Greenes Fence Cedar Raised Bed",
      "Keter Eden Raised Garden Bed", "Birdies 6-in-1 Metal Raised Bed"]),

    ("lawn-garden", "8%", "best soaker hose for vegetable garden watering",
     ["Melnor Flat Soaker Garden Hose", "Swan Products Element Soaker Hose",
      "Gilmour Flat Weeper Soaker Hose", "Rocky Mountain Goods Soaker Hose",
      "BUYOOKAY Drip Irrigation Soaker Hose"]),

    ("lawn-garden", "8%", "best compost bin for small backyard that keeps pests out",
     ["FCMP Outdoor IM4000 Tumbler", "Envirocycle Composter Tumbler", "Maze Compost Tumbler",
      "Jora JK270 Compost Tumbler", "OXO Good Grips Easy Clean Compost Bin"]),

    ("lawn-garden", "8%", "best garden kneeler and seat for elderly gardeners",
     ["Goplus Garden Kneeler and Seat", "Tierra Garden Kneeler", "Fiskars Kneeling Pad",
      "CobraCo Garden Kneeler Bench", "AEUREX Garden Kneeler with Tool Bag"]),

    # ── LUXURY BEAUTY — 10% commission ───────────────────────────────────────
    ("luxury-beauty", "10%", "best face serum for dark spots and hyperpigmentation over 40",
     ["TruSkin Vitamin C Serum", "Neutrogena Rapid Tone Repair Serum", "Murad Rapid Age Spot Corrector",
      "Peter Thomas Roth Potent-C Power Serum", "Paula's Choice C15 Super Booster"]),

    ("luxury-beauty", "10%", "best retinol cream for beginners with sensitive skin",
     ["RoC Retinol Correxion Line Smoothing Serum", "Neutrogena Rapid Wrinkle Repair",
      "CeraVe Skin Renewing Retinol Serum", "Olay Regenerist Retinol24",
      "L'Oreal Paris Revitalift 0.3% Pure Retinol"]),

    ("luxury-beauty", "10%", "best hair mask for damaged color treated hair",
     ["Olaplex No.8 Bond Intense Moisture Mask", "Moroccanoil Intense Hydrating Mask",
      "Briogeo Don't Despair Repair Mask", "SheaMoisture Manuka Honey Masque",
      "Redken Extreme Strength Builder Plus Mask"]),

    ("luxury-beauty", "10%", "best sunscreen for oily skin that doesn't pill under makeup",
     ["EltaMD UV Clear Broad-Spectrum SPF 46", "La Roche-Posay Anthelios SPF 60",
      "Supergoop Unseen Sunscreen SPF 40", "Black Girl Sunscreen SPF 30",
      "Neutrogena Clear Face SPF 55"]),

    # ── MUSICAL INSTRUMENTS — 6% commission ──────────────────────────────────
    ("musical-instruments", "6%", "best beginner acoustic guitar under 200 dollars for adults",
     ["Fender CD-60S Acoustic Guitar", "Yamaha FG800 Acoustic Guitar", "Seagull S6 Original Acoustic",
      "Jasmine S35 Acoustic Guitar", "Taylor Academy 10 Acoustic Guitar"]),

    ("musical-instruments", "6%", "best keyboard piano for adult beginners learning at home",
     ["Casio CT-S300 Portable Keyboard", "Yamaha P-45 Digital Piano", "Roland FP-30X Digital Piano",
      "Alesis Recital 88-Key Digital Piano", "Casio PX-S1100 Privia Digital Piano"]),

    ("musical-instruments", "6%", "best ukulele for kids age 8 to 12 learning music",
     ["Kala KA-15S Soprano Ukulele", "Donner DUS-1 Soprano Ukulele", "Mahalo Rainbow Ukulele",
      "Luna Tattoo Concert Ukulele", "Lanikai LU-21S Soprano Ukulele"]),

    # ── KITCHEN — 4.5% commission ─────────────────────────────────────────────
    ("kitchen", "4.5%", "best cast iron skillet for glass top stove cooking",
     ["Lodge L8SK3 10.25-Inch Cast Iron Skillet", "Le Creuset Signature Cast Iron Skillet",
      "Utopia Kitchen Pre-Seasoned Cast Iron", "Victoria Cast Iron Skillet",
      "Camp Chef 12-Inch Seasoned Cast Iron"]),

    ("kitchen", "4.5%", "best immersion blender for blending hot soup in pot",
     ["Braun MultiQuick 5 Hand Blender", "KitchenAid KHBV53 Variable Speed Blender",
      "Mueller Ultra-Stick Immersion Blender", "Vitamix Immersion Blender",
      "Cuisinart CSB-179 Smart Stick Blender"]),

    ("kitchen", "4.5%", "best kitchen scale for baking bread with grams accuracy",
     ["OXO Good Grips Stainless Food Scale", "Escali Primo Digital Scale",
      "My Weigh KD-8000 Baker's Scale", "Greater Goods Digital Food Scale",
      "Nicewell Food Scale Digital Kitchen"]),

    # ── FITNESS — 3% commission ───────────────────────────────────────────────
    ("fitness", "3%", "best adjustable dumbbells for small apartment home gym",
     ["Bowflex SelectTech 552 Dumbbells", "PowerBlock Elite Dumbbell Set",
      "NordicTrack Select-A-Weight Dumbbell", "ATIVAFIT Adjustable Dumbbell",
      "Merax Deluxe Adjustable Dumbbell"]),

    ("fitness", "3%", "best resistance bands set for physical therapy exercises",
     ["TheraBand Resistance Band Set", "THERABAND CLX Consecutive Loop Bands",
      "Fit Simplify Resistance Loop Bands", "SPRI Xertube Resistance Bands",
      "Serious Steel Assisted Pull-Up Bands"]),

    # ── PET SUPPLIES — 3% commission ─────────────────────────────────────────
    ("pet-supplies", "3%", "best dog bed for large dogs that chew and destroy beds",
     ["K9 Ballistics Tough Orthopedic Dog Bed", "Kuranda Dog Bed Chew Proof",
      "Big Barker 7-Inch Pillow Top Orthopedic Bed", "Molly Mutt Dog Bed Cover",
      "PetFusion Ultimate Dog Bed"]),

    ("pet-supplies", "3%", "best automatic cat feeder for two cats on a schedule",
     ["PETLIBRO Automatic Cat Feeder", "PetSafe 5-Meal Automatic Feeder",
      "HoneyGuaridan Automatic Pet Feeder", "Cat Mate C500 5-Meal Feeder",
      "WOPET Automatic Pet Feeder"]),

    # ── HOME OFFICE — 3% commission ───────────────────────────────────────────
    ("home-office", "3%", "best monitor arm for dual screen desk setup under 50 dollars",
     ["HUANUO Dual Monitor Stand", "VIVO Dual Monitor Desk Mount", "Ergotech Freedom Arm",
      "AmazonBasics Premium Single Monitor Arm", "Fully Jarvis Single Monitor Arm"]),
]

# Pick topic based on week number + day so Mon/Wed/Fri each get a different topic
week = today.isocalendar()[1]
day = today.weekday()   # 0=Mon, 2=Wed, 4=Fri
offset = {0: 0, 2: 1, 4: 2}.get(day, 0)
index = (week * 3 + offset) % len(TOPICS)

category_slug, commission, search_query, products = TOPICS[index]

# ── Prompt ────────────────────────────────────────────────────────────────────
prompt = f"""Write a detailed Amazon affiliate blog post targeting this exact search query: "{search_query}"

Products to review: {', '.join(products)}
Category commission rate: {commission}

CRITICAL RULES — follow every one exactly:
1. The title must match or closely paraphrase the search query — this is what people typed into Google.
2. Every product section MUST open with a COMPLETELY DIFFERENT sentence structure.
3. Each product description explains specifically WHO this is best for and WHY — not generic praise.
4. Drawbacks must be REAL and SPECIFIC to that product — never "may require a learning curve".
5. Bottom Line for each product must be unique and specific — never "great value for money".
6. Comparison table columns: Product | Price | Best For
7. All Amazon links must include tag: {TAG}. Format: https://www.amazon.com/dp/ASIN?tag={TAG}
8. Use real ASINs for the listed products.
9. Output raw markdown only — no commentary, no code fences.
10. Intro must address the specific pain point behind this search query in 2-3 sentences.

Frontmatter — include exactly:
---
layout: post
title: "TITLE MATCHING THE SEARCH QUERY"
date: {today} 09:00:00
categories: [{category_slug}]
tags: [tag1, tag2, tag3]
description: "SEO meta description under 155 characters targeting the exact search query"
---

Structure:
- Intro (2-3 sentences addressing the pain point)
- ## Quick Comparison Table
- ## Top 5 Picks (with specific category title)
  - ### 1. [Product with affiliate link]
  - **Price:** X | **Rating:** X/5
  - Unique opening paragraph (WHO + WHY)
  - **Highlights:** 3 specific bullets
  - **Drawbacks:** 2 product-specific bullets
  - **Bottom Line:** 1 specific sentence + CTA link
  - (repeat for all 5)
- ## Buying Guide (specific to this query)
- ## FAQ (4 questions specific to this search)
- ## Final Thoughts
- Affiliate disclosure
"""

# ── Generate ──────────────────────────────────────────────────────────────────
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
content = response.text.strip()

# Strip markdown code fences if present
if content.startswith("```"):
    content = "\n".join(content.split("\n")[1:])
if content.endswith("```"):
    content = "\n".join(content.split("\n")[:-1])
content = content.strip()

# ── Build filename from search query ─────────────────────────────────────────
slug = re.sub(r'[^a-z0-9\s-]', '', search_query.lower())
slug = re.sub(r'\s+', '-', slug.strip())[:60]
filename = f"_posts/{today}-{slug}.md"

os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Created:   {filename}")
print(f"Category:  {category_slug} ({commission} commission)")
print(f"Query:     {search_query}")
