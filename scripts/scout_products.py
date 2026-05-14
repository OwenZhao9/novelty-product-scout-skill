#!/usr/bin/env python3
import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SEARCH_ENDPOINT = "https://duckduckgo.com/html/"

MARKET_REGION_ALIASES = {
    "泰国": "TH",
    "thailand": "TH",
    "th": "TH",
    "越南": "VN",
    "vietnam": "VN",
    "vn": "VN",
    "菲律宾": "PH",
    "philippines": "PH",
    "ph": "PH",
    "马来西亚": "MY",
    "malaysia": "MY",
    "my": "MY",
    "新加坡": "SG",
    "singapore": "SG",
    "sg": "SG",
    "印尼": "ID",
    "印度尼西亚": "ID",
    "indonesia": "ID",
    "id": "ID",
    "美国": "US",
    "us": "US",
    "usa": "US",
}

STOPWORDS = {
    "best", "top", "new", "viral", "trend", "trending", "product", "products",
    "shop", "shopping", "buy", "amazon", "aliexpress", "tiktok", "shopify",
    "for", "with", "and", "the", "this", "that", "ideas", "idea", "finds",
    "review", "reviews", "price", "deal", "deals", "online", "store"
}

GENERIC_CANDIDATES = {
    "ad", "ads", "on", "pets", "pet", "cat", "cats", "dog", "dogs", "supplies",
    "pet supplies", "content", "video", "generator", "content video generator",
    "affiliates", "influencers", "ideas", "shopping", "products", "product",
    "amazon", "aliexpress", "tiktok", "shopify"
}

VISUAL_WORDS = {
    "before", "after", "demo", "transform", "magic", "automatic", "portable",
    "foldable", "mini", "clean", "organizer", "light", "led", "self", "smart",
    "remover", "tool", "hidden", "instant", "visual", "satisfying"
}

DEMAND_WORDS = {
    "pain", "problem", "solution", "easy", "save", "clean", "protect", "fix",
    "comfort", "organize", "reduce", "remove", "fast", "daily", "home", "travel",
    "pet", "kitchen", "office", "baby", "car"
}

RISK_WORDS = {
    "medical", "medicine", "health claim", "laser", "battery", "knife", "weapon",
    "children", "baby", "food", "supplement", "cosmetic", "copyright", "disney",
    "pokemon", "lego", "nike", "apple", "branded", "fragile", "glass", "liquid",
    "drug", "weight loss", "skin whitening", "teeth whitening", "pesticide",
    "flammable", "magnet", "adult", "toy gun", "explosive", "patent"
}

RISK_SEVERITY = {
    "medical": "critical",
    "medicine": "critical",
    "health claim": "critical",
    "supplement": "critical",
    "food": "high",
    "cosmetic": "high",
    "children": "high",
    "baby": "high",
    "battery": "high",
    "laser": "high",
    "knife": "high",
    "weapon": "critical",
    "drug": "critical",
    "explosive": "critical",
    "weight loss": "critical",
    "skin whitening": "high",
    "teeth whitening": "high",
    "pesticide": "critical",
    "flammable": "high",
    "magnet": "medium",
    "adult": "high",
    "toy gun": "high",
    "copyright": "high",
    "patent": "high",
    "disney": "high",
    "pokemon": "high",
    "lego": "high",
    "nike": "high",
    "apple": "high",
    "branded": "high",
    "fragile": "medium",
    "glass": "medium",
    "liquid": "medium",
}

SOURCE_LABELS = {
    "tiktok": "TikTok / TikTok Shop",
    "tiktok_signal": "TikTok 搜索",
    "tiktok_shop_signal": "TikTok Shop 搜索",
    "tiktok_creative": "TikTok Creative Center",
    "tiktok_creative_signal": "TikTok Creative Center",
    "seed_tiktok_creative": "TikTok Creative Center",
    "amazon": "Amazon",
    "amazon_signal": "Amazon",
    "amazon_movers": "Amazon Movers & Shakers",
    "amazon_movers_signal": "Amazon Movers & Shakers",
    "shopee": "Shopee",
    "shopee_signal": "Shopee",
    "lazada": "Lazada",
    "lazada_signal": "Lazada",
    "aliexpress": "AliExpress",
    "aliexpress_signal": "AliExpress",
    "1688": "1688 / Alibaba",
    "sourcing_signal": "1688 / Alibaba",
    "alibaba": "Alibaba",
    "alibaba_signal": "Alibaba",
    "seed_alibaba": "Alibaba",
    "google_trends": "Google Trends",
    "trend_signal": "Google Trends",
    "seed_google_trends": "Google Trends",
    "pinterest_trends": "Pinterest Trends",
    "pinterest_trend_signal": "Pinterest Trends",
    "seed_pinterest_trends": "Pinterest Trends",
    "meta_ads": "Meta Ad Library",
    "meta_ads_signal": "Meta Ad Library",
    "seed_meta_ads": "Meta Ad Library",
    "xiaohongshu": "Xiaohongshu",
    "xiaohongshu_signal": "Xiaohongshu",
    "douyin": "Douyin",
    "douyin_signal": "Douyin",
    "reddit": "Reddit",
    "reddit_signal": "Reddit",
    "seed_reddit": "Reddit",
    "quora": "Quora",
    "quora_signal": "Quora",
    "seed_quora": "Quora",
    "pantip": "Pantip",
    "pantip_signal": "Pantip",
    "seed_pantip": "Pantip",
    "youtube": "YouTube",
    "youtube_signal": "YouTube",
    "seed_youtube": "YouTube",
    "problem": "Problem-solution search",
    "problem_signal": "Problem-solution search",
    "creator": "Creator / affiliate signal",
    "creator_signal": "Creator / affiliate signal",
    "seed_creator": "Creator / affiliate signal",
    "seed_tiktok": "TikTok 搜索",
    "seed_sourcing": "1688 / AliExpress",
    "content_signal": "Short video idea search",
}

FREE_SOURCE_GROUPS = {
    "trend": {"google_trends", "pinterest_trends", "trend_signal", "pinterest_trend_signal", "seed_google_trends", "seed_pinterest_trends"},
    "content": {"tiktok", "tiktok_creative", "creator", "youtube", "douyin", "xiaohongshu", "tiktok_signal", "tiktok_shop_signal", "tiktok_creative_signal", "creator_signal", "youtube_signal", "douyin_signal", "xiaohongshu_signal", "content_signal", "seed_tiktok", "seed_creator", "seed_tiktok_creative", "seed_youtube"},
    "ads": {"meta_ads", "meta_ads_signal", "seed_meta_ads"},
    "marketplace": {"amazon", "amazon_movers", "shopee", "lazada", "aliexpress", "amazon_signal", "amazon_movers_signal", "shopee_signal", "lazada_signal", "aliexpress_signal"},
    "sourcing": {"1688", "alibaba", "sourcing_signal", "alibaba_signal", "seed_sourcing", "seed_alibaba"},
    "community": {"reddit", "quora", "pantip", "problem", "reddit_signal", "quora_signal", "pantip_signal", "problem_signal", "seed_reddit", "seed_quora", "seed_pantip"},
}

FREE_SOURCE_DEFAULTS = [
    "tiktok",
    "tiktok_creative",
    "google_trends",
    "meta_ads",
    "pinterest_trends",
    "amazon",
    "amazon_movers",
    "shopee",
    "lazada",
    "aliexpress",
    "1688",
    "alibaba",
    "reddit",
    "quora",
    "pantip",
    "youtube",
    "xiaohongshu",
    "problem",
    "creator",
]

CATEGORY_GROUPS = {
    "pet": {"宠物", "猫", "狗", "pet", "cat", "dog", "grooming"},
    "jewelry": {"饰品", "珠宝", "首饰", "项链", "戒指", "耳环", "手链", "发饰", "jewelry", "necklace", "ring", "earring", "bracelet"},
    "beauty": {"美妆", "护肤", "美甲", "个护", "美发", "beauty", "makeup", "skincare", "nail", "hair"},
    "electronics": {"手机", "电子", "充电", "电脑", "相机", "直播", "phone", "electronic", "charging", "camera", "livestream"},
    "home": {"家居", "收纳", "清洁", "厨房", "浴室", "灯", "home", "storage", "cleaning", "kitchen", "bathroom"},
}

