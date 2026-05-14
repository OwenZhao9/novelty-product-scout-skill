#!/usr/bin/env python3
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / "web"
sys.path.insert(0, str(ROOT / "scripts"))

from scout_products import SourceDataError, public_source_status, run_scout  # noqa: E402


class ScoutHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_POST(self):
        if self.path != "/api/scout":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8")
        try:
            data = json.loads(payload or "{}")
            profile = normalize_profile(data.get("profile") or {})
            signals_csv = data.get("signals_csv") or ""
            no_web = bool(data.get("no_web"))
            limit = int(data.get("limit") or 3)
            result = run_scout(
                profile=profile,
                signals_csv_text=signals_csv,
                output_path=str(ROOT / "output" / "web-report.md"),
                no_web=no_web,
                limit=max(min(limit, 8), 1),
            )
            self.send_json(result)
        except SourceDataError as exc:
            self.send_json({"error": str(exc)}, status=400)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def do_GET(self):
        if self.path == "/api/source-status":
            self.send_json(public_source_status())
            return
        if self.path == "/report.md":
            report_path = ROOT / "output" / "web-report.md"
            if not report_path.exists():
                self.send_response(404)
                self.end_headers()
                return
            body = report_path.read_text(encoding="utf-8").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/report":
            report_path = ROOT / "output" / "web-report.md"
            if not report_path.exists():
                self.send_json({"report": ""})
                return
            self.send_json({"report": report_path.read_text(encoding="utf-8")})
            return
        super().do_GET()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def normalize_profile(profile):
    return {
        "market": profile.get("market") or "US",
        "platform": profile.get("platform") or "TikTok Shop",
        "data_source_mode": normalize_data_source_mode(profile.get("data_source_mode")),
        "ranking_mode": profile.get("ranking_mode") or "hot_sales",
        "cycle": profile.get("cycle") or "week",
        "audience": normalize_unlimited(profile.get("audience"), "泛人群"),
        "category": normalize_unlimited(profile.get("category"), "全品类"),
        "price_range": normalize_unlimited(profile.get("price_range"), ""),
        "currency": normalize_currency(profile.get("currency") or "THB"),
        "min_score": parse_int(profile.get("min_score"), 0),
        "max_risk_count": parse_int(profile.get("max_risk_count"), 99),
        "data_sources": normalize_data_sources(profile.get("data_sources")),
        "preferences": split_lines_or_commas(profile.get("preferences") or "lightweight, visual demo, low compliance risk"),
        "seed_keywords": split_lines_or_commas(profile.get("seed_keywords") or ""),
    }


def parse_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def normalize_unlimited(value, fallback):
    value = str(value or "").strip()
    if value in {"不限", "全部", "all", "any", "unlimited", "no limit"}:
        return fallback
    return value or fallback


def normalize_currency(value):
    aliases = {
        "泰铢": "THB",
        "人民币": "CNY",
        "越南盾": "VND",
        "新加坡元": "SGD",
        "美金": "USD",
        "美元": "USD",
        "菲律宾": "PHP",
        "菲律宾比索": "PHP",
        "马来西亚币": "MYR",
        "马币": "MYR",
        "林吉特": "MYR",
    }
    value = str(value or "THB").strip()
    return aliases.get(value, value.upper())


def normalize_data_sources(value):
    allowed = {
        "tiktok",
        "tiktok_creative",
        "amazon",
        "amazon_movers",
        "shopee",
        "lazada",
        "aliexpress",
        "1688",
        "alibaba",
        "google_trends",
        "pinterest_trends",
        "meta_ads",
        "xiaohongshu",
        "douyin",
        "reddit",
        "quora",
        "pantip",
        "youtube",
        "problem",
        "creator",
    }
    defaults = [
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
    if not value:
        return defaults
    if isinstance(value, list):
        items = [str(item).strip() for item in value]
    else:
        items = split_lines_or_commas(value)
    selected = [item for item in items if item in allowed]
    return selected or defaults


def normalize_data_source_mode(value):
    return "public"


def split_lines_or_commas(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    normalized = str(value).replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = ThreadingHTTPServer(("127.0.0.1", port), ScoutHandler)
    print(f"Novelty Product Scout web app: http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
