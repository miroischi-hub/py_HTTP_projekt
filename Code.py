#!/usr/bin/env python3
"""
Python HTTP Projekt (Minimalsystem + Selenium/Chrome)

Commands:
- python myproject.py "title"
- python myproject.py scrape-tag --url https://example.com title
- python myproject.py get --url https://httpbin.org/get --param a=1 --param b=hello
- python myproject.py post --url https://httpbin.org/post --field a=1 --field b=hello
- python myproject.py list-cookies --url https://example.com
- python myproject.py selenium-title --url https://example.com
- python myproject.py selenium-cookies --url https://example.com
- python myproject.py selenium-screenshot --url https://example.com --out page.png
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests

# Selenium (Chrome)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


DEFAULT_URL = "https://example.com"


@dataclass
class HttpResult:
    status_code: int
    elapsed_ms: int
    final_url: str
    text: str


def _kv_list_to_dict(items: List[str]) -> Dict[str, str]:
    """
    Converts ["a=1","b=hello"] to {"a":"1","b":"hello"}.
    Ignores empty list.
    """
    data: Dict[str, str] = {}
    for it in items:
        if "=" not in it:
            raise ValueError(f"Ungültig (erwarte key=value): {it}")
        k, v = it.split("=", 1)
        data[k] = v
    return data


def scrape_html_tag(url: str, tag: str) -> str:
    """
    Minimal Scraping: findet ersten <tag>...</tag> Block (case-insensitive).
    Fürs Minimalsystem genügt das i.d.R. für <title>.
    """
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    html = r.text

    open_tag = f"<{tag}>".lower()
    close_tag = f"</{tag}>".lower()

    low = html.lower()
    start = low.find(open_tag)
    end = low.find(close_tag)

    if start == -1 or end == -1 or end < start:
        return f"(tag <{tag}> nicht gefunden)"
    start += len(open_tag)
    return html[start:end].strip()


def http_get(url: str, params: List[str]) -> HttpResult:
    q = _kv_list_to_dict(params)
    t0 = time.perf_counter()
    r = requests.get(url, params=q, timeout=10)
    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    r.raise_for_status()
    return HttpResult(r.status_code, elapsed_ms, str(r.url), r.text)


def http_post(url: str, fields: List[str]) -> HttpResult:
    data = _kv_list_to_dict(fields)
    t0 = time.perf_counter()
    r = requests.post(url, data=data, timeout=10)
    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    r.raise_for_status()
    return HttpResult(r.status_code, elapsed_ms, str(r.url), r.text)


def list_cookies_requests(url: str) -> str:
    """
    Cookies via requests.Session() sammeln und ausgeben.
    """
    s = requests.Session()
    r = s.get(url, timeout=10)
    r.raise_for_status()

    if not s.cookies:
        return "(keine Cookies erhalten)"

    lines = []
    for c in s.cookies:
        # c.domain kann None/leer sein je nach Cookie
        lines.append(f"{c.name}={c.value}; domain={c.domain}; path={c.path}")
    return "\n".join(lines)


def create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Erstellt Chrome WebDriver. webdriver-manager lädt passenden Driver automatisch.
    Headless default: True (CI/Server-freundlich).
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def selenium_title(url: str, headless: bool = True) -> str:
    driver = create_chrome_driver(headless=headless)
    try:
        driver.get(url)
        return driver.title
    finally:
        driver.quit()


def selenium_cookies(url: str, headless: bool = True) -> str:
    driver = create_chrome_driver(headless=headless)
    try:
        driver.get(url)
        cookies = driver.get_cookies()
        if not cookies:
            return "(keine Cookies)"
        lines = []
        for c in cookies:
            # keys: name, value, domain, path, expiry, httpOnly, secure, sameSite ...
            lines.append(f"{c.get('name')}={c.get('value')}; domain={c.get('domain')}; path={c.get('path')}")
        return "\n".join(lines)
    finally:
        driver.quit()


def selenium_screenshot(url: str, out_path: str, headless: bool = True) -> str:
    driver = create_chrome_driver(headless=headless)
    try:
        driver.get(url)
        ok = driver.save_screenshot(out_path)
        return out_path if ok else "(screenshot fehlgeschlagen)"
    finally:
        driver.quit()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="myproject.py",
        description="Python HTTP Projekt: GET/POST/Cookies + Scraping + Selenium(Chrome)",
    )
    sub = p.add_subparsers(dest="cmd")

    # scrape-tag
    ps = sub.add_parser("scrape-tag", help="Inhalt eines HTML-Tags anzeigen (z.B. title)")
    ps.add_argument("--url", default=DEFAULT_URL)
    ps.add_argument("tag", help="z.B. title")

    # get
    pg = sub.add_parser("get", help="GET request mit Variablen")
    pg.add_argument("--url", required=True)
    pg.add_argument("--param", action="append", default=[], help="key=value (mehrfach möglich)")

    # post
    pp = sub.add_parser("post", help="POST request mit Variablen (Form submission)")
    pp.add_argument("--url", required=True)
    pp.add_argument("--field", action="append", default=[], help="key=value (mehrfach möglich)")

    # list-cookies
    pc = sub.add_parser("list-cookies", help="Liste der Cookies anzeigen (requests.Session)")
    pc.add_argument("--url", required=True)

    # selenium-title
    pst = sub.add_parser("selenium-title", help="Title via Selenium (Chrome)")
    pst.add_argument("--url", required=True)
    pst.add_argument("--show-browser", action="store_true", help="Chrome sichtbar starten (nicht headless)")

    # selenium-cookies
    psc = sub.add_parser("selenium-cookies", help="Cookies via Selenium (Chrome)")
    psc.add_argument("--url", required=True)
    psc.add_argument("--show-browser", action="store_true", help="Chrome sichtbar starten (nicht headless)")

    # selenium-screenshot
    pss = sub.add_parser("selenium-screenshot", help="Screenshot via Selenium (Chrome)")
    pss.add_argument("--url", required=True)
    pss.add_argument("--out", default="page.png", help="Dateiname für Screenshot (default: page.png)")
    pss.add_argument("--show-browser", action="store_true", help="Chrome sichtbar starten (nicht headless)")

    # Komfort-Fallback: python myproject.py "title"
    p.add_argument("maybe_tag", nargs="?", help='Wenn kein Command: wird als Tag interpretiert (z.B. "title")')
    p.add_argument("--url", default=DEFAULT_URL, help="Default URL für maybe_tag (fallback)")
    return p


def _print_http_result(res: HttpResult) -> None:
    print(f"Status: {res.status_code} | Time: {res.elapsed_ms}ms")
    print(f"URL:    {res.final_url}")
    print()
    print(res.text)


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.cmd == "scrape-tag":
            print(scrape_html_tag(args.url, args.tag))
            return 0

        if args.cmd == "get":
            res = http_get(args.url, args.param)
            _print_http_result(res)
            return 0

        if args.cmd == "post":
            res = http_post(args.url, args.field)
            _print_http_result(res)
            return 0

        if args.cmd == "list-cookies":
            print(list_cookies_requests(args.url))
            return 0

        if args.cmd == "selenium-title":
            print(selenium_title(args.url, headless=not args.show_browser))
            return 0

        if args.cmd == "selenium-cookies":
            print(selenium_cookies(args.url, headless=not args.show_browser))
            return 0

        if args.cmd == "selenium-screenshot":
            out = selenium_screenshot(args.url, args.out, headless=not args.show_browser)
            print(out)
            return 0

        # fallback: python myproject.py "title"
        if args.maybe_tag:
            print(scrape_html_tag(args.url, args.maybe_tag))
            return 0

        parser.print_help()
        return 2

    except ValueError as e:
        print(f"Input-Fehler: {e}", file=sys.stderr)
        return 2
    except requests.RequestException as e:
        print(f"HTTP-Fehler: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