ENGLISH_KEYWORD_MAP = {
    "泰国": "Thailand",
    "越南": "Vietnam",
    "菲律宾": "Philippines",
    "马来西亚": "Malaysia",
    "新加坡": "Singapore",
    "印尼": "Indonesia",
    "印度尼西亚": "Indonesia",
    "美国": "United States",
    "英国": "United Kingdom",
    "欧盟": "European Union",
    "日本": "Japan",
    "东南亚": "Southeast Asia",
    "TikTok 小店": "TikTok Shop",
    "TikTok小店": "TikTok Shop",
    "抖音": "Douyin",
    "小红书": "Xiaohongshu",
    "亚马逊": "Amazon",
    "速卖通": "AliExpress",
    "独立站": "DTC store",
    "虾皮": "Shopee",
    "不限": "",
    "全部": "",
    "全品类": "",
    "养猫人群": "cat owners",
    "养狗人群": "dog owners",
    "宠物主人": "pet owners",
    "小户型养宠人群": "small apartment pet owners",
    "新手铲屎官": "new pet owners",
    "年轻白领": "young professionals",
    "办公室人群": "office workers",
    "内容创作者": "content creators",
    "直播卖家": "livestream sellers",
    "短视频达人": "short video creators",
    "家庭做饭人群": "home cooks",
    "收纳爱好者": "home organizers",
    "美妆用户": "beauty users",
    "旅行人群": "travelers",
    "礼物购买者": "gift buyers",
    "新手父母": "new parents",
    "孕妇": "pregnant women",
    "新手妈妈": "new moms",
    "幼儿父母": "parents of toddlers",
    "学生家长": "parents of school kids",
    "老人护理人群": "elderly caregivers",
    "银发人群": "seniors",
    "大学生": "college students",
    "高中生": "high school students",
    "远程办公人群": "remote workers",
    "教师": "teachers",
    "护士": "nurses",
    "小商家": "small business owners",
    "游戏玩家": "gamers",
    "手机摄影用户": "phone photographers",
    "烘焙爱好者": "bakers",
    "咖啡爱好者": "coffee lovers",
    "备餐人群": "meal prep users",
    "清洁爱好者": "cleaning enthusiasts",
    "租房人群": "renters",
    "小户型家庭": "small apartment residents",
    "养植物人群": "plant lovers",
    "护肤用户": "skincare users",
    "化妆新手": "makeup beginners",
    "护发用户": "hair care users",
    "美甲用户": "nail art users",
    "健身新手": "fitness beginners",
    "瑜伽人群": "yoga users",
    "居家健身人群": "home workout users",
    "跑步人群": "runners",
    "骑行人群": "cyclists",
    "露营人群": "outdoor campers",
    "汽车用户": "car owners",
    "摩托车用户": "motorcycle riders",
    "网约车司机": "ride-share drivers",
    "背包客": "backpackers",
    "商务差旅人群": "business travelers",
    "派对主办者": "party hosts",
    "手作爱好者": "DIY users",
    "园艺人群": "gardeners",
    "穆斯林女性": "Muslim women",
    "预算型消费者": "budget shoppers",
    "冲动消费人群": "impulse buyers",
    "宠物用品": "pet supplies",
    "宠物梳毛工具": "pet grooming tools",
    "宠物玩具": "pet toys",
    "宠物喂食用品": "pet feeding supplies",
    "宠物清洁用品": "pet cleaning supplies",
    "宠物出行配件": "pet travel accessories",
    "宠物窝垫家具": "pet beds and furniture",
    "猫用品": "cat supplies",
    "狗用品": "dog supplies",
    "家居收纳": "home organization",
    "收纳盒/收纳架": "storage organizers",
    "衣柜收纳": "closet organizers",
    "鞋类收纳": "shoe storage",
    "洗衣配件": "laundry accessories",
    "清洁工具": "cleaning tools",
    "地面清洁工具": "floor cleaning tools",
    "厨房清洁工具": "kitchen cleaning tools",
    "浴室用品": "bathroom accessories",
    "家居装饰": "home decor",
    "墙面装饰": "wall decor",
    "节日装饰": "seasonal decor",
    "灯具照明": "lighting",
    "夜灯": "night lights",
    "智能家居小工具": "smart home gadgets",
    "厨房小工具": "kitchen gadgets",
    "厨房收纳": "kitchen storage",
    "烹饪工具": "cooking tools",
    "切削削皮工具": "cutting and peeling tools",
    "杯壶水具": "drinkware",
    "咖啡配件": "coffee accessories",
    "茶饮配件": "tea accessories",
    "烘焙工具": "baking tools",
    "食品保鲜收纳": "food storage",
    "美妆工具": "beauty tools",
    "个护工具": "personal care tools",
    "护肤仪器": "skincare devices",
    "洁面工具": "facial cleansing tools",
    "美发工具": "hair styling tools",
    "化妆配件": "makeup accessories",
    "按摩工具": "massage tools",
    "沐浴身体护理": "bath and body accessories",
    "手机配件": "phone accessories",
    "电子配件": "electronics accessories",
    "充电配件": "charging accessories",
    "线缆收纳": "cable organizers",
    "平板配件": "tablet accessories",
    "电脑配件": "computer accessories",
    "桌面设备": "desk setup gadgets",
    "键鼠配件": "keyboard and mouse accessories",
    "直播配件": "livestream accessories",
    "音频配件": "audio accessories",
    "可穿戴配件": "wearable accessories",
    "汽车配件": "car accessories",
    "摩托车配件": "motorcycle accessories",
    "汽车清洁工具": "car cleaning tools",
    "车载收纳": "car storage organizers",
    "车载手机支架": "car phone mounts",
    "汽车内饰": "car interior accessories",
    "户外装备": "outdoor gear",
    "露营装备": "camping gear",
    "旅行配件": "travel accessories",
    "行李收纳": "luggage organizers",
    "便携旅行小工具": "portable travel gadgets",
    "运动配件": "sports accessories",
    "健身配件": "fitness accessories",
    "瑜伽配件": "yoga accessories",
    "跑步配件": "running accessories",
    "居家健身器材": "home workout equipment",
    "母婴用品": "baby products",
    "母婴配件": "mom and baby accessories",
    "婴儿喂养用品": "baby feeding accessories",
    "婴儿安全用品": "baby safety products",
    "婴儿车配件": "stroller accessories",
    "办公小物": "office gadgets",
    "学习用品": "school supplies",
    "文具": "stationery",
    "桌面配件": "desk accessories",
    "学习工具": "study tools",
    "玩具兴趣": "toys and hobbies",
    "益智玩具": "educational toys",
    "解压玩具": "fidget toys",
    "收藏品": "collectibles",
    "派对用品": "party supplies",
    "礼品包装": "gift packaging",
    "DIY 工具": "DIY tools",
    "手动工具": "hand tools",
    "家装修理小工具": "home repair gadgets",
    "园艺工具": "garden tools",
    "植物护理工具": "plant care tools",
    "时尚配件": "fashion accessories",
    "饰品配件": "jewelry accessories",
    "饰品": "jewelry accessories",
    "珠宝": "jewelry",
    "发饰": "hair accessories",
    "包袋行李": "bags and luggage",
    "钱包卡包": "wallets and card holders",
    "旅行包": "travel bags",
    "鞋类配件": "shoe accessories",
    "穆斯林时尚配件": "Muslim fashion accessories",
    "健康护理配件": "health and wellness accessories",
    "睡眠配件": "sleep accessories",
    "体态矫正配件": "posture accessories",
    "居家安全用品": "home safety products",
    "节日季节产品": "festival and seasonal products",
    "环保产品": "eco friendly products",
    "数码产品配件": "digital product accessories",
    "猫咪梳毛": "cat grooming brush",
    "宠物除毛": "pet hair remover",
    "猫窗床": "cat window hammock",
    "互动猫玩具": "interactive cat toy",
    "猫咪自助蹭毛刷": "self-grooming cat brush",
    "猫窗吊床": "cat window hammock",
    "宠物除毛手套": "pet grooming glove",
    "折叠猫隧道窝": "foldable cat tunnel bed",
    "旅行首饰收纳": "travel jewelry organizer",
    "防缠绕项链": "anti-tangle necklace organizer",
    "磁吸耳环": "magnetic earring holder",
    "可调节戒指": "adjustable ring sizer",
    "发饰收纳": "hair accessory organizer",
    "旅行首饰收纳包": "travel jewelry organizer case",
    "防缠绕项链收纳盒": "anti-tangle necklace organizer box",
    "磁吸耳环展示架": "magnetic earring display stand",
    "可调节戒指测量器": "adjustable ring sizer",
    "美妆收纳": "makeup organizer",
    "美甲工具": "nail art tools",
    "化妆刷清洁": "makeup brush cleaner",
    "护肤小工具": "skincare tool",
    "便携补妆": "portable makeup touch-up mirror",
    "化妆刷快速清洁垫": "makeup brush cleaning mat",
    "便携补妆镜灯": "portable lighted makeup mirror",
    "美甲磁吸练习架": "magnetic nail practice stand",
    "护肤冰球按摩器": "ice globe facial massager",
    "手机支架": "phone stand",
    "磁吸充电线": "magnetic charging cable",
    "桌面线缆收纳": "desk cable organizer",
    "直播补光灯": "livestream ring light",
    "相机配件": "camera accessories",
    "折叠磁吸手机支架": "foldable magnetic phone stand",
    "桌面线缆收纳夹": "desk cable clips",
    "直播补光手机夹": "phone clip ring light",
    "迷你键盘清洁刷": "mini keyboard cleaning brush",
    "浴室清洁": "bathroom cleaning tool",
    "桌面收纳": "desk organizer",
    "除尘工具": "dust cleaning tool",
    "氛围灯": "ambient light",
    "免打孔旋转收纳架": "no-drill rotating storage rack",
    "缝隙除尘清洁刷": "gap dust cleaning brush",
    "水槽沥水收纳篮": "sink drain storage basket",
    "感应夜灯贴片": "motion sensor night light",
    "新奇特小工具": "novelty gadget",
    "视觉演示产品": "visual demo product",
    "轻小件好物": "lightweight small product",
    "礼物型产品": "giftable product",
    "便携收纳小工具": "portable organizer gadget",
    "创意礼物小物": "creative gift gadget",
}


CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def has_cjk(value):
    return bool(CJK_RE.search(str(value or "")))


