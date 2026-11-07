import time
from pathlib import Path
from telethon.tl.custom import Message

from nexus.loader import BaseModule, module, command
from nexus.utils import format_duration
from nexus.config import config

@module(
    name="Core",
    description="Core management system, module loader, and latency diagnostics.",
    author="txltedxgod",
    version="1.0.0"
)
class CoreModule(BaseModule):
    @command(
        name="ping",
        description="Check userbot round-trip latency to Telegram servers.",
        usage=".ping"
    )
    async def cmd_ping(self, message: Message, args: list):
        start = time.perf_counter()
        await message.edit("`Pinging Telegram servers...`")
        end = time.perf_counter()
        latency_ms = (end - start) * 1000

        # Latency grade indicator
        if latency_ms < 60:
            badge = "🚀 Ultra Fast"
            icon = "zap"
        elif latency_ms < 150:
            badge = "⚡ Normal"
            icon = "sparkles"
        else:
            badge = "🐢 High"
            icon = "warn"

        uptime_str = format_duration(time.time() - self.client.start_time)
        res = self.ui.card(
            title="PONG",
            fields={
                "Latency": f"{latency_ms:.2f} ms ({badge})",
                "Uptime": uptime_str,
                "Prefix": self.client.prefix,
                "Active Modules": len(self.client.modules.modules)
            },
            icon=icon
        )
        await message.edit(res)

    @command(
        name="help",
        description="Display help menu for all loaded modules or a specific command.",
        usage=".help [module/command]"
    )
    async def cmd_help(self, message: Message, args: list):
        if not args:
            # Show list of all modules
            lines = [self.ui.header("Nexus Command Center", subtitle="Modular Telethon Engine", icon="crown")]
            for mod_name, mod in sorted(self.client.modules.modules.items()):
                cmds = ", ".join([f"`{c}`" for c in sorted(mod._commands.keys())]) or "_No commands_"
                lines.append(f"📦 **{mod.name}** `v{mod.version}`\n   ↳ {cmds}")
            lines.append(self.ui.theme["line"])
            lines.append(f"💡 _Use `{self.client.prefix}help <command>` for detailed command syntax._")
            await message.edit("\n".join(lines))
            return

        query = args[0].lower().lstrip(self.client.prefix)
        # Check if it's a command
        if query in self.client.modules.commands:
            meta = self.client.modules.commands[query]
            fields = {
                "Command": f"`{self.client.prefix}{meta.name}`",
                "Module": f"`{meta.module_name}`",
                "Description": meta.description,
                "Usage": f"`{meta.usage}`",
                "Aliases": ", ".join([f"`{a}`" for a in meta.aliases]) if meta.aliases else "None"
            }
            await message.edit(self.ui.card(title=f"Command: {meta.name}", fields=fields, icon="terminal"))
            return

        # Check if it's a module
        if query in self.client.modules.modules:
            mod = self.client.modules.modules[query]
            cmd_list = [f"`{self.client.prefix}{c}` - {meta.description}" for c, meta in mod._commands.items()]
            res = self.ui.list_items(
                title=f"Module: {mod.name} v{mod.version}",
                items=cmd_list or ["No commands registered."],
                icon="folder"
            )
            await message.edit(res)
            return

        await message.edit(self.ui.error(f"Unknown module or command: `{query}`"))

    @command(
        name="modules",
        description="List all active modules with metadata.",
        usage=".modules"
    )
    async def cmd_modules(self, message: Message, args: list):
        items = []
        for name, mod in sorted(self.client.modules.modules.items()):
            items.append(f"**{mod.name}** (`v{mod.version}`) - {mod.description} [by @{mod.author}]")
        await message.edit(self.ui.list_items("Active Modules Registry", items, icon="folder"))

    @command(
        name="prefix",
        description="Change userbot command prefix dynamically.",
        usage=".prefix <new_prefix>"
    )
    async def cmd_prefix(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning(f"Current prefix: `{self.client.prefix}`\nUsage: `.prefix <new_prefix>`"))
            return
        new_prefix = args[0]
        self.client.set_prefix(new_prefix)
        await message.edit(self.ui.success(f"Command prefix updated to: `{new_prefix}`"))

    @command(
        name="theme",
        description="Switch luxury visual theme (neon_cyber, luxury_gold, minimal).",
        usage=".theme [neon_cyber|luxury_gold|minimal]"
    )
    async def cmd_theme(self, message: Message, args: list):
        if not args:
            themes_avail = ", ".join([f"`{t}`" for t in self.ui.THEMES.keys()])
            await message.edit(self.ui.info(f"Current theme: `{self.ui.theme_name}`\nAvailable: {themes_avail}"))
            return
        target = args[0].lower()
        if self.ui.set_theme(target):
            self.set_config("theme", target)
            await message.edit(self.ui.success(f"Visual theme switched to: **{target}**"))
        else:
            await message.edit(self.ui.error(f"Invalid theme. Choose from: {list(self.ui.THEMES.keys())}"))

    @command(
        name="reload",
        description="Hot-reload a module from disk without restarting userbot.",
        usage=".reload <module_name>"
    )
    async def cmd_reload(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.reload <module_name>`"))
            return
        target = args[0].lower()
        file_path = config.MODULES_DIR / f"{target}.py"
        if not file_path.exists():
            await message.edit(self.ui.error(f"Module file not found: `{file_path.name}`"))
            return
        
        self.client.modules.unregister_module(target)
        loaded = self.client.modules.load_module_from_file(file_path)
        if loaded:
            await message.edit(self.ui.success(f"Module `{loaded.name}` successfully hot-reloaded!"))
        else:
            await message.edit(self.ui.error(f"Failed to reload module `{target}`."))
