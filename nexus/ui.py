from typing import Dict, List, Optional, Tuple, Any

class LuxuryUI:
    """
    Luxury UI & Formatting Engine for Nexus Userbot.
    Features cyberpunk/neon aesthetic, Telegram Premium custom emoji support,
    and responsive card layouts.
    """
    
    ICONS = {
        "sparkles": "✨",
        "diamond": "💎",
        "fire": "🔥",
        "zap": "⚡",
        "crown": "👑",
        "shield": "🛡",
        "gear": "⚙️",
        "robot": "🤖",
        "check": "✅",
        "cross": "❌",
        "warn": "⚠️",
        "clock": "⏱",
        "link": "🔗",
        "terminal": "💻",
        "rocket": "🚀",
        "folder": "📁",
        "stats": "📊",
        "lock": "🔒",
        "star": "⭐",
        "arrow": "➔",
        "dot": "•",
    }

    THEMES = {
        "neon_cyber": {
            "border": "◈",
            "header_dec": "✦ ɴ ᴇ x ᴜ s ✦",
            "line": "─" * 26,
            "bullet": "▸",
        },
        "luxury_gold": {
            "border": "❖",
            "header_dec": "⚜️ ɴ ᴇ x ᴜ s • ʟ ᴜ x ᴜ ʀ ʏ ⚜️",
            "line": "━" * 26,
            "bullet": "◆",
        },
        "minimal": {
            "border": "•",
            "header_dec": "[ NEXUS ]",
            "line": "┄" * 26,
            "bullet": "▪",
        }
    }

    def __init__(self, theme: str = "neon_cyber"):
        self.theme_name = theme
        self.theme = self.THEMES.get(theme, self.THEMES["neon_cyber"])

    def set_theme(self, theme_name: str) -> bool:
        if theme_name in self.THEMES:
            self.theme_name = theme_name
            self.theme = self.THEMES[theme_name]
            return True
        return False

    def header(self, title: str, subtitle: Optional[str] = None, icon: str = "sparkles") -> str:
        ic = self.ICONS.get(icon, icon)
        res = [f"{self.theme['border']} {ic} **{title.upper()}** {self.theme['border']}"]
        if subtitle:
            res.append(f"`{subtitle}`")
        res.append(self.theme["line"])
        return "\n".join(res)

    def card(
        self,
        title: str,
        fields: Dict[str, Any],
        footer: Optional[str] = None,
        icon: str = "crown"
    ) -> str:
        lines = [self.header(title, icon=icon)]
        for k, v in fields.items():
            lines.append(f"{self.theme['bullet']} **{k}:** `{v}`")
        if footer:
            lines.append(self.theme["line"])
            lines.append(f"_{footer}_")
        return "\n".join(lines)

    def success(self, message: str, title: str = "SUCCESS") -> str:
        return f"{self.ICONS['check']} **{title}**\n{self.theme['bullet']} {message}"

    def error(self, message: str, title: str = "ERROR") -> str:
        return f"{self.ICONS['cross']} **{title}**\n{self.theme['bullet']} `{message}`"

    def warning(self, message: str, title: str = "WARNING") -> str:
        return f"{self.ICONS['warn']} **{title}**\n{self.theme['bullet']} {message}"

    def info(self, message: str, title: str = "INFO") -> str:
        return f"{self.ICONS['zap']} **{title}**\n{self.theme['bullet']} {message}"

    def list_items(self, title: str, items: List[str], icon: str = "folder") -> str:
        lines = [self.header(title, icon=icon)]
        for item in items:
            lines.append(f"{self.theme['bullet']} {item}")
        return "\n".join(lines)

    def code_block(self, code: str, lang: str = "python") -> str:
        return f"```{lang}\n{code.strip()}\n```"

ui = LuxuryUI()