def english_keyword(value, profile=None, fallback="novelty product"):
    text = str(value or "").strip()
    if not text:
        return ""
    if not has_cjk(text):
        return normalize_spaces(text)
    if text in ENGLISH_KEYWORD_MAP:
        return normalize_spaces(ENGLISH_KEYWORD_MAP[text])

    converted = text
    for zh, en in sorted(ENGLISH_KEYWORD_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        if zh:
            converted = converted.replace(zh, f" {en} ")
    converted = re.sub(r"[\u4e00-\u9fff]+", " ", converted)
    converted = re.sub(r"[,，/|、]+", " ", converted)
    converted = normalize_spaces(converted)
    if converted:
        return converted

    category = str((profile or {}).get("category") or "").strip()
    if category and category != text:
        category_keyword = english_keyword(category, None, "")
        if category_keyword:
            return normalize_spaces(f"{category_keyword} product")
    return fallback


def normalize_spaces(value):
    return re.sub(r"\s+", " ", str(value or "")).strip(" -_")


@dataclass
class Signal:
    product: str
    source: str
    title: str = ""
    snippet: str = ""
    link: str = ""
    price: str = ""
    mentions: int = 0
    notes: str = ""
    sales: int = 0
    gmv: float = 0
    video_count: int = 0
    influencer_count: int = 0
    live_count: int = 0
    commission_rate: float = 0
    product_id: str = ""
    region: str = ""
    image_url: str = ""
    product_url: str = ""
    seller_id: str = ""
    rating: float = 0
    review_count: int = 0
    category_id: str = ""
    category_l2_id: str = ""
    category_l3_id: str = ""
    category_name: str = ""
    rank_position: int = 0


@dataclass
class Candidate:
    name: str
    signals: list[Signal] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)
    risk_flags: list[str] = field(default_factory=list)
    leaderboard_metrics: dict[str, Any] = field(default_factory=dict)

    @property
    def evidence_text(self):
        return " ".join(
            [self.name] + [s.title for s in self.signals] + [s.snippet for s in self.signals] + [s.notes for s in self.signals]
        ).lower()

    @property
    def sources(self):
        return sorted({s.source for s in self.signals if s.source})

    @property
    def total_score(self):
        base = sum(self.scores.values())
        penalty = min(len(self.risk_flags) * 8, 35)
        return max(base - penalty, 0)

    @property
    def grade(self):
        score = self.total_score
        if score >= 78:
            return "A - Worth testing now"
        if score >= 62:
            return "B - Needs manual validation"
        if score >= 45:
            return "C - Watchlist"
        return "D - Skip for now"


def main():
    parser = argparse.ArgumentParser(description="Scout novelty e-commerce product opportunities.")
    parser.add_argument("--market", help="Market profile JSON file.")
    parser.add_argument("--signals", help="Optional manual CSV signals.")
    parser.add_argument("--output", default="output/report.md", help="Output report path.")
    parser.add_argument("--no-web", action="store_true", help="Skip automatic web collection and use CSV/seed data only.")
    parser.add_argument("--limit", type=int, default=5, help="Search results per query.")
    args = parser.parse_args()

    profile = load_or_prompt_profile(args.market)
    result = run_scout(
        profile=profile,
        signals_path=args.signals,
        output_path=args.output,
        no_web=args.no_web,
        limit=args.limit,
    )

    print(f"Generated report: {result['output_path']}")
    print(f"Candidates found: {len(result['candidates'])}")
    print("Top 5:")
    for candidate in result["candidates"][:5]:
        print(f"- {candidate['name']}: {candidate['total_score']} ({candidate['grade']})")


def run_scout(profile, signals_path=None, signals_csv_text=None, output_path="output/report.md", no_web=False, limit=5):
    signals = []
    if signals_path:
        signals.extend(load_csv_signals(signals_path))
    if signals_csv_text:
        signals.extend(load_csv_signals_text(signals_csv_text))
    seed_signals = seed_keyword_signals(profile)
    signals.extend(seed_signals)
    signals.extend(build_direct_free_source_signals(profile))
    if not no_web:
        signals.extend(collect_web_signals(profile, limit))
    if not signals:
        raise SourceDataError("没有采集到公开线索。请增加种子关键词或放宽类目。")
    has_metrics = any(has_real_metric(signal) for signal in signals)
    source_meta = {
        "source": "public",
        "label": "信源采集",
        "rows": len(signals),
        "selected_sources": [source_label(item) for item in profile.get("data_sources", [])],
        "note": "销量/GMV为机会评分估算，不是平台真实销量。" if not has_metrics else "包含用户CSV结构化字段和公开线索。",
    }

    signals = filter_obviously_irrelevant_signals(signals, profile)
    candidates = build_candidates(signals)
    score_candidates(candidates, profile)
    filtered = apply_filters(candidates.values(), profile)
    ranked = rank_candidates(filtered, profile)

    report = build_report(profile, ranked)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return {
        "profile": profile,
        "source_status": source_meta,
        "report": report,
        "output_path": str(output_path),
        "candidates": [candidate_to_dict(candidate, profile) for candidate in ranked],
    }


def load_or_prompt_profile(path):
    if path:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    print("Novelty Product Scout beginner mode")
    print("Press Enter to use the default in brackets.")
    profile = {
        "market": prompt("Target market", "US"),
        "platform": prompt("Target platform", "TikTok Shop"),
        "ranking_mode": prompt("Ranking mode", "hot_sales"),
        "cycle": prompt("Cycle", "week"),
        "audience": prompt("Target audience", "cat owners"),
        "category": prompt("Category", "pet supplies"),
        "price_range": prompt("Price range", "300-1200"),
        "currency": prompt("Currency", "THB"),
    }
    preferences = prompt("Preferences, comma separated", "lightweight, visual demo, low compliance risk")
    seed_keywords = prompt("Seed keywords, comma separated", "cat grooming, cat hair remover, cat window bed")
    profile["preferences"] = [item.strip() for item in preferences.split(",") if item.strip()]
    profile["seed_keywords"] = [item.strip() for item in seed_keywords.split(",") if item.strip()]
    return profile


def prompt(label, default):
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def load_csv_signals(path):
    signals = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return parse_csv_signal_rows(csv.DictReader(handle))


def load_csv_signals_text(csv_text):
    rows = csv.DictReader(csv_text.splitlines())
    return parse_csv_signal_rows(rows)


def parse_csv_signal_rows(rows):
    signals = []
    for row in rows:
        original_product = (row.get("product") or row.get("name") or "").strip()
        product = english_keyword(original_product)
        if not product:
            continue
        signals.append(Signal(
            product=product,
            source=(row.get("source") or "manual").strip(),
            title=english_keyword(row.get("title") or original_product or product),
            snippet=(row.get("notes") or "").strip(),
            link=(row.get("link") or row.get("url") or "").strip(),
            price=(row.get("price") or "").strip(),
            mentions=parse_int(row.get("mentions")),
            notes=(row.get("notes") or "").strip(),
            sales=parse_int(row.get("sales") or row.get("sale_count") or row.get("totalSaleCnt")),
            gmv=parse_float(row.get("gmv") or row.get("totalSaleGmvAmt")),
            video_count=parse_int(row.get("video_count") or row.get("videos") or row.get("totalVideoCnt")),
            influencer_count=parse_int(row.get("influencer_count") or row.get("influencers") or row.get("totalIflCnt")),
            live_count=parse_int(row.get("live_count") or row.get("lives") or row.get("totalLiveCnt")),
            commission_rate=parse_float(row.get("commission_rate") or row.get("commission") or row.get("productCommissionRate")),
            product_id=(row.get("product_id") or "").strip(),
            region=(row.get("region") or "").strip(),
            image_url=(row.get("image_url") or row.get("cover_url") or "").strip(),
            product_url=(row.get("product_url") or row.get("link") or row.get("url") or "").strip(),
            seller_id=(row.get("seller_id") or "").strip(),
            rating=parse_float(row.get("rating") or row.get("product_rating")),
            review_count=parse_int(row.get("review_count")),
            category_id=(row.get("category_id") or "").strip(),
            category_l2_id=(row.get("category_l2_id") or "").strip(),
            category_l3_id=(row.get("category_l3_id") or "").strip(),
            category_name=(row.get("category_name") or "").strip(),
        ))
    return signals


def parse_int(value):
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def parse_float(value):
    if not value:
        return 0
    cleaned = re.sub(r"[^0-9.]+", "", str(value))
    if not cleaned:
        return 0
    try:
        return float(cleaned)
    except ValueError:
        return 0


class SourceDataError(RuntimeError):
    pass


def public_source_status(profile=None):
    return {
        "source": "public",
        "configured": True,
        "label": "信源已启用：趋势、内容广告、竞品、供应链、社区痛点",
    }


def normalize_region(value):
    raw = str(value or "TH").strip()
    return MARKET_REGION_ALIASES.get(raw, MARKET_REGION_ALIASES.get(raw.lower(), raw.upper()[:2] or "TH"))


def has_real_metric(signal):
    return any([signal.sales, signal.gmv, signal.video_count, signal.influencer_count, signal.live_count])


def seed_keyword_signals(profile):
    signals = []
    for keyword in profile.get("seed_keywords", []):
        english = english_keyword(keyword, profile)
        if not english:
            continue
        signals.append(Signal(
            product=english,
            source="seed",
            title=english,
            snippet=f"Seed keyword for {english_keyword(profile.get('audience', ''), profile)} in {english_keyword(profile.get('category', ''), profile)}.",
        ))
    return signals


