import logging
import sys
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[90m',     # Dark grey
        'INFO': '\033[94m',      # Blue
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        prefix = f"{self.CYAN}[NEXUS]{self.RESET} {self.BOLD}{timestamp}{self.RESET}"
        level = f"{color}[{record.levelname:<7}]{self.RESET}"
        name = f"\033[92m[{record.name}]{self.RESET}"
        msg = f"{color}{record.getMessage()}{self.RESET}"
        return f"{prefix} {level} {name} {msg}"

def get_logger(name: str = "core") -> logging.Logger:
    logger = logging.getLogger(f"nexus.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
