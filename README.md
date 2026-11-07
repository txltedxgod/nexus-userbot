# ✦ NEXUS USERBOT ✦
> **Next-Generation High-Performance Modular Telegram Userbot with Luxury Premium Emoji UI & Dynamic Hot-Reloading**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-1.36%2B-orange.svg)](https://github.com/LonamiWebs/Telethon)
[![Status: Production](https://img.shields.io/badge/Status-Production-success.svg)](#)

---

## ⚡ Key Highlights

- 🧩 **Dynamic Module Engine**: Hot-load, unload, and reload modules at runtime without dropping connections (`.load`, `.unload`, `.reload`).
- 💎 **Luxury Premium UI**: Custom Telegram Premium emoji rendering, Cyberpunk & Neon themes, structured cards, and status badges.
- 🗄️ **Persistent SQLite KV Store**: Atomic, namespaced key-value storage for per-module configuration and persistent states.
- 🚀 **Asynchronous & Non-blocking**: Fully built on `asyncio` and `telethon` for sub-millisecond command handling.
- 🛡️ **Zero Memory Leaks**: Clean watcher lifecycle, resource disposal, and graceful degradation.

---

## 🏗️ Architecture

```
nexus-userbot/
├── main.py                  # Entrypoint & signal handling
├── nexus/
│   ├── client.py            # TelegramClient wrapper & event router
│   ├── config.py            # Typed settings & environment loader
│   ├── database.py          # SQLite KV storage engine
│   ├── loader.py            # Dynamic module & watcher decorator system
│   ├── logger.py            # ANSI colored terminal logger
│   ├── ui.py                # Luxury Premium UI card formatter
│   ├── utils.py             # Helpers (shlex args, duration, byte formatters)
│   └── modules/             # Built-in & dynamic modules
│       ├── core.py          # .help, .ping, .modules, .reload, .theme
│       └── ...
└── tests/                   # Automated unit test suite
```

---

## 📦 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/txltedxgod/nexus-userbot.git
cd nexus-userbot
pip install -r requirements.txt
```

### 2. Configure Credentials
Copy `.env.example` to `.env` and fill in your API credentials from [my.telegram.org](https://my.telegram.org):
```ini
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
SESSION_NAME=nexus_userbot
DEFAULT_PREFIX=.
DEFAULT_THEME=neon_cyber
```

### 3. Launch
```bash
python main.py
```

---

## 📚 Writing Custom Modules

Creating a module is as simple as defining a class with the `@module` and `@command` decorators:

```python
from telethon.tl.custom import Message
from nexus.loader import BaseModule, module, command

@module(name="Echo", description="Simple echo module", author="txltedxgod", version="1.0.0")
class EchoModule(BaseModule):
    @command(name="echo", description="Echo text back", usage=".echo <text>")
    async def cmd_echo(self, message: Message, args: list):
        text = " ".join(args) or "Echo!"
        await message.edit(self.ui.card(title="ECHO", fields={"Text": text}, icon="zap"))
```

---

## 🛡️ License
Released under the [MIT License](LICENSE). Built with ❤️ by [@txltedxgod](https://github.com/txltedxgod).
