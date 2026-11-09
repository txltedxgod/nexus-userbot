import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

@dataclass
class Config:
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    SESSION_NAME: str = os.getenv("SESSION_NAME", "nexus_userbot")
    DEFAULT_PREFIX: str = os.getenv("DEFAULT_PREFIX", ".")
    DATABASE_PATH: Path = BASE_DIR / "nexus_data.sqlite"
    MODULES_DIR: Path = BASE_DIR / "nexus" / "modules"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Premium UI settings
    PREMIUM_MODE: bool = os.getenv("PREMIUM_MODE", "true").lower() in ("true", "1", "yes")
    DEFAULT_THEME: str = os.getenv("DEFAULT_THEME", "neon_cyber")

    # AyuGram & Desktop Client Compatibility (prevents session kicks on PC)
    DEVICE_MODEL: str = os.getenv("DEVICE_MODEL", "AyuGram Desktop")
    SYSTEM_VERSION: str = os.getenv("SYSTEM_VERSION", "Windows 11 x64")
    APP_VERSION: str = os.getenv("APP_VERSION", "5.12.2 x64")
    LANG_CODE: str = os.getenv("LANG_CODE", "en")
    SYSTEM_LANG_CODE: str = os.getenv("SYSTEM_LANG_CODE", "en")

config = Config()
