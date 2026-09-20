#!/usr/bin/env python3
"""Interactive YouTube video analyzer powered by Gemini.

Paste a YouTube URL, get back a structured JSON analysis
(title, summary, key points, topics, entities, quotes, sentiment, confidence).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).parent / ".claude" / "skills" / "watch" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

from gemini_analyze import analyze_youtube, load_api_key  # noqa: E402


def main() -> int:
    api_key = load_api_key()
    print("YouTube Video Analyzer (Gemini) — paste a URL, or 'quit' to exit.")
    while True:
        try:
            url = input("\nYouTube URL: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not url or url.lower() in {"quit", "exit"}:
            return 0
        try:
            result = analyze_youtube(url, api_key)
        except SystemExit as exc:
            print(f"Error: {exc}", file=sys.stderr)
            continue
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())
