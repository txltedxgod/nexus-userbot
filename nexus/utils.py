import shlex
import time
from typing import List, Optional, Tuple, Any

def parse_args(text: str) -> List[str]:
    """Safely split command arguments supporting quotes."""
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()

def format_duration(seconds: float) -> str:
    """Format duration into human-readable string (e.g. 2d 5h 32m 14s)."""
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts)

def format_bytes(size: float) -> str:
    """Format byte sizes into human readable units."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size) < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def progress_bar(current: int, total: int, length: int = 12) -> str:
    """Generate a clean visual progress bar."""
    if total <= 0:
        return "▱" * length
    fraction = min(1.0, current / total)
    filled = int(fraction * length)
    empty = length - filled
    percent = int(fraction * 100)
    return f"{'▰' * filled}{'▱' * empty} {percent}%"
