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
- Which TikTok search results should be hidden or kept after applying negative words, required words, author filters, and date filters?

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

Supported currencies: `THB`, `CNY`, `VND`, `SGD`, `USD`, `PHP`, `MYR`.

Supported data sources: `tiktok`, `amazon`, `aliexpress`, `1688`, `google_trends`, `xiaohongshu`, `douyin`, `problem`, `creator`.

## TikTok Floating Filter Panel

The web app includes a TikTok page panel that uses the same technical pattern as the Xiaohongshu negative-search skill: a local Node script calls Google Chrome through AppleScript and injects a draggable filter panel into the active TikTok page.

Required macOS Chrome setting:

```text
查看 > 开发者 > 允许 Apple 事件中的 JavaScript
```

Web flow:

1. Run `python3 scripts/web_app.py`.
2. Open `http://127.0.0.1:8765`.
3. Run analysis and click a candidate.
4. Open `TikTok过滤`.
5. Click `安装到已打开的 TikTok 页面`, or click a `tiktok.com` evidence/result link.
6. Chrome opens the TikTok page and installs the right-side floating panel automatically.

The injected TikTok panel supports:

- content exclusion words
- required words
- account / author exclusion words
- start and end date filters
- hiding unknown-date cards
- automatic re-filtering after scroll-loaded content appears
- draggable saved panel position

Direct CLI flow:

```bash
node scripts/tiktok_filter_panel.js \
  --panel \
  --url "https://www.tiktok.com/search?q=pet%20hair%20remover" \
  --negative "广告,招募,代理,私信,agency,hiring,wholesale"
```

Boundaries:

- Only filters content already loaded in the user's Chrome session.
- Does not bypass login, CAPTCHA, risk controls, paywalls, or access restrictions.
- TikTok DOM changes can require selector updates.

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
