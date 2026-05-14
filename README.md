# Novelty Product Scout Skill

This is a competition-ready Skill package for novelty e-commerce product scouting.

## Positioning

Track: E-commerce

Target users:

- TikTok Shop sellers
- Douyin / Xiaohongshu merchants
- Cross-border e-commerce sellers
- Private traffic group-buying operators
- E-commerce agencies
- Livestream creators

Core value:

Automatically collect public product signals, rank novelty product opportunities, and produce a first validation plan before the seller spends money on inventory.

The current version includes five leaderboard modes inspired by e-commerce hot-sale tools:

- Hot sales potential
- Hot push potential
- Content virality
- Category opportunity
- Low-risk testing shortlist

The web app also includes data confidence labels, verification checklists, profit estimates, risk severity, multilingual sourcing keywords, short-video scripts, and export actions.

## Quick Start

Beginner mode:

```bash
python3 scripts/scout_products.py
```

You will be asked for:

- Target market
- Platform
- Audience
- Category
- Price range
- Currency and profit assumptions
- Data sources
- Preferences

The report is generated at:

```text
output/report.md
```

Fast demo mode:

```bash
bash run_demo.sh
```

Web app mode:

```bash
python3 scripts/web_app.py
```

Then open:

```text
http://127.0.0.1:8765
```

Run with example config:

```bash
python3 scripts/scout_products.py \
  --market examples/market_profile.json \
  --output output/report.md
```

Add manual CSV signals:

```bash
python3 scripts/scout_products.py \
  --market examples/market_profile.json \
  --signals examples/input_signals.csv \
  --output output/report.md
```

## Data Sources

The first version uses public web search result pages and optional CSV input. It does not require API keys.

Search templates include:

- TikTok product trend searches
- Influencer / affiliate push searches
- Amazon product searches
- AliExpress sourcing searches
- 1688 sourcing searches
- Google trend-style searches
- Douyin / Xiaohongshu keyword searches
- Short-video product idea searches
- Problem/solution searches for the target audience

Manual CSV can also include sales, GMV, video count, influencer count, live count, and commission rate columns. This keeps the demo stable while still allowing richer real-world data when the seller has it.

## Files

```text
novelty-product-scout-skill/
  SKILL.md
  README.md
  scripts/
    scout_products.py
  examples/
    market_profile.json
    input_signals.csv
  templates/
    opportunity_report.md
```

## Competition Demo

1. Open the web app.
2. Choose market, platform, category, currency, data sources, and profit assumptions.
3. Run analysis to generate the leaderboard.
4. Click a product to inspect opportunity judgment, evidence, sourcing, content scripts, risks, and validation plan.
5. Export CSV or copy the Markdown report.

## Business Value

Product selection is the most upstream e-commerce decision. A wrong product wastes ad budget, content production, sourcing effort, and inventory cash. This Skill reduces selection risk by turning public trend and marketplace signals into a structured product scoring report and test plan.
