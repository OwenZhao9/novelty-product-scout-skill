const form = document.querySelector("#scoutForm");
const statusPill = document.querySelector("#statusPill");
const runButton = document.querySelector("#runButton");
const ranking = document.querySelector("#ranking");
const detail = document.querySelector("#detail");
const emptyState = document.querySelector("#emptyState");
const candidateCount = document.querySelector("#candidateCount");
const topScore = document.querySelector("#topScore");
const activeMode = document.querySelector("#activeMode");
const highConfidence = document.querySelector("#highConfidence");
const markdownReport = document.querySelector("#markdownReport");
const exampleButton = document.querySelector("#exampleButton");
const clearButton = document.querySelector("#clearButton");
const copyReportButton = document.querySelector("#copyReportButton");
const exportCsvButton = document.querySelector("#exportCsvButton");
const sourceStatus = document.querySelector("#sourceStatus");
const presetSelects = document.querySelectorAll(".preset-select");
const unlimitedToggles = document.querySelectorAll(".unlimited-toggle");
const priceMinInput = form.elements.price_min;
const priceMaxInput = form.elements.price_max;
const selectOnFocusInputs = document.querySelectorAll('input[name="price_min"], input[name="price_max"]');

let allCandidates = [];
let candidates = [];
let activeIndex = 0;

const audiencePresets = [
  "养猫人群", "养狗人群", "宠物主人", "小户型养宠人群", "新手铲屎官",
  "新手父母", "孕妇", "新手妈妈", "幼儿父母", "学生家长", "老人护理人群", "银发人群",
  "大学生", "高中生", "年轻白领", "办公室人群", "远程办公人群", "教师", "护士", "小商家",
  "内容创作者", "直播卖家", "短视频达人", "游戏玩家", "手机摄影用户",
  "家庭做饭人群", "烘焙爱好者", "咖啡爱好者", "备餐人群", "清洁爱好者", "收纳爱好者",
  "租房人群", "小户型家庭", "养植物人群", "美妆用户", "护肤用户", "化妆新手",
  "护发用户", "美甲用户", "健身新手", "瑜伽人群", "居家健身人群", "跑步人群",
  "骑行人群", "露营人群", "汽车用户", "摩托车用户", "网约车司机", "旅行人群",
  "背包客", "商务差旅人群", "礼物购买者", "派对主办者", "手作爱好者", "园艺人群",
  "穆斯林女性", "预算型消费者", "冲动消费人群"
];

const categoryPresets = [
  "宠物用品", "宠物梳毛工具", "宠物玩具", "宠物喂食用品", "宠物清洁用品", "宠物出行配件",
  "宠物窝垫家具", "猫用品", "狗用品", "家居收纳", "收纳盒/收纳架", "衣柜收纳", "桌面收纳",
  "鞋类收纳", "洗衣配件", "清洁工具", "地面清洁工具", "除尘工具", "厨房清洁工具",
  "浴室用品", "家居装饰", "墙面装饰", "节日装饰", "灯具照明", "氛围灯", "夜灯",
  "智能家居小工具", "厨房小工具", "厨房收纳", "烹饪工具", "切削削皮工具", "杯壶水具",
  "咖啡配件", "茶饮配件", "烘焙工具", "食品保鲜收纳", "美妆工具", "个护工具",
  "护肤仪器", "洁面工具", "美发工具", "化妆配件", "美甲工具", "按摩工具", "沐浴身体护理",
  "手机配件", "电子配件", "充电配件", "线缆收纳", "手机支架", "平板配件",
  "电脑配件", "桌面设备", "键鼠配件", "相机配件", "创作者设备", "直播配件", "音频配件",
  "可穿戴配件", "汽车配件", "摩托车配件", "汽车清洁工具", "车载收纳", "车载手机支架",
  "汽车内饰", "户外装备", "露营装备", "旅行配件", "行李收纳", "便携旅行小工具",
  "运动配件", "健身配件", "瑜伽配件", "跑步配件", "居家健身器材", "母婴用品",
  "母婴配件", "婴儿喂养用品", "婴儿安全用品", "婴儿车配件", "办公小物", "学习用品",
  "文具", "桌面配件", "学习工具", "玩具兴趣", "益智玩具", "解压玩具", "收藏品",
  "派对用品", "礼品包装", "DIY 工具", "手动工具", "家装修理小工具", "园艺工具",
  "植物护理工具", "时尚配件", "发饰", "围巾帽子", "饰品配件", "包袋行李", "钱包卡包",
  "旅行包", "鞋类配件", "穆斯林时尚配件", "健康护理配件", "睡眠配件", "体态矫正配件",
  "居家安全用品", "节日季节产品", "环保产品", "数码产品配件"
];

