"""Utility helpers: slug generation, title extraction, formatting."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from typing import List, Optional, Tuple


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text or "untitled"


def extract_title_from_filename(filename: str) -> str:
    """Extract a human-readable title from a filename."""
    # Remove extension
    name = re.sub(r"\.[^.]+$", "", filename)
    # Replace dots, underscores with spaces
    name = re.sub(r"[._]+", " ", name)
    # Remove common noise patterns (year in brackets, resolution tags)
    name = re.sub(r"\[.*?\]|\(.*?\)", "", name)
    # Remove resolution tags like 1080p, 720p, 4K
    name = re.sub(r"\b(1080|720|480|2160|4K)[piP]\b", "", name, flags=re.IGNORECASE)
    # Remove codec tags
    name = re.sub(r"\b(x264|x265|h264|h265|hevc|aac|mp3|webrip|bluray|web-dl)\b", "", name, flags=re.IGNORECASE)
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    # Title case
    if name:
        name = name[0].upper() + name[1:]
    return name or filename


def guess_category(filename: str, mime_type: str = "") -> str:
    """Guess a category from filename and mime type."""
    fn_lower = filename.lower()
    mt_lower = mime_type.lower()

    if "anime" in fn_lower:
        return "Anime"
    if "documentary" in fn_lower or "doc" in fn_lower:
        return "Documentary"
    if "series" in fn_lower or "s01" in fn_lower or "s02" in fn_lower or re.search(r"\bs\d{2}e\d{2}\b", fn_lower, re.IGNORECASE):
        return "TV Series"
    if "movie" in fn_lower or "film" in fn_lower:
        return "Movies"
    if mt_lower.startswith("audio/") or "music" in fn_lower or "mp3" in fn_lower:
        return "Music"
    if mt_lower.startswith("video/"):
        return "Movies"
    return "Uncategorized"


def extract_tags(filename: str, caption: str = "") -> List[str]:
    """Extract tags from filename and caption."""
    tags: List[str] = []
    combined = f"{filename} {caption}".lower()

    quality_patterns = ["4k", "1080p", "720p", "480p", "hd", "uhd", "bluray", "web-dl", "webrip"]
    for q in quality_patterns:
        if q in combined:
            tags.append(q)

    codec_patterns = ["x264", "x265", "h264", "h265", "hevc", "aac", "mp3", "dts"]
    for c in codec_patterns:
        if c in combined:
            tags.append(c)

    # Extract year
    years = re.findall(r"\b(19\d{2}|20[0-2]\d)\b", combined)
    for y in years:
        if y not in tags:
            tags.append(y)

    return list(set(tags))[:10]


def format_duration(seconds: int) -> str:
    """Format seconds into H:MM:SS or M:SS."""
    if seconds <= 0:
        return "0:00"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_file_size(size_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if size_bytes <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    idx = 0
    size = float(size_bytes)
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    if idx == 0:
        return f"{int(size)} {units[idx]}"
    return f"{size:.1f} {units[idx]}"


def parse_range_header(range_header: str, file_size: int) -> Tuple[int, int]:
    """Parse an HTTP Range header. Returns (start, end) byte positions.

    If no Range header or invalid, returns (0, file_size - 1).
    """
    if not range_header:
        return 0, file_size - 1

    m = re.match(r"bytes=(\d*)-(\d*)", range_header)
    if not m:
        return 0, file_size - 1

    start_str, end_str = m.group(1), m.group(2)

    if start_str == "" and end_str == "":
        return 0, file_size - 1

    if start_str == "":
        # Suffix range: last N bytes
        suffix = int(end_str)
        start = max(0, file_size - suffix)
        end = file_size - 1
    else:
        start = int(start_str)
        end = int(end_str) if end_str else file_size - 1

    if start >= file_size:
        raise ValueError("Range start exceeds file size")

    end = min(end, file_size - 1)
    return start, end


def build_content_range(start: int, end: int, total: int) -> str:
    """Build a Content-Range header value."""
    return f"bytes {start}-{end}/{total}"