#!/usr/bin/env python3
"""Analyze a YouTube video directly via the Gemini API.

Unlike watch.py (which downloads the video locally with yt-dlp/ffmpeg and lets
Claude read the extracted frames), this script sends the YouTube URL straight
to Gemini, which fetches and watches the video itself. No local download,
no ffmpeg/yt-dlp required. Useful as a lightweight/headless alternative, or
when GEMINI_API_KEY is the only credential available.

Usage:
    python3 gemini_analyze.py "<youtube-url>" [--intent "what to focus on"]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "topics": {"type": "array", "items": {"type": "string"}},
        "entities": {"type": "array", "items": {"type": "string"}},
        "notable_quotes": {"type": "array", "items": {"type": "string"}},
        "sentiment": {
            "type": "string",
            "enum": ["positive", "neutral", "negative", "mixed"],
        },
        "confidence": {"type": "number"},
    },
    "required": [
        "title", "summary", "key_points", "topics", "entities",
        "notable_quotes", "sentiment", "confidence",
    ],
}


def load_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    for candidate in (Path.cwd() / ".env", Path.home() / ".config" / "watch" / ".env"):
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(
        "No GEMINI_API_KEY found (env var, ./.env, or ~/.config/watch/.env). "
        "Get a key at https://aistudio.google.com/apikey"
    )


def analyze_youtube(url: str, api_key: str, intent: str | None = None) -> dict:
    prompt = (
        "Watch this YouTube video and analyze it. "
        "Respond ONLY with JSON matching the given schema."
    )
    if intent:
        prompt += f" Focus especially on: {intent}."

    body = {
        "contents": [{
            "parts": [
                {"file_data": {"file_uri": url}},
                {"text": prompt},
            ]
        }],
        "generationConfig": {
            "response_mime_type": "application/json",
            "response_schema": RESPONSE_SCHEMA,
        },
    }

    req = urllib.request.Request(
        f"{API_URL}?key={api_key}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Gemini API error {e.code}: {detail}") from None

    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise SystemExit(f"Unexpected Gemini response shape: {json.dumps(payload)[:500]}") from exc

    result = json.loads(text)
    result["url"] = url
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze a YouTube video via Gemini (no local download)")
    ap.add_argument("url", help="YouTube video URL")
    ap.add_argument("--intent", default=None, help="What to focus the analysis on")
    args = ap.parse_args()

    api_key = load_api_key()
    result = analyze_youtube(args.url, api_key, args.intent)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