def build_direct_free_source_signals(profile):
    data_sources = profile.get("data_sources") or FREE_SOURCE_DEFAULTS
    keywords = profile.get("seed_keywords") or []
    if not keywords:
        keywords = [profile.get("category") or "新奇特产品"]
    signals = []
    for keyword in keywords[:5]:
        keyword = str(keyword or "").strip()
        if not keyword:
            continue
        english = english_keyword(keyword, profile)
        if not english:
            continue
        for source in data_sources:
            link = direct_source_link(source, english, profile)
            if not link:
                continue
            signals.append(Signal(
                product=english,
                source=source,
                title=f"{english} - {source_label(source)} validation entry",
                snippet=f"Free source validation entry: check {english} on {source_label(source)} for trend, content, competitor, sourcing, or community signals.",
                link=link,
            ))
    return signals


def direct_source_link(source, keyword, profile):
    encoded = urllib.parse.quote(str(keyword or ""))
    market = urllib.parse.quote(english_keyword(profile.get("market") or ""))
    links = {
        "tiktok": f"https://www.tiktok.com/search?q={encoded}",
        "tiktok_creative": f"https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en?search={encoded}",
        "google_trends": f"https://trends.google.com/trends/explore?q={encoded}&geo={normalize_region(profile.get('market'))}",
        "meta_ads": f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={encoded}&search_type=keyword_unordered",
        "pinterest_trends": f"https://www.pinterest.com/search/pins/?q={encoded}",
        "amazon": f"https://www.amazon.com/s?k={encoded}",
        "amazon_movers": "https://www.amazon.com/gp/movers-and-shakers",
        "shopee": f"https://shopee.co.th/search?keyword={encoded}",
        "lazada": f"https://www.lazada.co.th/catalog/?q={encoded}",
        "aliexpress": f"https://www.aliexpress.com/wholesale?SearchText={encoded}",
        "1688": f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded}",
        "alibaba": f"https://www.alibaba.com/trade/search?SearchText={encoded}",
        "reddit": f"https://www.reddit.com/search/?q={encoded}%20{market}",
        "quora": f"https://www.quora.com/search?q={encoded}",
        "pantip": f"https://pantip.com/search?q={encoded}",
        "youtube": f"https://www.youtube.com/results?search_query={encoded}",
        "xiaohongshu": f"https://www.xiaohongshu.com/search_result?keyword={encoded}",
        "douyin": f"https://www.douyin.com/search/{encoded}",
        "problem": f"https://www.google.com/search?q={encoded}%20problem%20solution",
        "creator": f"https://www.google.com/search?q={encoded}%20creator%20affiliate%20tiktok%20shop",
    }
    return links.get(source, "")


def filter_obviously_irrelevant_signals(signals, profile):
    target_group = category_group(profile.get("category", ""))
    if not target_group:
        return signals
    target_words = CATEGORY_GROUPS[target_group]
    other_groups = {
        group: words for group, words in CATEGORY_GROUPS.items()
        if group != target_group
    }
    filtered = []
    for signal in signals:
        parts = [signal.product, signal.title, signal.notes]
        if signal.source != "seed":
            parts.append(signal.snippet)
        text = " ".join(parts).lower()
        has_target = contains_any(text, target_words)
        has_conflicting_group = any(
            contains_any(text, words) for words in other_groups.values()
        )
        if has_conflicting_group and not has_target:
            continue
        filtered.append(signal)
    return filtered


def category_group(category):
    text = str(category or "").lower()
    for group, words in CATEGORY_GROUPS.items():
        if contains_any(text, words):
            return group
    return ""


def contains_any(text, words):
    return any(str(word).lower() in text for word in words)


def collect_web_signals(profile, limit):
    queries = build_queries(profile)
    signals = []
    for source, query in queries:
        try:
            results = search_duckduckgo(query, limit=limit)
        except Exception as exc:
            print(f"Warning: failed to collect {source}: {exc}", file=sys.stderr)
            continue
        for result in results:
            product = infer_product_name(result["title"], result["snippet"], profile)
            if not product:
                continue
            signals.append(Signal(
                product=product,
                source=source,
                title=result["title"],
                snippet=result["snippet"],
                link=result["link"],
            ))
        time.sleep(0.4)
    return signals


def build_queries(profile):
    market = english_keyword(profile.get("market", ""))
    platform = english_keyword(profile.get("platform", ""))
    audience = english_keyword(profile.get("audience", ""), profile)
    category = english_keyword(profile.get("category", ""), profile)
    price = profile.get("price_range", "")
    seeds = [english_keyword(seed, profile) for seed in profile.get("seed_keywords", [])]
    seeds = [seed for seed in seeds if seed]
    data_sources = set(profile.get("data_sources") or FREE_SOURCE_DEFAULTS)

    base = f"{audience} {category}".strip() or "novelty product"
    queries = []
    if "tiktok" in data_sources:
        queries.append(("tiktok_signal", f"{base} viral product {platform} {market} sales best seller"))
        queries.append(("tiktok_shop_signal", f"{category} tiktok shop best sellers {market} category trend"))
    if "tiktok_creative" in data_sources:
        queries.append(("tiktok_creative_signal", f"site:ads.tiktok.com/business/creativecenter {base} top ads product trend keyword insights"))
    if "creator" in data_sources:
        queries.append(("creator_signal", f"{base} {platform} influencer affiliate commission product"))
    if "youtube" in data_sources:
        queries.append(("youtube_signal", f"site:youtube.com {base} review shorts unboxing demo"))
    if "xiaohongshu" in data_sources:
        queries.append(("xiaohongshu_signal", f"{base} Xiaohongshu viral product recommendation"))
    if "douyin" in data_sources:
        queries.append(("douyin_signal", f"{base} Douyin viral product short video ecommerce"))
    if "amazon" in data_sources:
        queries.append(("amazon_signal", f"site:amazon.com {base} novelty product {price} reviews"))
    if "amazon_movers" in data_sources:
        queries.append(("amazon_movers_signal", f"site:amazon.com/gp/movers-and-shakers {base}"))
    if "shopee" in data_sources:
        queries.append(("shopee_signal", f"site:shopee.co.th {base} {market} sold reviews"))
    if "lazada" in data_sources:
        queries.append(("lazada_signal", f"site:lazada.co.th {base} {market} reviews"))
    if "aliexpress" in data_sources:
        queries.append(("aliexpress_signal", f"site:aliexpress.com {base} wholesale novelty product"))
    if "1688" in data_sources:
        queries.append(("sourcing_signal", f"{base} wholesale 1688 Alibaba novelty product"))
    if "alibaba" in data_sources:
        queries.append(("alibaba_signal", f"site:alibaba.com {base} wholesale supplier factory"))
    if "google_trends" in data_sources:
        queries.append(("trend_signal", f"site:trends.google.com/trends {base} rising breakout trend {market}"))
    if "pinterest_trends" in data_sources:
        queries.append(("pinterest_trend_signal", f"site:pinterest.com/trends {base} trend ideas"))
    if "meta_ads" in data_sources:
        queries.append(("meta_ads_signal", f"site:facebook.com/ads/library {base} ecommerce ads"))
    if "reddit" in data_sources:
        queries.append(("reddit_signal", f"site:reddit.com {audience} {category} problem recommendation"))
    if "quora" in data_sources:
        queries.append(("quora_signal", f"site:quora.com {audience} {category} problem solution"))
    if "pantip" in data_sources:
        queries.append(("pantip_signal", f"site:pantip.com {category} {market} review problem recommendation"))
    if "problem" in data_sources:
        queries.append(("problem_signal", f"{audience} problems solved by {category} product"))
    queries.append(("content_signal", f"{base} short video product ideas visual demo before after"))

    for seed in seeds:
        if "tiktok" in data_sources:
            queries.append(("seed_tiktok", f"{seed} viral product {platform} {market}"))
        if "tiktok_creative" in data_sources:
            queries.append(("seed_tiktok_creative", f"site:ads.tiktok.com/business/creativecenter {seed} top ads products"))
        if "1688" in data_sources or "aliexpress" in data_sources:
            queries.append(("seed_sourcing", f"{seed} wholesale aliexpress 1688 amazon"))
        if "alibaba" in data_sources:
            queries.append(("seed_alibaba", f"site:alibaba.com {seed} supplier factory wholesale"))
        if "creator" in data_sources:
            queries.append(("seed_creator", f"{seed} tiktok shop affiliate influencer video"))
        if "google_trends" in data_sources:
            queries.append(("seed_google_trends", f"site:trends.google.com/trends {seed} trend {market}"))
        if "pinterest_trends" in data_sources:
            queries.append(("seed_pinterest_trends", f"site:pinterest.com/trends {seed} trend"))
        if "meta_ads" in data_sources:
            queries.append(("seed_meta_ads", f"site:facebook.com/ads/library {seed} ads ecommerce"))
        if "youtube" in data_sources:
            queries.append(("seed_youtube", f"site:youtube.com {seed} review demo shorts"))
        if "reddit" in data_sources:
            queries.append(("seed_reddit", f"site:reddit.com {seed} problem review recommendation"))
        if "quora" in data_sources:
            queries.append(("seed_quora", f"site:quora.com {seed} problem solution"))
        if "pantip" in data_sources:
            queries.append(("seed_pantip", f"site:pantip.com {seed} review recommendation"))
    return queries