const sampleProfiles = {
  pet: {
    match: ["宠物", "猫", "狗"],
    seeds: "cat grooming brush, pet hair remover, cat window hammock, interactive cat toy",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
self-grooming cat brush,TikTok Shop,399,120,260,103740,38,16,5,18,画面演示强; 猫会主动蹭; 重量轻
cat window hammock,Amazon,699,80,140,97860,19,6,1,12,使用场景明确; 竞品较多; 礼物属性好
pet grooming glove,AliExpress,299,200,320,95680,45,22,4,20,前后对比明显; 货源便宜; 市场较拥挤
foldable cat tunnel bed,TikTok Shop,599,65,90,53910,24,9,2,15,视频行为有趣; 包裹偏大; 礼品季适合`,
  },
  jewelry: {
    match: ["饰品", "珠宝", "发饰", "项链", "戒指", "耳环", "手链"],
    seeds: "travel jewelry organizer, anti-tangle necklace organizer, magnetic earring holder, adjustable ring sizer, hair accessory organizer",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
travel jewelry organizer case,TikTok Shop,349,160,280,97720,42,18,3,20,打开前后对比明显; 适合旅行场景; 轻小件
anti-tangle necklace organizer box,Amazon,499,110,190,94810,26,9,1,15,解决项链打结痛点; 礼物属性强; 可做套装
magnetic earring display stand,AliExpress,259,95,150,38850,21,8,2,18,展示效果强; 适合直播陈列; 供应链容易
adjustable ring sizer,TikTok Shop,199,70,120,23880,18,6,1,12,工具属性明确; 内容演示简单; 客单价偏低`,
  },
  beauty: {
    match: ["美妆", "护肤", "美甲", "个护", "美发", "洁面", "按摩"],
    seeds: "makeup organizer, nail art tools, makeup brush cleaner, skincare tool, portable makeup mirror",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
makeup brush cleaning mat,TikTok Shop,299,130,240,71760,36,14,3,18,前后对比明显; 易拍清洁过程; 轻小件
portable lighted makeup mirror,Amazon,599,90,160,95840,22,8,2,15,场景明确; 适合通勤旅行; 竞品较多
magnetic nail practice stand,AliExpress,269,70,110,29590,18,7,1,16,适合美甲教程; 供应链容易; 内容垂直
ice globe facial massager,TikTok Shop,399,85,130,51870,24,9,2,12,视觉演示强; 需注意功效宣称风险`,
  },
  electronics: {
    match: ["手机", "电子", "充电", "电脑", "桌面", "相机", "直播", "音频", "数码"],
    seeds: "phone stand, magnetic charging cable, desk cable organizer, livestream ring light, camera accessories",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
foldable magnetic phone stand,TikTok Shop,399,150,260,103740,34,15,4,16,演示角度多; 办公车载都可用; 轻小件
desk cable clips,Amazon,199,100,210,41790,20,7,1,12,痛点明确; 客单价低; 可组合销售
phone clip ring light,AliExpress,499,85,150,74850,24,11,3,15,创作者场景明确; 适合直播演示
mini keyboard cleaning brush,TikTok Shop,159,120,180,28620,28,10,1,10,清洁前后对比强; 采购低; 同质化偏高`,
  },
  home: {
    match: ["家居", "收纳", "清洁", "厨房", "浴室", "灯", "装饰"],
    seeds: "kitchen storage, bathroom cleaning tool, desk organizer, dust cleaning tool, ambient light",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
no-drill rotating storage rack,TikTok Shop,499,150,240,119760,32,12,3,16,安装演示简单; 收纳前后对比强
gap dust cleaning brush,Amazon,199,170,300,59700,38,16,2,14,清洁画面解压; 轻小件; 同质化较高
sink drain storage basket,AliExpress,299,90,150,44850,20,7,1,12,厨房场景明确; 采购容易; 适合组合销售
motion sensor night light,TikTok Shop,399,80,130,51870,18,6,1,10,夜间演示强; 注意电池和认证风险`,
  },
  generic: {
    match: [],
    seeds: "novelty gadget, visual demo product, lightweight small product, giftable product",
    csv: `product,source,price,mentions,sales,gmv,video_count,influencer_count,live_count,commission_rate,notes
portable organizer gadget,TikTok Shop,299,80,120,35880,18,6,1,12,轻小件; 可做前后对比; 适合测试
creative gift gadget,Amazon,399,60,90,35910,14,5,1,10,礼物属性; 需要验证真实需求`,
  },
};

const sampleFingerprints = Object.values(sampleProfiles).map((profile) => profile.seeds);

localizePresetLists();
syncPriceRange();
populatePresetSelects();
loadSourceStatus();

presetSelects.forEach((select) => {
  select.addEventListener("change", () => {
    const target = form.elements[select.dataset.fill];
    if (target && select.value) {
      target.value = select.value;
      if (select.dataset.fill === "category") {
        applyCategorySample(select.value);
      }
    }
  });
});

form.category.addEventListener("change", () => {
  if (!form.data_source_mode || form.data_source_mode.value === "public") {
    applyCategorySample(form.category.value);
  }
});

unlimitedToggles.forEach((toggle) => {
  toggle.addEventListener("change", () => {
    applyUnlimitedToggle(toggle);
  });
});

selectOnFocusInputs.forEach((input) => {
  input.addEventListener("focus", () => {
    window.requestAnimationFrame(() => input.select());
  });
  input.addEventListener("mouseup", (event) => {
    event.preventDefault();
  });
  input.addEventListener("input", syncPriceRange);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  syncPriceRange();
  setRunning(true);
  try {
    const data = new FormData(form);
    const payload = {
      profile: {
        market: data.get("market"),
        platform: data.get("platform"),
        data_source_mode: data.get("data_source_mode") || "public",
        audience: unlimitedValue("audience", data.get("audience")),
        category: unlimitedValue("category", data.get("category")),
        price_range: unlimitedValue("price_range", data.get("price_range")),
        currency: data.get("currency"),
        ranking_mode: data.get("ranking_mode"),
        cycle: data.get("cycle"),
        data_sources: data.getAll("data_sources"),
        preferences: data.get("preferences"),
        seed_keywords: data.get("seed_keywords"),
      },
      signals_csv: "",
      no_web: data.get("no_web") === "on",
      limit: Number(data.get("limit") || 3),
    };

    const response = await fetch("/api/scout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok || result.error) {
      throw new Error(result.error || "Failed to run scout");
    }
    allCandidates = result.candidates || [];
    candidates = visibleCandidates();
    activeIndex = 0;
    renderResults(result);
    statusPill.textContent = "Done";
    statusPill.className = "status-pill";
  } catch (error) {
    statusPill.textContent = "Error";
    statusPill.className = "status-pill error";
    emptyState.hidden = false;
    emptyState.textContent = error.message;
  } finally {
    setRunning(false);
  }
});

exampleButton.addEventListener("click", () => {
  form.market.value = "泰国";
  form.platform.value = "TikTok 小店";
  form.audience.value = "养猫人群";
  form.category.value = "宠物用品";
  form.currency.value = "THB";
  priceMinInput.value = "300";
  priceMaxInput.value = "1200";
  syncPriceRange();
  form.preferences.value = "轻小件, 视觉演示强, 合规风险低, 容易找货源";
  if (form.data_source_mode) {
    form.data_source_mode.value = "public";
  }
  applyCategorySample(form.category.value, true);
  unlimitedToggles.forEach((toggle) => {
    toggle.checked = false;
    applyUnlimitedToggle(toggle);
  });
});

clearButton.addEventListener("click", () => {
  form.reset();
  syncPriceRange();
  unlimitedToggles.forEach((toggle) => applyUnlimitedToggle(toggle));
  allCandidates = [];
  candidates = [];
  activeIndex = 0;
  renderResults({ report: "" });
});

copyReportButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(markdownReport.textContent || "");
  statusPill.textContent = "Copied";
  statusPill.className = "status-pill";
});

exportCsvButton.addEventListener("click", () => {
  const rows = [
    ["rank", "product", "score", "confidence", "risk", "primary_link"],
    ...candidates.map((candidate, index) => [
      index + 1,
      candidate.name,
      candidate.total_score,
      candidate.data_confidence?.label || "",
      candidate.risk_assessment?.label || "",
      candidate.primary_link || "",
    ]),
  ];
  const csv = rows.map((row) => row.map(csvCell).join(",")).join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "novelty-product-scout.csv";
  link.click();
  URL.revokeObjectURL(url);
});

function applyCategorySample(category, force = false) {
  const profile = sampleProfileForCategory(category);
  if (force || canReplaceSample(form.seed_keywords.value)) {
    form.seed_keywords.value = profile.seeds;
  }
}

function sampleProfileForCategory(category) {
  const text = String(category || "");
  return Object.values(sampleProfiles).find((profile) => (
    profile.match.some((keyword) => text.includes(keyword))
  )) || sampleProfiles.generic;
}

function canReplaceSample(value) {
  const text = String(value || "").trim();
  if (!text) {
    return true;
  }
  return sampleFingerprints.some((item) => item && text.includes(item));
}

function unlimitedValue(fieldName, value) {
  const toggle = document.querySelector(`.unlimited-toggle[data-target="${fieldName}"]`);
  return toggle?.checked ? "不限" : value;
}

function applyUnlimitedToggle(toggle) {
  const targetName = toggle.dataset.target;
  const input = form.elements[targetName];
  const preset = document.querySelector(`.preset-select[data-fill="${targetName}"]`);
  if (!input) {
    return;
  }
  input.disabled = toggle.checked;
  input.classList.toggle("disabled-field", toggle.checked);
  if (preset) {
    preset.disabled = toggle.checked;
    preset.classList.toggle("disabled-field", toggle.checked);
  }
  if (toggle.checked) {
    input.dataset.previousValue = input.value;
    input.value = "不限";
  } else if (input.value === "不限") {
    input.value = input.dataset.previousValue || "";
  }
}

function localizePresetLists() {
  setDatalistValues("#audienceOptions", audiencePresets);
  setDatalistValues("#categoryOptions", categoryPresets);
}

function populatePresetSelects() {
  populateOnePresetSelect(document.querySelector('[data-fill="audience"]'), datalistValues("#audienceOptions"));
  populateOnePresetSelect(document.querySelector('[data-fill="category"]'), datalistValues("#categoryOptions"));
}

function syncPriceRange() {
  if (!form.price_range) {
    return "";
  }
  const minValue = normalizePriceNumber(priceMinInput?.value) || "0";
  const maxRaw = String(priceMaxInput?.value || "").trim();
  const maxValue = normalizePriceNumber(maxRaw);
  let range = "";
  if (isInfinitePrice(maxRaw)) {
    range = Number(minValue) > 0 ? `${minValue}+` : "";
  } else if (maxValue) {
    range = `${minValue}-${maxValue}`;
  } else {
    range = Number(minValue) > 0 ? `${minValue}+` : "";
  }
  form.price_range.value = range;
  return range;
}

function normalizePriceNumber(value) {
  const match = String(value || "").replaceAll(",", "").match(/\d+(?:\.\d+)?/);
  return match ? match[0] : "";
}

function isInfinitePrice(value) {
  const normalized = String(value || "").trim().toLowerCase();
  return !normalized || ["无限大", "不限", "∞", "infinity", "inf", "unlimited", "no limit", "all"].includes(normalized);
}

function populateOnePresetSelect(select, values, labeler = (value) => value) {
  if (!select) {
    return;
  }
  const firstLabel = select.querySelector("option")?.textContent || "选择...";
  select.innerHTML = `<option value="">${escapeHtml(firstLabel)}</option>` + values.map((value) => (
    `<option value="${escapeAttribute(value)}">${escapeHtml(labeler(value))}</option>`
  )).join("");
}

function setDatalistValues(selector, values) {
  const datalist = document.querySelector(selector);
  if (!datalist) {
    return;
  }
  datalist.innerHTML = values.map((value) => `<option value="${escapeAttribute(value)}">`).join("");
}

function datalistValues(selector) {
  return Array.from(document.querySelectorAll(`${selector} option`))
    .map((option) => option.value)
    .filter(Boolean);
}

function currencyName(currency) {
  return {
    THB: "泰铢",
    CNY: "人民币",
    VND: "越南盾",
    SGD: "新加坡元",
    USD: "美元",
    PHP: "菲律宾比索",
    MYR: "马来西亚林吉特",
  }[currency] || currency;
}

function setRunning(isRunning) {
  runButton.disabled = isRunning;
  runButton.textContent = isRunning ? "正在采集信源..." : "开始选品分析";
  if (isRunning) {
    statusPill.textContent = "Running";
    statusPill.className = "status-pill running";
  }
}

function renderResults(result) {
  emptyState.hidden = candidates.length > 0;
  candidateCount.textContent = candidates.length;
  topScore.textContent = candidates[0] ? candidates[0].total_score : "-";
  activeMode.textContent = modeLabel(new FormData(form).get("ranking_mode"));
  highConfidence.textContent = allCandidates.filter((candidate) => candidate.data_confidence?.label === "高").length;
  markdownReport.textContent = result.report || "";
  if (result.source_status && sourceStatus) {
    sourceStatus.textContent = `${result.source_status.label} | ${result.source_status.region || "-"} | ${result.source_status.date || ""} | ${result.source_status.rows || 0} 条${result.source_status.note ? ` | ${result.source_status.note}` : ""}`;
  }

  ranking.innerHTML = candidates.map((candidate, index) => `
    <div class="product-row ${index === activeIndex ? "active" : ""}" data-index="${index}">
      <span class="rank-badge">${index + 1}</span>
      <a class="product-main-link" href="${escapeAttribute(candidate.primary_link || buildFallbackLink(candidate.name))}" target="_blank" rel="noreferrer">
        <p class="product-name">${escapeHtml(candidate.name)}</p>
        <span class="row-meta">${escapeHtml(candidate.grade)} | 可信度 ${escapeHtml(candidate.data_confidence?.label || "-")} | ${escapeHtml(candidate.ranking_reason || "")}</span>
      </a>
      <span class="score-block">
        <strong>${candidate.total_score}</strong>
        <span class="row-meta">score</span>
      </span>
      <button class="detail-button" data-index="${index}" type="button">查看分析</button>
    </div>
  `).join("");

  ranking.querySelectorAll(".detail-button").forEach((button) => {
    button.addEventListener("click", () => {
      activeIndex = Number(button.dataset.index);
      renderResults({ report: markdownReport.textContent });
    });
  });

  renderDetail(candidates[activeIndex]);
}

function visibleCandidates() {
  return allCandidates;
}

function renderDetail(candidate) {
  if (!candidate) {
    detail.classList.add("hidden");
    detail.innerHTML = "";
    return;
  }
  detail.classList.remove("hidden");
  const risks = candidate.risk_flags.length ? candidate.risk_flags.join(", ") : "未检测到明显高风险词，仍需人工核查合规和侵权。";
  const metrics = candidate.leaderboard_metrics || {};
  const confidence = candidate.data_confidence || {};
  const risk = candidate.risk_assessment || {};
  const density = candidate.competitor_density || {};
  const sourceBreakdown = candidate.free_signal_breakdown || [];
  detail.innerHTML = `
    <h2>${escapeHtml(candidate.name)}</h2>
    <p class="row-meta">${escapeHtml(candidate.grade)} | ${candidate.total_score}/100 | 可信度 ${escapeHtml(confidence.label || "-")} | 风险 ${escapeHtml(risk.label || "-")}</p>
    <div class="detail-tabs">
      <button type="button" class="tab-button active" data-tab="decision">机会判断</button>
      <button type="button" class="tab-button" data-tab="evidence">数据证据</button>
      <button type="button" class="tab-button" data-tab="sourcing">供应链</button>
      <button type="button" class="tab-button" data-tab="content">内容脚本</button>
      <button type="button" class="tab-button" data-tab="risk">风险核查</button>
      <button type="button" class="tab-button" data-tab="plan">测试计划</button>
    </div>
    <div class="metric-grid">
      ${metricChip(metrics.is_estimated ? "销量信号" : "真实销量", metrics.sales_signal)}
      ${metricChip(metrics.is_estimated ? "GMV信号" : "真实GMV", candidate.formatted_gmv_signal || candidate.formatted_gmv || metrics.gmv_signal)}
      ${metricChip("视频信号", metrics.video_signal)}
      ${metricChip("达人信号", metrics.influencer_signal)}
      ${metricChip("直播信号", metrics.live_count || metrics.estimated_live_count)}
      ${metricChip("佣金率", `${metrics.commission_rate || metrics.estimated_commission_rate || 0}%`)}
    </div>
    <div class="score-grid">
      ${scoreChip("新奇度", candidate.scores.novelty)}
      ${scoreChip("需求强度", candidate.scores.demand)}
      ${scoreChip("内容传播", candidate.scores.content_virality)}
      ${scoreChip("竞争可控", candidate.scores.competition_control)}
      ${scoreChip("供应链", candidate.scores.sourcing_feasibility)}
      ${scoreChip("测试可行", candidate.scores.test_feasibility)}
    </div>
    <section class="tab-panel active" data-panel="decision">
      <div class="detail-grid">
        ${infoBlock("适合测试原因", candidate.decision_summary)}
        ${infoBlock("上榜原因", candidate.ranking_reason)}
        ${infoBlock("可信度", `${confidence.label || "-"}：${confidence.reason || ""}`)}
        ${infoBlock("竞品密度", `${density.label || "-"}：${density.reason || ""}`)}
        ${infoBlock("数据说明", metrics.is_estimated ? "销量/GMV为估算信号，不是平台真实销量。" : "结构化榜单/CSV字段。")}
        ${infoBlock("平台类目", candidate.category_name || "-")}
        ${infoBlock("评分/评论", `${candidate.rating || "-"} / ${candidate.review_count || 0}`)}
        ${infoBlock("目标用户", candidate.target_user)}
        ${infoBlock("用户痛点", candidate.pain_point)}
        ${infoBlock("不要做的情况", (candidate.avoid_reasons || []).join("；"))}
      </div>
      <div class="info-block">
        <h3>信源分解</h3>
        <div class="source-breakdown">
          ${sourceBreakdown.map((item) => `
            <div class="source-breakdown-item">
              <span>${escapeHtml(item.label)}</span>
              <strong>${Number(item.score || 0)}</strong>
              <small>${Number(item.count || 0)} 条证据${item.sources?.length ? ` · ${escapeHtml(item.sources.join("、"))}` : ""}</small>
            </div>
          `).join("")}
        </div>
      </div>
    </section>
    <section class="tab-panel" data-panel="evidence">
      <div class="info-block">
        <h3>跳转链接</h3>
        <div class="link-list">
          ${(candidate.destination_links || []).map((item) => `
            <a href="${escapeAttribute(item.url)}" target="_blank" rel="noreferrer">${escapeHtml(item.label)}</a>
          `).join("")}
        </div>
      </div>
      <div class="info-block">
        <h3>证据来源</h3>
        <ul>
          ${candidate.evidence.map((item) => `
            <li>
              <strong>[${escapeHtml(item.type || item.source)}]</strong>
              ${item.link ? `<a href="${escapeAttribute(item.link)}" target="_blank" rel="noreferrer">${escapeHtml(item.title)}</a>` : escapeHtml(item.title)}
              ${item.snippet ? `<br>${escapeHtml(item.snippet)}` : ""}
            </li>
          `).join("")}
        </ul>
      </div>
    </section>
    <section class="tab-panel" data-panel="sourcing">
      <div class="detail-grid">
        ${infoBlock("采购关键词", candidate.sourcing_keywords.join(", "))}
        ${infoBlock("中文货源词", (candidate.multilingual_sourcing_keywords?.chinese || []).join(", "))}
        ${infoBlock("英文扩展词", (candidate.multilingual_sourcing_keywords?.english || []).join(", "))}
      </div>
    </section>
    <section class="tab-panel" data-panel="content">
      <div class="detail-grid">
        ${infoBlock("短视频钩子", candidate.video_hook)}
        ${infoBlock("直播讲法", candidate.livestream_angle)}
      </div>
      <div class="info-block">
        <h3>短视频脚本</h3>
        <ul>
          ${(candidate.video_scripts || []).map((item) => `<li><strong>${escapeHtml(item.type)}</strong>：${escapeHtml(item.script)}</li>`).join("")}
        </ul>
      </div>
    </section>
    <section class="tab-panel" data-panel="risk">
      <div class="detail-grid">
        ${infoBlock("风险等级", `${risk.label || "-"}：${risk.summary || ""}`)}
        ${infoBlock("风险提示", risks)}
      </div>
      <div class="info-block">
        <h3>风险项</h3>
        <ul>
          ${(risk.items || []).length ? risk.items.map((item) => `<li><strong>${escapeHtml(item.severity)}</strong> ${escapeHtml(item.keyword)}：${escapeHtml(item.action)}</li>`).join("") : "<li>未检测到明显高风险词，仍需人工核查。</li>"}
        </ul>
      </div>
      <div class="info-block">
        <h3>可信度核查清单</h3>
        <ol>
          ${(candidate.verification_checklist || []).map((item) => `<li><strong>${escapeHtml(item.title)}</strong> [${escapeHtml(item.status)}] ${escapeHtml(item.action)}</li>`).join("")}
        </ol>
      </div>
    </section>
    <section class="tab-panel" data-panel="plan">
      <div class="info-block">
        <h3>首轮验证计划</h3>
        <ol>
          ${candidate.validation_plan.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ol>
      </div>
      <button type="button" class="secondary-button rerun-button" data-product="${escapeAttribute(candidate.name)}">重新分析这个商品</button>
    </section>
  `;

  detail.querySelectorAll(".tab-button").forEach((button) => {
    button.addEventListener("click", () => {
      detail.querySelectorAll(".tab-button").forEach((item) => item.classList.remove("active"));
      detail.querySelectorAll(".tab-panel").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      detail.querySelector(`[data-panel="${button.dataset.tab}"]`)?.classList.add("active");
    });
  });

  detail.querySelector(".rerun-button")?.addEventListener("click", (event) => {
    form.seed_keywords.value = event.currentTarget.dataset.product || candidate.name;
    form.dispatchEvent(new Event("submit"));
  });
}

async function loadSourceStatus() {
  if (!sourceStatus) {
    return;
  }
  try {
    const response = await fetch("/api/source-status");
    const data = await response.json();
    sourceStatus.textContent = data.label || "数据源状态未知";
    sourceStatus.classList.add("source-ok");
    sourceStatus.classList.remove("source-missing");
  } catch (error) {
    sourceStatus.textContent = "无法读取数据源状态";
    sourceStatus.classList.add("source-missing");
  }
}

function scoreChip(label, value) {
  const safeValue = Number(value || 0);
  const percent = Math.max(0, Math.min(100, safeValue * 4));
  return `
    <div class="score-chip">
      <span>${label}</span>
      <strong>${safeValue}</strong>
      <i style="width:${percent}%"></i>
    </div>
  `;
}

function metricChip(label, value) {
  return `<div class="metric-chip"><span>${label}</span><strong>${escapeHtml(value ?? 0)}</strong></div>`;
}

function infoBlock(title, body) {
  return `<div class="info-block"><h3>${escapeHtml(title)}</h3><p>${escapeHtml(body || "")}</p></div>`;
}

function modeLabel(mode) {
  return {
    hot_sales: "热销",
    hot_push: "热推",
    content_viral: "内容",
    category_opportunity: "类目",
    low_risk: "低风险",
  }[mode] || "热销";
}

function buildFallbackLink(name) {
  return `https://www.google.com/search?q=${encodeURIComponent(name || "")}`;
}

function csvCell(value) {
  const text = String(value ?? "");
  return `"${text.replaceAll('"', '""')}"`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}
