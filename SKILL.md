# Novelty Product Scout Skill

Use this skill when a user wants to find and evaluate "novelty" e-commerce product opportunities for TikTok Shop, Douyin, Xiaohongshu, Amazon, Shopify, or cross-border commerce.

## What This Skill Does

This skill automatically collects public web signals for a target audience, market, category, and platform, then turns those signals into a structured product opportunity report.

It helps users answer:

- What novelty products are worth testing now?
- Which candidates belong on a hot-sales, hot-push, content-viral, category-opportunity, or low-risk shortlist?
- Why might this product spread on short video or livestream?
- Is the opportunity already too competitive?
- What keywords should I search on Amazon, AliExpress, 1688, TikTok, or Xiaohongshu?
- What is the first small-budget validation plan?
- What risks should I avoid before buying inventory?

## Best Fit Tasks

Use this skill for:

- Novelty product ideation
- TikTok Shop or Douyin product scouting
- Cross-border product research
- 1688 / AliExpress sourcing keyword generation
- Short-video commerce product validation
- First-batch testing plans for merchants and creators

Do not use this skill for:

- Guaranteed "next viral product" prediction
- Products involving medical claims, food safety, cosmetics compliance, children safety, weapons, or regulated goods without expert review
- Scraping private accounts, logged-in pages, or websites that prohibit automated access
- Making purchasing or inventory decisions without manual verification

## Inputs

The skill accepts a market profile JSON file:

```json
{
  "market": "Thailand",
  "platform": "TikTok Shop",
  "audience": "cat owners",
  "category": "pet supplies",
  "price_range": "300-1200",
  "currency": "THB",
  "ranking_mode": "hot_sales",
  "cycle": "week",
  "min_score": 0,
  "max_risk_count": 3,
  "target_selling_price": "699",
  "product_cost": "180",
  "shipping_cost": "70",
  "platform_fee_rate": "8",
  "return_rate": "3",
  "ad_budget": "3000",
  "data_sources": ["tiktok", "amazon", "aliexpress", "1688", "creator", "problem"],
  "preferences": ["lightweight", "visual demo", "low compliance risk"]
}
```

Optional CSV signals can be provided as a fallback or supplement:

```csv
product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
cat self grooming brush,TikTok,19.99,120,260,4920,38,16,5,18,many demo videos
```

Ranking modes:

- `hot_sales`: current-period sales potential
- `hot_push`: influencer and affiliate push potential
- `content_viral`: short-video demonstration potential
- `category_opportunity`: demand and virality with controllable competition
- `low_risk`: safer first-test shortlist

Cycles: `day`, `week`, or `month`.

Supported currencies: `THB`, `CNY`, `VND`, `SGD`, `USD`, `PHP`, `MYR`.

Supported data sources: `tiktok`, `amazon`, `aliexpress`, `1688`, `google_trends`, `xiaohongshu`, `douyin`, `problem`, `creator`.

## Output

The skill generates a Markdown report with:

1. Product opportunity ranking
2. Leaderboard metrics: sales proxy, GMV proxy, video count, influencer count, live count, commission proxy
3. Data confidence labels: real source link, user CSV data, public web signal, seed inference
4. Score breakdown and competitor density
5. Profit estimate: gross margin, breakeven ROAS, first-test budget implication
6. Evidence links and source snippets
7. Target user and purchase motivation
8. Short-video hook, livestream angle, and three script patterns
9. Multilingual sourcing/search keywords
10. Risk warnings with severity
11. Verification checklist and first validation plan

## How To Run

Beginner mode:

```bash
python3 scripts/scout_products.py
```

Config mode:

```bash
python3 scripts/scout_products.py \
  --market examples/market_profile.json \
  --output output/report.md
```

With manual CSV signals:

```bash
python3 scripts/scout_products.py \
  --market examples/market_profile.json \
  --signals examples/input_signals.csv \
  --output output/report.md
```

Web app mode:

```bash
python3 scripts/web_app.py
```

Then open `http://127.0.0.1:8765`.

## Judging Pitch

This skill helps e-commerce sellers reduce product selection risk. Instead of asking AI to randomly invent product ideas, it collects public demand, content, creator, marketplace, and sourcing signals, ranks candidates like an e-commerce leaderboard, and outputs a small-budget validation plan. It is useful for TikTok Shop sellers, cross-border sellers, creators, private traffic operators, and e-commerce agencies.
