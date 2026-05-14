# Expanded Production Prompt

## Title + Style

Create a 35-second landscape promotional video for “新奇特选品雷达”, an e-commerce skill that turns market, audience, category, price band, ranking mode, and public source signals into a candidate product shortlist with evidence links, risk checks, content angles, sourcing terms, Markdown report, and CSV export.

Use the project design system exactly: background `#080d11`, panel `#0f161b`, field `#0b1318`, foreground `#edf7f4`, muted `#8fa09d`, green `#4ce0a2`, cyan `#63d8ff`, amber `#f2b84b`, danger `#ff6f7d`. Typography: `Space Grotesk` for display, `PingFang SC`/`Microsoft YaHei` for Chinese UI text, `IBM Plex Mono` for data.

## Rhythm Declaration

Pattern: `hook-build-BUILD-PEAK-breathe-CTA`.

The first 5 seconds hook the viewer with the problem and the product promise. The middle builds the workflow: input controls, public source matrix, ranking engine. The peak is the candidate result board with score and confidence. The final scenes breathe into analysis depth and export/verification.

## Global Rules

- Every scene has 2-5 background decoratives: grid, scan lines, ghost labels, signal paths, low-opacity glows.
- Use screenshot assets as real product evidence, with device-frame treatment and motion. Do not iframe the local app.
- Transitions are CSS-based: push/blur and scan wipes. No jump cuts.
- Every scene has entrance animations; only the last scene fades out.
- All numbers use tabular numeric styling.
- Keep claims accurate: “公开信号”, “机会评分”, “估算信号”, “验证链接”.

## Scene 1 — Hook / Problem To Radar

Concept: The viewer starts inside a dark data room where messy platform signals are floating without order. The skill name locks into the frame and signal chips converge into one radar pulse. It should feel like “选品不再靠感觉”.

Mood: cinematic product system reveal, precise and commercial.

Depth layers:
- BG: grid floor, slow green/cyan glow, ghost words “TREND / CONTENT / SUPPLY / RISK”.
- MG: large title “新奇特选品雷达”, subtitle “把公开信号变成可测试商品清单”.
- FG: four signal chips: 趋势、内容、竞品、供应链, plus small radar rings.

Choreography:
- Title SLIDES in from left and tightens tracking.
- Signal chips CASCADE in from four directions.
- Radar rings EXPAND from center and settle.
- Subtitle TYPES on.

Transition out: push/blur to the right, 0.45s, `power3.inOut`.

## Scene 2 — Input Control Console

Concept: The product is not a chat answer; it is a guided skill. The left control console becomes the hero, showing market, platform, audience, category, price band, ranking mode, cycle, collection depth, and source choices.

Mood: operator dashboard, tactical but clean.

Depth layers:
- BG: angled scan grid and tiny metadata labels.
- MG: real screenshot `app-empty.png` in a laptop-like frame.
- FG: floating callouts for “市场 / 人群 / 类目 / 价格带 / 榜单模式”.

Choreography:
- Screenshot DROPS into a device frame with perspective.
- Callouts DRAW connector lines to the screenshot.
- Key input fields PULSE once.
- Metadata bar COUNTS from 0 to “20+ sources”.

Transition out: vertical scan wipe, 0.4s.

## Scene 3 — Source Matrix

Concept: The selected sources fan out as a credible ecosystem, not one black-box API. TikTok, Creative Center, Google Trends, Amazon, Shopee, Lazada, 1688/Alibaba, Meta ads, Reddit/Quora/Pantip/YouTube are shown as source nodes feeding the scoring engine.

Mood: signal routing map, intelligence workflow.

Depth layers:
- BG: route lines and low-opacity source names.
- MG: source nodes grouped into trend/content/marketplace/supply/community/risk.
- FG: center scoring core with labels “去重 / 过滤 / 打分 / 排序”.

Choreography:
- Nodes CASCADE by group.
- Lines DRAW from nodes into center.
- Center core FILLS with four steps.
- Warning note appears: “公开信号 + 估算，不冒充平台真实销量”.

Transition out: chromatic scan wipe, 0.35s.

## Scene 4 — Candidate Ranking Reveal

Concept: The “机会看板” is the payoff. Real result screenshot enters, rows lock into rank positions, top scores glow. The viewer sees not only product names but score, confidence, ranking reason, and detail button.

Mood: decision board, crisp and confident.

Depth layers:
- BG: scoreboard grid, faint score ticks.
- MG: real screenshot `app-results.png` clipped to the results panel.
- FG: enlarged product rows: pet hair remover, cat grooming brush, cat window hammock, interactive cat toy.

Choreography:
- Screenshot SLIDES in and scales to fit.
- Rank rows LOCK in one by one.
- Scores COUNT UP to 84/79/79/79.
- Confidence chips FLASH green.

Transition out: push/blur upward, 0.45s.

## Scene 5 — Deep Analysis, Not A Simple List

Concept: The tool explains why each candidate is worth testing. Tabs fan across the frame: 机会判断、数据证据、供应链、内容脚本、风险核查、测试计划. This scene should prove depth.

Mood: analytical, layered, premium SaaS dashboard.

Depth layers:
- BG: subtle radial panels and tab labels drifting.
- MG: six feature cards with concrete outputs.
- FG: evidence links, risk badge, sourcing keywords, video script snippets.

Choreography:
- Tabs SLIDE across the top like an instrument panel.
- Cards CASCADE in pairs.
- Evidence links BRANCH out from the selected candidate.
- Risk badge DRAWS a warning outline, then settles green/low risk.

Transition out: slow blur crossfade, 0.6s.

## Scene 6 — Output And CTA

Concept: The workflow closes: run skill, shortlist candidates, click source links, export Markdown/CSV, test small budget. The final frame should feel like a practical competition demo, not hype.

Mood: confident close, product-ready.

Depth layers:
- BG: quiet grid, slow glow, final route path.
- MG: workflow line with five steps.
- FG: title “从灵感到首测清单”, CTA “Skill ready for demo”.

Choreography:
- Workflow steps DRAW left to right.
- Export buttons POP in.
- Final title SLAMS softly, then holds.
- End card fades to black in the final 0.5s.

Transition out: final fade only.

## Recurring Motifs

- Signal lines converging into score cards.
- Monospace metadata labels.
- Green as “可信/可行动”, cyan as “数据/链接”, amber as “注意/风险”.
- Real UI screenshots treated as physical dashboard glass.

## Negative Prompt

Avoid generic startup fluff, fake dashboards, fake sales guarantees, purple-blue gradients, decorative orbs, stock imagery, and tiny unreadable UI text. Do not imply paid API integration or exact TikTok Shop sales data.