def search_duckduckgo(query, limit=5):
    params = urllib.parse.urlencode({"q": query})
    url = f"{SEARCH_ENDPOINT}?{params}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8", errors="ignore")
    return parse_duckduckgo_results(body, limit)


def parse_duckduckgo_results(body, limit):
    results = []
    blocks = re.findall(r'<div class="result results_links.*?</div>\s*</div>', body, flags=re.S)
    if not blocks:
        blocks = re.findall(r'<a rel="nofollow" class="result__a".*?</a>.*?(?:<a|</body>)', body, flags=re.S)
    for block in blocks:
        title_match = re.search(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S)
        if not title_match:
            continue
        link = clean_ddg_link(html.unescape(title_match.group(1)))
        title = clean_text(title_match.group(2))
        snippet_match = re.search(r'class="result__snippet"[^>]*>(.*?)</a>|class="result__snippet"[^>]*>(.*?)</div>', block, flags=re.S)
        snippet = ""
        if snippet_match:
            snippet = clean_text(snippet_match.group(1) or snippet_match.group(2) or "")
        if title:
            results.append({"title": title, "snippet": snippet, "link": link})
        if len(results) >= limit:
            break
    return results


def clean_ddg_link(link):
    parsed = urllib.parse.urlparse(link)
    if parsed.path.startswith("/l/"):
        query = urllib.parse.parse_qs(parsed.query)
        if "uddg" in query:
            return query["uddg"][0]
    return link


def clean_text(value):
    value = re.sub(r"<.*?>", " ", value, flags=re.S)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def infer_product_name(title, snippet, profile):
    text = f"{title} {snippet}"
    text = re.sub(r"[-|:–—].*$", "", text)
    text = re.sub(r"\b\d{4}\b", "", text)
    text = re.sub(r"[^A-Za-z0-9\u4e00-\u9fa5 ]+", " ", text)
    words = [word.strip().lower() for word in text.split() if word.strip()]
    words = [word for word in words if word not in STOPWORDS and len(word) > 1]
    if not words:
        return ""

    category_words = [word.lower() for word in re.split(r"\W+", profile.get("category", "")) if word]
    audience_words = [word.lower() for word in re.split(r"\W+", profile.get("audience", "")) if word]
    useful = []
    for word in words:
        if word in category_words or word in audience_words or word in STOPWORDS:
            continue
        useful.append(word)
        if len(useful) >= 5:
            break
    return english_keyword(" ".join((useful or words)[:5]), profile)


def normalize_name(name):
    name = re.sub(r"[^\w\u0e00-\u0e7f\u4e00-\u9fa5 ]+", " ", name.lower(), flags=re.UNICODE)
    words = [word for word in name.split() if word and word not in STOPWORDS]
    return " ".join(words[:5])


def build_candidates(signals):
    candidates = {}
    for signal in signals:
        key = signal.product_id or normalize_name(signal.product)
        if not is_valid_candidate_key(key):
            continue
        if key not in candidates:
            candidates[key] = Candidate(name=signal.product)
        candidates[key].signals.append(signal)
    return candidates


def is_valid_candidate_key(key):
    if not key:
        return False
    if key in GENERIC_CANDIDATES:
        return False
    words = key.split()
    if len(words) == 1 and len(words[0]) < 4:
        return False
    if len(words) == 1 and words[0] in GENERIC_CANDIDATES:
        return False
    generic_count = sum(1 for word in words if word in GENERIC_CANDIDATES)
    if generic_count >= max(len(words) - 1, 1):
        return False
    return True


