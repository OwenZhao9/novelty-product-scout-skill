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

## TikTok Page Filter Panel

The web app can also install a Xiaohongshu-skill-style floating panel directly into a TikTok page opened in Google Chrome.

One-time Chrome setup on macOS:

```text
Google Chrome > View > Developer > Allow JavaScript from Apple Events
```

Chinese Chrome menu:

```text
查看 > 开发者 > 允许 Apple 事件中的 JavaScript
```

Use it from the web app:

1. Start the web app and open `http://127.0.0.1:8765`.
2. Run product analysis.
3. Click a candidate product.
4. Open the `TikTok过滤` tab.
5. Click `安装到已打开的 TikTok 页面`, or click any `tiktok.com` result link.
6. The app opens the TikTok page in Google Chrome and installs the right-side floating panel automatically.

The TikTok floating panel supports:

- content exclusion words
- required words
- account / author exclusion words
- date range filtering
- hiding cards with unknown dates
- automatic filtering for newly loaded cards while scrolling
- draggable position with saved placement

CLI usage is also available:

```bash
node scripts/tiktok_filter_panel.js \
  --panel \
  --url "https://www.tiktok.com/search?q=pet%20hair%20remover" \
  --negative "广告,招募,代理,私信,agency,hiring,wholesale"
```

This feature only works on content already visible or loaded in the user's Chrome session. It does not bypass login, CAPTCHA, platform limits, or access controls.

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
    web_app.py
    tiktok_filter_panel.js
  web/
    index.html
    app.js
    styles.css
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
5. Use `TikTok过滤` to either review collected TikTok evidence inside the tool or install the floating panel into a Chrome TikTok page.
6. Export CSV or copy the Markdown report.

## Business Value

Product selection is the most upstream e-commerce decision. A wrong product wastes ad budget, content production, sourcing effort, and inventory cash. This Skill reduces selection risk by turning public trend and marketplace signals into a structured product scoring report and test plan.
