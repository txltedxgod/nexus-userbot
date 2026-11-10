## 📦 Built-in Modules & Command Matrix

| Module | Commands | Description |
| :--- | :--- | :--- |
| **Admin** (`admin.py`) | `purge`, `del`, `pin`, `unpin`, `user`, `id` | High-speed message purge, pin/unpin, user inspection, and moderation suite. |
| **AIAssistant** (`ai_assistant.py`) | `ai`, `summary`, `pitch_ai` | Neural AI prompt assistant, chat thread summarizer, and automated pitch generator. |
| **Core** (`core.py`) | `ping`, `help`, `modules`, `prefix`, `theme`, `reload` | Core management system, module loader, and latency diagnostics. |
| **Crypto** (`crypto.py`) | `p`, `qr`, `gas` | Live cryptocurrency prices, QR code payment generator, and blockchain gas tracker. |
| **Downloader** (`downloader.py`) | `dem`, `dl` | Universal media downloader (TikTok/Reels/Shorts) and instant demotivator meme generator. |
| **Leads** (`leads.py`) | `scanleads`, `addkeyword`, `delkeyword`, `keywords`, `setalert` | Automated freelance order detector, keyword filter, and lead alert dispatcher. |
| **Media** (`media.py`) | `circle`, `voice`, `mediainfo` | Video to circular note converter, voice synthesizer, and metadata inspector. |
| **Profile** (`profile.py`) | `afk`, `unafk`, `setbio`, `setname`, `clone`, `revert` | Stealth profile cloner, identity reverter, and AFK auto-responder. |
| **Reactions** (`reactions.py`) | `autoreact`, `delreact`, `reacts`, `flex` | Automated user reaction watcher, emoji sniper, and visual flex animations. |
| **Stealth** (`stealth.py`) | `dmmute`, `undmmute`, `dmmuted`, `antidel` | DM blackhole mute (auto-delete incoming messages), ghost mode, and anti-delete logger. |
| **Terminal** (`terminal.py`) | `eval`, `exec`, `sh`, `sys` | Developer power tools: async eval/exec, shell terminal, and hardware diagnostics. |
| **Text** (`text.py`) | `type`, `paste`, `hide`, `translit`, `quote` | Animated typewriter, text formatting, transliteration, and pastebin uploader. |
| **Theme** (`theme.py`) | `settheme`, `setemoji`, `emojipack`, `carddemo` | Luxury theme manager, custom emoji palette configurer, and visual showcase. |


### Admin (`nexus/modules/admin.py`)
> High-speed message purge, pin/unpin, user inspection, and moderation suite.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.purge` | `.purge [limit]` | Fast bulk message deletion from replied message down to latest or N messages. |
| `.del` | `.del` | Delete replied message immediately. |
| `.pin` | `.pin [loud]` | Pin replied message (silently or with notification). |
| `.unpin` | `.unpin` | Unpin replied or current chat pinned message. |
| `.user` | `.user [reply/username/id]` | Inspect detailed Telegram user metadata. |
| `.id` | `.id` | Display chat and sender Telegram IDs. |

### AIAssistant (`nexus/modules/ai_assistant.py`)
> Neural AI prompt assistant, chat thread summarizer, and automated pitch generator.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.ai` | `.ai <prompt or reply>` | Query neural AI assistant directly in chat or reply to a message. |
| `.summary` | `.summary [limit=30]` | Summarize the last N messages in the chat into key takeaways. |
| `.pitch_ai` | `.pitch_ai [reply to order]` | Generate a tailored, high-converting freelance pitch in reply to a client order. |

### Core (`nexus/modules/core.py`)
> Core management system, module loader, and latency diagnostics.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.ping` | `.ping` | Check userbot round-trip latency to Telegram servers. |
| `.help` | `.help [module/command]` | Display help menu for all loaded modules or a specific command. |
| `.modules` | `.modules` | List all active modules with metadata. |
| `.prefix` | `.prefix <new_prefix>` | Change userbot command prefix dynamically. |
| `.theme` | `.theme [neon_cyber|luxury_gold|minimal]` | Switch luxury visual theme (neon_cyber, luxury_gold, minimal). |
| `.reload` | `.reload <module_name>` | Hot-reload a module from disk without restarting userbot. |

### Crypto (`nexus/modules/crypto.py`)
> Live cryptocurrency prices, QR code payment generator, and blockchain gas tracker.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.p` | `.p <btc/ton/sol/eth/usdt>` | Query live crypto price and 24h percentage change. |
| `.qr` | `.qr <wallet_address/text>` | Generate a scannable QR code for a crypto wallet address, card or payment link. |
| `.gas` | `.gas` | Check current network transaction gas fees. |