def score_candidates(candidates, profile):
    for candidate in candidates.values():
        text = candidate.evidence_text
        source_count = len(candidate.sources)
        explicit_sales = sum(signal.sales for signal in candidate.signals)
        explicit_videos = sum(signal.video_count for signal in candidate.signals)
        explicit_influencers = sum(signal.influencer_count for signal in candidate.signals)
        explicit_lives = sum(signal.live_count for signal in candidate.signals)

        novelty = score_keyword_density(text, VISUAL_WORDS, base=10, per_hit=5, cap=20)
        demand = score_keyword_density(text, DEMAND_WORDS, base=12, per_hit=4, cap=25)
        virality = score_virality(text, source_count)
        competition = score_competition(candidate)
        sourcing = score_sourcing(text, profile)
        risk_flags = detect_risks(text)
        test_feasibility = score_test_feasibility(text, source_count, risk_flags)
        group_counts = free_signal_group_counts(candidate)

        if explicit_sales:
            demand = min(25, max(demand, 14 + min(explicit_sales // 5000, 11)))
        if explicit_videos or explicit_influencers or explicit_lives:
            virality = min(20, max(virality, 10 + min((explicit_videos + explicit_influencers + explicit_lives) // 3, 10)))
        demand = min(25, demand + min(group_counts.get("trend", 0) + group_counts.get("community", 0), 5))
        virality = min(20, virality + min(group_counts.get("content", 0) + group_counts.get("ads", 0), 5))
        sourcing = min(10, sourcing + min(group_counts.get("sourcing", 0), 2))
        if group_counts.get("marketplace", 0) >= 3:
            competition = max(4, competition - 2)

        candidate.scores = {
            "novelty": novelty,
            "demand": demand,
            "content_virality": virality,
            "competition_control": competition,
            "sourcing_feasibility": sourcing,
            "test_feasibility": test_feasibility,
        }
        if candidate.sources == ["seed"]:
            candidate.scores = {key: max(value - 4, 1) for key, value in candidate.scores.items()}
        candidate.risk_flags = risk_flags
        candidate.leaderboard_metrics = build_leaderboard_metrics(candidate, profile)


def apply_filters(candidates, profile):
    min_score = int(profile.get("min_score") or 0)
    max_risk_count = int(profile.get("max_risk_count") if profile.get("max_risk_count") is not None else 99)
    return [
        candidate for candidate in candidates
        if candidate.total_score >= min_score and len(candidate.risk_flags) <= max_risk_count
    ]


def rank_candidates(candidates, profile):
    mode = profile.get("ranking_mode") or "hot_sales"
    sort_map = {
        "hot_sales": ("sales_signal", "gmv_signal"),
        "hot_push": ("influencer_signal", "video_signal"),
        "content_viral": ("video_signal", "content_virality"),
        "category_opportunity": ("opportunity_gap", "competition_control"),
        "low_risk": ("risk_adjusted_score", "sourcing_feasibility"),
    }
    primary, secondary = sort_map.get(mode, sort_map["hot_sales"])

    def value(candidate, key):
        if key in candidate.leaderboard_metrics:
            return candidate.leaderboard_metrics.get(key) or 0
        return candidate.scores.get(key) or candidate.total_score

    return sorted(candidates, key=lambda item: (value(item, primary), value(item, secondary), item.total_score), reverse=True)


def build_leaderboard_metrics(candidate, profile):
    text = candidate.evidence_text
    source_count = len(candidate.sources)
    mentions = sum(signal.mentions for signal in candidate.signals)
    explicit_sales = sum(signal.sales for signal in candidate.signals)
    explicit_gmv = sum(signal.gmv for signal in candidate.signals)
    explicit_videos = sum(signal.video_count for signal in candidate.signals)
    explicit_influencers = sum(signal.influencer_count for signal in candidate.signals)
    explicit_lives = sum(signal.live_count for signal in candidate.signals)
    commissions = [signal.commission_rate for signal in candidate.signals if signal.commission_rate]
    cycle = profile.get("cycle") or "week"
    evidence_count = len(candidate.signals)
    visual_hits = count_hits(text, VISUAL_WORDS)
    demand_hits = count_hits(text, DEMAND_WORDS)
    sourcing_hits = count_hits(text, {"aliexpress", "1688", "alibaba", "wholesale", "supplier"})
    creator_hits = count_hits(text, {"influencer", "affiliate", "creator", "达人", "佣金", "commission"})
    live_hits = count_hits(text, {"live", "livestream", "直播"})
    base_sales = explicit_sales or mentions or evidence_count * 18
    estimated_sales = int(base_sales + demand_hits * 15 + visual_hits * 12 + source_count * 10)
    estimated_videos = int(explicit_videos or evidence_count * 2 + visual_hits * 3 + (6 if "tiktok" in text or "short video" in text else 0))
    estimated_influencers = int(explicit_influencers or source_count * 3 + creator_hits * 4 + max(estimated_videos // 3, 1))
    estimated_lives = int(explicit_lives or live_hits * 3 + max(estimated_influencers // 5, 0))
    estimated_gmv = int(explicit_gmv or estimated_sales * estimate_price_midpoint(profile.get("price_range", ""), profile.get("currency", "")))
    estimated_commission = min(35, 8 + sourcing_hits * 3 + creator_hits * 2)
    opportunity_gap = int(candidate.scores.get("demand", 0) + candidate.scores.get("content_virality", 0) + candidate.scores.get("competition_control", 0) - len(candidate.risk_flags) * 5)

    return {
        "sales": explicit_sales,
        "gmv": explicit_gmv,
        "video_count": explicit_videos,
        "influencer_count": explicit_influencers,
        "live_count": explicit_lives,
        "commission_rate": round(sum(commissions) / len(commissions), 1) if commissions else 0,
        "estimated_sales": estimated_sales,
        "estimated_gmv": estimated_gmv,
        "estimated_video_count": estimated_videos,
        "estimated_influencer_count": estimated_influencers,
        "estimated_live_count": estimated_lives,
        "estimated_commission_rate": round(sum(commissions) / len(commissions), 1) if commissions else estimated_commission,
        "sales_signal": explicit_sales or estimated_sales,
        "gmv_signal": explicit_gmv or estimated_gmv,
        "video_signal": explicit_videos or estimated_videos,
        "influencer_signal": explicit_influencers or estimated_influencers,
        "mentions": mentions,
        "opportunity_gap": max(opportunity_gap, 0),
        "risk_adjusted_score": candidate.total_score,
        "cycle": cycle,
        "is_estimated": not bool(explicit_sales or explicit_gmv or explicit_videos or explicit_influencers or explicit_lives),
    }


def count_hits(text, keywords):
    return sum(1 for keyword in keywords if keyword in text)


def free_signal_group_counts(candidate):
    counts = defaultdict(int)
    for signal in candidate.signals:
        group = source_group_for(signal.source)
        if group:
            counts[group] += 1
    return dict(counts)


def source_group_for(source):
    source = str(source or "").strip()
    for group, sources in FREE_SOURCE_GROUPS.items():
        if source in sources:
            return group
    return ""


def free_signal_breakdown(candidate):
    labels = {
        "trend": "趋势需求",
        "content": "内容热度",
        "ads": "广告验证",
        "marketplace": "竞品平台",
        "sourcing": "供应链",
        "community": "社区痛点",
    }
    counts = free_signal_group_counts(candidate)
    breakdown = []
    for key, label in labels.items():
        count = counts.get(key, 0)
        breakdown.append({
            "key": key,
            "label": label,
            "count": count,
            "score": min(100, count * 25),
            "sources": sorted({
                source_label(signal.source)
                for signal in candidate.signals
                if source_group_for(signal.source) == key
            }),
        })
    return breakdown


def estimate_price_midpoint(price_range, currency=""):
    if str(price_range or "").strip() in {"不限", "全部", "all", "any", "unlimited", "no limit"}:
        price_range = ""
    numbers = [float(item) for item in re.findall(r"\d+(?:\.\d+)?", price_range or "")]
    if len(numbers) >= 2:
        return max(sum(numbers[:2]) / 2, 1)
    if numbers:
        return max(numbers[0], 1)
    defaults = {
        "THB": 750,
        "CNY": 150,
        "VND": 500000,
        "SGD": 35,
        "USD": 25,
        "PHP": 1200,
        "MYR": 100,
    }
    return defaults.get(str(currency or "").upper(), 750)


def score_keyword_density(text, keywords, base, per_hit, cap):
    hits = sum(1 for keyword in keywords if keyword in text)
    return min(base + hits * per_hit, cap)


def score_virality(text, source_count):
    score = 10
    if "tiktok" in text or "short video" in text or "viral" in text:
        score += 6
    if any(word in text for word in VISUAL_WORDS):
        score += 5
    score += min(source_count * 2, 6)
    return min(score, 20)


def score_competition(candidate):
    count = len(candidate.signals)
    text = candidate.evidence_text
    score = 15
    if count > 8:
        score -= 4
    if "amazon" in text and "aliexpress" in text:
        score -= 3
    if any(item in text for item in ["shopee", "lazada", "temu"]):
        score -= 2
    if "unique" in text or "new" in text or "novelty" in text:
        score += 3
    return max(min(score, 15), 4)


def score_sourcing(text, profile):
    score = 8
    if "aliexpress" in text or "1688" in text or "alibaba" in text or "wholesale" in text:
        score += 5
    preferences = " ".join(profile.get("preferences", [])).lower()
    if "lightweight" in preferences or "easy to source" in preferences:
        score += 2
    if "fragile" in text or "glass" in text or "liquid" in text:
        score -= 4
    return max(min(score, 10), 1)


def score_test_feasibility(text, source_count, risk_flags):
    score = 6 + min(source_count, 3)
    if any(item in text for item in ["portable", "foldable", "mini", "lightweight", "demo", "before after"]):
        score += 2
    if any(item in text for item in ["supplier", "wholesale", "1688", "alibaba", "aliexpress"]):
        score += 1
    if risk_flags:
        score -= min(len(risk_flags), 3)
    return max(min(score, 10), 1)


def detect_risks(text):
    flags = []
    for keyword in RISK_WORDS:
        if keyword in text:
            flags.append(keyword)
    return sorted(set(flags))


def build_report(profile, ranked):
    report = []
    report.append("# Novelty Product Scout Report\n\n")
    report.append("## Market Profile\n\n")
    report.append(f"- Market: {profile.get('market', '')}\n")
    report.append(f"- Platform: {profile.get('platform', '')}\n")
    report.append(f"- Audience: {profile.get('audience', '')}\n")
    report.append(f"- Category: {profile.get('category', '')}\n")
    report.append(f"- Price range: {format_price_range(profile)}\n")
    report.append(f"- Ranking mode: {ranking_mode_label(profile.get('ranking_mode'))}\n")
    report.append(f"- Cycle: {cycle_label(profile.get('cycle'))}\n")
    report.append("- Data source: 信源采集；销量/GMV为机会评分估算，不是平台真实销量\n")
    report.append(f"- Sources: {', '.join(source_label(item) for item in profile.get('data_sources', []))}\n")
    report.append(f"- Preferences: {', '.join(profile.get('preferences', []))}\n\n")

    report.append("## Executive Summary\n\n")
    if ranked:
        report.append(
            f"The scout found {len(ranked)} candidate product opportunities. "
            f"The top opportunity is **{ranked[0].name}** with a score of {ranked[0].total_score}. "
            "Treat this as a test shortlist, not a guaranteed viral prediction.\n\n"
        )
    else:
        report.append("No candidates were found. Broaden the category, price band, or ranking cycle.\n\n")

    report.append("## Opportunity Ranking\n\n")
    sales_label = "Sales Estimate"
    gmv_label = "GMV Estimate"
    report.append(f"| Rank | Product | Score | Confidence | {sales_label} | {gmv_label} | Videos | Influencers | Risk |\n")
    report.append("| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |\n")
    for index, candidate in enumerate(ranked[:15], start=1):
        risk = ", ".join(candidate.risk_flags[:3]) if candidate.risk_flags else "none detected"
        metrics = candidate.leaderboard_metrics
        confidence = build_confidence(candidate)
        report.append(
            f"| {index} | {candidate.name} | {candidate.total_score} | {confidence['label']} | {metrics.get('sales_signal', 0)} | "
            f"{format_money(metrics.get('gmv_signal', 0), profile)} | {metrics.get('video_signal', 0)} | {metrics.get('influencer_signal', 0)} | {risk} |\n"
        )

    report.append("\n## Product Details\n")
    for index, candidate in enumerate(ranked[:8], start=1):
        report.append(build_candidate_section(index, candidate, profile))

    report.append("\n## How To Use This Report\n\n")
    report.append("- Pick 2-3 A/B-grade products for manual validation.\n")
    report.append("- Search the generated sourcing keywords on 1688, Alibaba, AliExpress, Amazon, TikTok, and Xiaohongshu.\n")
    report.append("- Do not buy inventory before checking IP, compliance, shipping cost, and return risk.\n")
    report.append("- Run a small content test first: 3 short videos, 1 landing page, and a small ad budget or organic creator test.\n")
    return "".join(report)


def build_candidate_section(index, candidate, profile):
    scores = candidate.scores
    audience = profile.get("audience", "target users")
    category = profile.get("category", "product category")
    product = candidate.name
    sourcing_keywords = build_sourcing_keywords(product, profile)
    hook = build_video_hook(product, audience)
    risks = ", ".join(candidate.risk_flags) if candidate.risk_flags else "No obvious high-risk keyword detected. Still verify compliance and IP manually."
    metrics = candidate.leaderboard_metrics

    section = []
    section.append(f"\n### {index}. {product}\n\n")
    section.append(f"- Score: {candidate.total_score} / 100\n")
    section.append(f"- Grade: {candidate.grade}\n")
    if metrics.get("is_estimated"):
        section.append(
            f"- Public signal estimate: sales signal {metrics.get('sales_signal', 0)}, GMV signal {format_money(metrics.get('gmv_signal', 0), profile)}, "
            f"videos {metrics.get('video_signal', 0)}, influencers {metrics.get('influencer_signal', 0)}, "
            f"lives {metrics.get('estimated_live_count', 0)}, commission {metrics.get('estimated_commission_rate', 0)}%\n"
        )
    else:
        section.append(
            f"- Structured data: sales {metrics.get('sales', 0)}, GMV {format_money(metrics.get('gmv', 0), profile)}, "
            f"videos {metrics.get('video_count', 0)}, influencers {metrics.get('influencer_count', 0)}, "
            f"lives {metrics.get('live_count', 0)}, commission {metrics.get('commission_rate', 0)}%\n"
        )
    section.append(f"- Target user: {audience}\n")
    section.append(f"- Likely pain point: {infer_pain_point(product, category, audience)}\n")
    section.append(f"- Decision: {build_decision_summary(candidate, profile)}\n")
    section.append(f"- Data confidence: {build_confidence(candidate)['label']} - {build_confidence(candidate)['reason']}\n")
    section.append(f"- Competition density: {build_competitor_density(candidate)['label']} - {build_competitor_density(candidate)['reason']}\n")
    section.append(f"- Short-video hook: {hook}\n")
    section.append(f"- Livestream angle: Show the problem first, demonstrate the product in under 10 seconds, then compare before/after.\n")
    section.append(f"- Sourcing keywords: {', '.join(sourcing_keywords)}\n")
    section.append(f"- Risks: {risks}\n")
    section.append(f"- Do not do if: {'; '.join(build_avoid_reasons(candidate, profile))}\n")
    section.append("\nScore breakdown:\n\n")
    section.append("| Dimension | Score |\n| --- | ---: |\n")
    labels = {
        "novelty": "Novelty",
        "demand": "Demand strength",
        "content_virality": "Content virality",
        "competition_control": "Competition control",
        "sourcing_feasibility": "Sourcing feasibility",
        "test_feasibility": "Test feasibility",
    }
    for key, label in labels.items():
        section.append(f"| {label} | {scores.get(key, 0)} |\n")

    section.append("\nFree source breakdown:\n\n")
    section.append("| Source group | Evidence count | Score |\n| --- | ---: | ---: |\n")
    for item in free_signal_breakdown(candidate):
        section.append(f"| {item['label']} | {item['count']} | {item['score']} |\n")

    section.append("\nEvidence:\n")
    for signal in candidate.signals[:4]:
        title = signal.title or signal.product
        snippet = signal.snippet or signal.notes
        link = f" ({signal.link})" if signal.link else ""
        section.append(f"- [{source_label(signal.source)}] {title}{link}\n")
        if snippet:
            section.append(f"  - {snippet[:240]}\n")

    section.append("\nFirst validation plan:\n")
    for item in build_validation_plan(candidate, profile):
        section.append(f"- {item}\n")

    section.append("\nVideo scripts:\n")
    for script in build_video_scripts(product, audience):
        section.append(f"- {script['type']}: {script['script']}\n")
    return "".join(section)


def candidate_to_dict(candidate, profile):
    metrics = candidate.leaderboard_metrics
    destination_links = build_destination_links(candidate, profile)
    confidence = build_confidence(candidate)
    risk_assessment = build_risk_assessment(candidate)
    competitor_density = build_competitor_density(candidate)
    return {
        "name": candidate.name,
        "total_score": candidate.total_score,
        "grade": candidate.grade,
        "sources": candidate.sources,
        "product_id": first_signal_value(candidate, "product_id"),
        "image_url": first_signal_value(candidate, "image_url"),
        "category_name": first_signal_value(candidate, "category_name"),
        "rating": first_signal_value(candidate, "rating"),
        "review_count": first_signal_value(candidate, "review_count"),
        "primary_link": destination_links[0]["url"] if destination_links else "",
        "destination_links": destination_links,
        "risk_flags": candidate.risk_flags,
        "scores": candidate.scores,
        "leaderboard_metrics": metrics,
        "currency": normalize_currency(profile.get("currency", "")),
        "formatted_price_range": format_price_range(profile),
        "formatted_gmv": format_money(metrics.get("gmv", 0), profile),
        "formatted_gmv_signal": format_money(metrics.get("gmv_signal", 0), profile),
        "ranking_reason": build_ranking_reason(candidate, profile),
        "decision_summary": build_decision_summary(candidate, profile),
        "avoid_reasons": build_avoid_reasons(candidate, profile),
        "data_confidence": confidence,
        "risk_assessment": risk_assessment,
        "competitor_density": competitor_density,
        "free_signal_breakdown": free_signal_breakdown(candidate),
        "target_user": profile.get("audience", "target users"),
        "pain_point": infer_pain_point(candidate.name, profile.get("category", ""), profile.get("audience", "target users")),
        "video_hook": build_video_hook(candidate.name, profile.get("audience", "target users")),
        "livestream_angle": "Show the problem first, demonstrate the product in under 10 seconds, then compare before/after.",
        "sourcing_keywords": build_sourcing_keywords(candidate.name, profile),
        "multilingual_sourcing_keywords": build_multilingual_sourcing_keywords(candidate.name, profile),
        "evidence": [
            {
                "source": source_label(signal.source),
                "type": signal_type(signal),
                "title": signal.title or signal.product,
                "snippet": signal.snippet or signal.notes,
                "link": signal.link,
                "sales": signal.sales,
                "gmv": signal.gmv,
                "rank_position": signal.rank_position,
                "category_name": signal.category_name,
            }
            for signal in candidate.signals[:6]
        ],
        "verification_checklist": build_verification_checklist(candidate, profile),
        "validation_plan": build_validation_plan(candidate, profile),
        "video_scripts": build_video_scripts(candidate.name, profile.get("audience", "target users")),
    }


def first_signal_value(candidate, field_name):
    for signal in candidate.signals:
        value = getattr(signal, field_name, "")
        if value:
            return value
    return ""


def source_label(source):
    return SOURCE_LABELS.get(str(source or "").strip(), str(source or "").strip())


def signal_type(signal):
    if signal.link:
        return "真实来源链接"
    if any([signal.sales, signal.gmv, signal.video_count, signal.influencer_count, signal.live_count, signal.commission_rate]):
        return "用户 CSV 数据"
    if signal.source == "seed":
        return "种子词"
    if signal.source:
        return "公开网页线索"
    return "公开线索"


def build_confidence(candidate):
    link_count = sum(1 for signal in candidate.signals if signal.link)
    csv_metric_count = sum(
        1 for signal in candidate.signals
        if any([signal.sales, signal.gmv, signal.video_count, signal.influencer_count, signal.live_count, signal.commission_rate])
    )
    source_count = len(candidate.sources)
    seed_only = candidate.sources == ["seed"]
    score = 35
    score += min(link_count * 12, 30)
    score += min(csv_metric_count * 14, 28)
    score += min(source_count * 6, 18)
    if seed_only:
        score -= 25
    score = max(min(score, 95), 15)
    if score >= 78:
        label = "高"
    elif score >= 55:
        label = "中"
    else:
        label = "低"
    reason_parts = []
    if link_count:
        reason_parts.append(f"{link_count} 个真实来源链接")
    if csv_metric_count:
        reason_parts.append(f"{csv_metric_count} 条结构化榜单数据")
    if source_count:
        reason_parts.append(f"{source_count} 类来源")
    if seed_only:
        reason_parts.append("主要来自种子词")
    reason = "，".join(reason_parts) if reason_parts else "来自公开线索和估算"
    return {"score": score, "label": label, "reason": reason}


def build_risk_assessment(candidate):
    flags = candidate.risk_flags
    if not flags:
        return {
            "level": "low",
            "label": "低",
            "summary": "未命中明显高风险词，仍需人工核查平台禁售、侵权和合规。",
            "items": [],
        }
    severity_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    level = "medium"
    items = []
    for flag in flags:
        severity = RISK_SEVERITY.get(flag, "medium")
        if severity_order[severity] > severity_order[level]:
            level = severity
        items.append({
            "keyword": flag,
            "severity": severity,
            "action": risk_action(flag, severity),
        })
    labels = {"low": "低", "medium": "中", "high": "高", "critical": "极高"}
    return {
        "level": level,
        "label": labels[level],
        "summary": f"命中 {len(flags)} 个风险词，最高等级 {labels[level]}。",
        "items": items,
    }


def risk_action(flag, severity):
    if severity == "critical":
        return f"先查平台禁售和当地法规，未确认前不要上架：{flag}。"
    if severity == "high":
        return f"需要人工合规/侵权核查，确认供应商资质和素材授权：{flag}。"
    return f"核查包装、物流、退货和破损率：{flag}。"


def build_competitor_density(candidate):
    text = candidate.evidence_text
    marketplace_hits = count_hits(text, {"amazon", "aliexpress", "temu", "shopee", "lazada", "1688", "alibaba"})
    listing_count = len(candidate.signals)
    if listing_count >= 8 or marketplace_hits >= 4:
        level = "high"
        label = "高"
        reason = "多个市场/来源都出现同类产品，可能已经较卷。"
    elif listing_count >= 4 or marketplace_hits >= 2:
        level = "medium"
        label = "中"
        reason = "已有一定同款和替代品，需要靠内容角度或组合包装差异化。"
    else:
        level = "low"
        label = "低"
        reason = "公开同类信号较少，可能是早期机会，也可能是需求不足。"
    return {"level": level, "label": label, "reason": reason}


def build_decision_summary(candidate, profile):
    confidence = build_confidence(candidate)
    risk = build_risk_assessment(candidate)
    density = build_competitor_density(candidate)
    if risk["level"] in {"critical", "high"}:
        return "先核查风险，不建议直接上架。"
    if candidate.total_score >= 78 and confidence["label"] != "低":
        return "适合进入小预算测试，先验证内容点击率和供应链价格。"
    if density["level"] == "high":
        return "只适合做差异化内容测试，不适合直接铺货。"
    if candidate.total_score >= 62:
        return "可以加入观察名单，补足真实榜单和供应链数据后再测。"
    return "暂不建议投入预算，除非你有额外强证据。"


def build_avoid_reasons(candidate, profile):
    risk = build_risk_assessment(candidate)
    density = build_competitor_density(candidate)
    reasons = []
    if risk["level"] in {"critical", "high"}:
        reasons.append("合规或侵权风险没有确认")
    if density["level"] == "high":
        reasons.append("同款过多且没有明确差异化卖点")
    if build_confidence(candidate)["label"] == "低":
        reasons.append("当前证据主要是推断，缺少真实链接或榜单数据")
    if not reasons:
        reasons.append("差评、供应链稳定性和素材授权没有人工核查")
    return reasons


def build_verification_checklist(candidate, profile):
    product = candidate.name
    return [
        checklist_item("TikTok 热度", "在 TikTok/TikTok Shop 搜索同名和同义关键词，确认近期视频、店铺和销量信号。", "待验证"),
        checklist_item("达人带货", "检查是否有达人/联盟视频，记录佣金率、视频互动和是否适合寄样。", "待验证"),
        checklist_item("供应链", f"用 {product}、中文词、功能词在 1688/AliExpress/Alibaba 搜索，记录可信供应商、起订量和发货地。", "待验证"),
        checklist_item("竞品密度", "找到 5 个竞品，比较价格、卖点、评论数、差评主题和内容角度。", "待验证"),
        checklist_item("风险合规", "核查侵权、儿童安全、食品、化妆品、医疗宣称、电池、液体和平台禁售。", "待验证"),
        checklist_item("物流退货", "确认重量、体积、易碎性、安装复杂度和退货概率。", "待验证"),
    ]


def checklist_item(title, action, status):
    return {"title": title, "action": action, "status": status}


def build_validation_plan(candidate, profile):
    product = candidate.name
    return [
        "先用跳转链接核对真实视频、店铺、竞品和供应链页面。",
        "记录 3 个供应商报价、起订量、发货地、重量和退换货条款。",
        "做 3 条短视频：痛点开场、前后对比、反常识/惊喜用法。",
        "小范围验证内容点击、询单质量和样品反馈后，再决定是否加大测试。",
        f"如果 {product} 的点击率、询单率或样品反馈低于预期，立即停止加预算。",
    ]


def build_video_scripts(product, audience):
    return [
        {
            "type": "痛点型",
            "script": f"先拍 {audience} 的日常麻烦，3 秒内切到 {product} 的解决动作，最后给出前后对比。"
        },
        {
            "type": "前后对比型",
            "script": f"左边展示不用 {product} 的结果，右边展示使用后变化，用同一场景强调省时和可视化效果。"
        },
        {
            "type": "猎奇反转型",
            "script": f"开头说“我以为这只是普通小工具”，随后展示 {product} 的意外用途和真实反应。"
        },
    ]


def build_multilingual_sourcing_keywords(product, profile):
    category = profile.get("category", "")
    base = [
        product,
        f"{product} wholesale",
        f"{product} supplier",
        f"{product} factory",
        f"{product} 1688",
        f"{product} aliexpress",
    ]
    chinese = [
        f"{product} 批发",
        f"{product} 工厂",
        f"{product} 货源",
        f"{category} 新奇特",
    ]
    scenario = [
        f"{product} for {profile.get('audience', 'users')}",
        f"{product} demo",
        f"{product} before after",
    ]
    return {"english": base, "chinese": chinese, "scenario": scenario}


def build_destination_links(candidate, profile):
    links = []
    seen = set()
    for signal in candidate.signals:
        if signal.product_url and signal.product_url not in seen:
            links.append({
                "label": "TikTok Shop 商品页",
                "url": signal.product_url,
            })
            seen.add(signal.product_url)
        if signal.link and signal.link not in seen:
            links.append({
                "label": source_label(signal.source) or "source",
                "url": signal.link,
            })
            seen.add(signal.link)

    product = candidate.name
    platform = (profile.get("platform") or "").lower()
    search_targets = []
    if "tiktok" in platform or "小店" in platform:
        search_targets.append(("TikTok search", f"https://www.tiktok.com/search?q={urllib.parse.quote(product)}"))
        search_targets.append(("TikTok Shop search", f"https://www.tiktok.com/shop/s/{urllib.parse.quote(product)}"))
    if "douyin" in platform or "抖音" in platform:
        search_targets.append(("Douyin search", f"https://www.douyin.com/search/{urllib.parse.quote(product)}"))
    if "xiaohongshu" in platform or "小红书" in platform:
        search_targets.append(("Xiaohongshu search", f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(product)}"))

    search_targets.extend([
        ("Google Trends", f"https://trends.google.com/trends/explore?q={urllib.parse.quote(product)}"),
        ("TikTok Creative Center", f"https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en?search={urllib.parse.quote(product)}"),
        ("Meta Ad Library", f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={urllib.parse.quote(product)}&search_type=keyword_unordered"),
        ("Pinterest search", f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(product)}"),
        ("Amazon search", f"https://www.amazon.com/s?k={urllib.parse.quote(product)}"),
        ("Shopee TH search", f"https://shopee.co.th/search?keyword={urllib.parse.quote(product)}"),
        ("Lazada TH search", f"https://www.lazada.co.th/catalog/?q={urllib.parse.quote(product)}"),
        ("AliExpress search", f"https://www.aliexpress.com/wholesale?SearchText={urllib.parse.quote(product)}"),
        ("1688 search", f"https://s.1688.com/selloffer/offer_search.htm?keywords={urllib.parse.quote(product)}"),
        ("Alibaba search", f"https://www.alibaba.com/trade/search?SearchText={urllib.parse.quote(product)}"),
        ("Reddit search", f"https://www.reddit.com/search/?q={urllib.parse.quote(product)}"),
        ("YouTube search", f"https://www.youtube.com/results?search_query={urllib.parse.quote(product)}"),
    ])

    for label, url in search_targets:
        if url not in seen:
            links.append({"label": label, "url": url})
            seen.add(url)
        if len(links) >= 10:
            break
    return links


def build_ranking_reason(candidate, profile):
    mode = profile.get("ranking_mode") or "hot_sales"
    metrics = candidate.leaderboard_metrics
    if mode == "hot_push":
        return f"达人/内容推动强：达人信号 {metrics.get('influencer_signal', 0)}，视频信号 {metrics.get('video_signal', 0)}。"
    if mode == "content_viral":
        return f"内容展示性强：视频信号 {metrics.get('video_signal', 0)}，内容传播分 {candidate.scores.get('content_virality', 0)}。"
    if mode == "category_opportunity":
        return f"类目机会较好：机会缺口 {metrics.get('opportunity_gap', 0)}，竞争可控分 {candidate.scores.get('competition_control', 0)}。"
    if mode == "low_risk":
        return f"风险调整后更稳：总分 {candidate.total_score}，风险词 {len(candidate.risk_flags)} 个。"
    if metrics.get("is_estimated"):
        return f"公开热度信号靠前：销量信号 {metrics.get('sales_signal', 0)}，GMV信号 {format_money(metrics.get('gmv_signal', 0), profile)}。"
    return f"结构化榜单靠前：销量 {metrics.get('sales', 0)}，GMV {format_money(metrics.get('gmv', 0), profile)}。"


def normalize_currency(value):
    value = str(value or "THB").strip().upper()
    return value if value else "THB"


def currency_symbol(currency):
    symbols = {
        "THB": "฿",
        "CNY": "¥",
        "VND": "₫",
        "SGD": "S$",
        "USD": "$",
        "PHP": "₱",
        "MYR": "RM",
    }
    return symbols.get(normalize_currency(currency), normalize_currency(currency))


def format_price_range(profile):
    price_range = str(profile.get("price_range") or "").strip()
    currency = normalize_currency(profile.get("currency", "THB"))
    if price_range in {"不限", "全部", "all", "any", "unlimited", "no limit"}:
        return "不限"
    if not price_range:
        return "不限"
    if re.search(r"\b(THB|CNY|VND|SGD|USD|PHP|MYR)\b", price_range, flags=re.I):
        return price_range
    return f"{price_range} {currency}"


def format_money(value, profile):
    currency = normalize_currency(profile.get("currency", "THB"))
    symbol = currency_symbol(currency)
    try:
        number = float(value or 0)
    except (TypeError, ValueError):
        number = 0
    if currency == "VND":
        amount = f"{number:,.0f}"
    elif number >= 1000:
        amount = f"{number:,.0f}"
    else:
        amount = f"{number:g}"
    return f"{symbol}{amount}"


def ranking_mode_label(mode):
    labels = {
        "hot_sales": "Hot sales potential",
        "hot_push": "Hot push potential",
        "content_viral": "Content virality",
        "category_opportunity": "Category opportunity",
        "low_risk": "Low-risk shortlist",
    }
    return labels.get(mode or "hot_sales", mode or "hot_sales")


def cycle_label(cycle):
    labels = {"day": "Day", "week": "Week", "month": "Month"}
    return labels.get(cycle or "week", cycle or "week")


def build_sourcing_keywords(product, profile):
    category = profile.get("category", "")
    words = [product, f"{product} wholesale", f"{product} 1688", f"{product} aliexpress"]
    if category:
        words.append(f"{category} novelty supplier")
    return words


def build_video_hook(product, audience):
    return f"{audience} do not realize this {product} can solve an annoying daily problem in seconds."


def infer_pain_point(product, category, audience):
    text = f"{product} {category}".lower()
    if "hair" in text or "groom" in text:
        return f"{audience} struggle with cleaning hair, grooming, or keeping the home tidy."
    if "organizer" in text or "storage" in text:
        return f"{audience} need a cleaner, faster way to organize small daily-use items."
    if "clean" in text or "remover" in text:
        return f"{audience} want a visible cleaning result with less effort."
    if "toy" in text:
        return f"{audience} want a more engaging and shareable product experience."
    return f"{audience} have a recurring small inconvenience in {category} that can be shown visually."


if __name__ == "__main__":
    main()