### Downloader (`nexus/modules/downloader.py`)
> Universal media downloader (TikTok/Reels/Shorts) and instant demotivator meme generator.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.dem` | `.dem <top text> [| <bottom text>]` | Generate a classic demotivator meme from a replied photo. |
| `.dl` | `.dl <video_url>` | Download clean video without watermarks from TikTok, Reels, Shorts, Twitter/X. |

### Leads (`nexus/modules/leads.py`)
> Automated freelance order detector, keyword filter, and lead alert dispatcher.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.scanleads` | `.scanleads [query]` | Search recent Telegram channels and groups for live development orders. |
| `.addkeyword` | `.addkeyword <word>` | Add a keyword to the live lead monitoring filter. |
| `.delkeyword` | `.delkeyword <word>` | Remove a keyword from the live lead filter. |
| `.keywords` | `.keywords` | List active keywords and alert destination. |
| `.setalert` | `.setalert <@username/id>` | Set Telegram user ID/username to receive hot order alerts. |

### Media (`nexus/modules/media.py`)
> Video to circular note converter, voice synthesizer, and metadata inspector.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.circle` | `.circle [reply to video]` | Convert a rectangular video into a circular Telegram video note. |
| `.voice` | `.voice [reply to audio/video]` | Convert audio or video file into a Telegram voice message with waveform. |
| `.mediainfo` | `.mediainfo [reply to media]` | Inspect technical metadata of replied media file. |

### Profile (`nexus/modules/profile.py`)
> Stealth profile cloner, identity reverter, and AFK auto-responder.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.afk` | `.afk [reason]` | Toggle AFK (Away From Keyboard) mode with reason and mention logging. |
| `.unafk` | `.unafk` | Manually disable AFK mode. |
| `.setbio` | `.setbio <text>` | Update your Telegram profile bio description. |
| `.setname` | `.setname <first_name> [last_name]` | Update your Telegram profile first and last name. |
| `.clone` | `.clone [reply/username]` | Clone avatar, name, and bio of a target user (saves original for .revert). |
| `.revert` | `.revert` | Restore original profile name and settings after cloning. |

### Reactions (`nexus/modules/reactions.py`)
> Automated user reaction watcher, emoji sniper, and visual flex animations.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.autoreact` | `.autoreact <@user/id> <emoji>` | Bind an automatic reaction to every message sent by a specific user. |
| `.delreact` | `.delreact <@user/id>` | Remove automated reaction rule for a user. |
| `.reacts` | `.reacts` | List all active auto-reaction rules. |
| `.flex` | `.flex` | Animate an emoji progression flex in the current message. |

### Stealth (`nexus/modules/stealth.py`)
> DM blackhole mute (auto-delete incoming messages), ghost mode, and anti-delete logger.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.dmmute` | `.dmmute [reply/username/id]` | Mute user in direct messages: any incoming message from them is silently deleted on arrival. |
| `.undmmute` | `.undmmute [reply/username/id]` | Unmute user from DM blackhole list. |
| `.dmmuted` | `.dmmuted` | List all users currently muted in DMs. |
| `.antidel` | `.antidel [on/off]` | Toggle anti-delete logger (logs deleted messages to Saved Messages). |

### Terminal (`nexus/modules/terminal.py`)
> Developer power tools: async eval/exec, shell terminal, and hardware diagnostics.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.eval` | `.eval <python expression>` | Evaluate an async Python expression with execution latency. |
| `.exec` | `.exec <python code>` | Execute arbitrary Python code block capturing stdout & stderr. |
| `.sh` | `.sh <command>` | Execute a shell terminal command asynchronously. |
| `.sys` | `.sys` | Display hardware and host operating system statistics. |

### Text (`nexus/modules/text.py`)
> Animated typewriter, text formatting, transliteration, and pastebin uploader.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.type` | `.type <text to type>` | Simulate realistic animated typewriter effect with blinking cursor. |
| `.paste` | `.paste [text/reply]` | Upload text or code snippet to Hastebin/Spacebin and get a shareable link. |
| `.hide` | `.hide <text>` | Wrap text into Telegram spoiler tags. |
| `.translit` | `.translit [text/reply]` | Switch text layout between Russian and English. |
| `.quote` | `.quote [text/reply]` | Format text or replied message into a luxury quoted block. |

### Theme (`nexus/modules/theme.py`)
> Luxury theme manager, custom emoji palette configurer, and visual showcase.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.settheme` | `.settheme <name>` | Switch luxury visual theme preset. |
| `.setemoji` | `.setemoji <slot> <emoji>` | Assign a custom emoji or character to a UI icon slot. |
| `.emojipack` | `.emojipack` | Display active custom emoji palette and icon mappings. |
| `.carddemo` | `.carddemo` | Render a luxury UI card showcase demonstrating current aesthetics. |