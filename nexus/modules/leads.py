import time
from telethon.tl.custom import Message
from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty

from nexus.loader import BaseModule, module, command, watcher

BLACK_LIST = [
    'gambling', 'казино', 'casino', 'беттинг', 'ставки', '1win', 'слот', 'рулетк',
    'адалт', 'adult', '18+', 'шлюбн', 'дейтинг', 'dating', 'онлифанс', 'onlyfans',
    'стример', 'чат-оператор', 'модел', 'крипто-чат', 'арбитраж', 'обнал', 'дроп',
    'p2p связк', 'фишинг', 'фейк', 'взлом', 'чит', 'кс2', 'спам', 'рефка', 'приват'
]

DEFAULT_KEYWORDS = ["разработчик", "бот", "парсер", "скрипт", "сайт", "aiogram", "python"]

@module(
    name="Leads",
    description="Automated freelance order detector, keyword filter, and lead alert dispatcher.",
    author="txltedxgod",
    version="1.1.0"
)
class LeadsModule(BaseModule):
    async def on_load(self):
        # Initialize default keywords if empty
        if not self.get_config("keywords"):
            self.set_config("keywords", DEFAULT_KEYWORDS)

    @command(
        name="scanleads",
        description="Search recent Telegram channels and groups for live development orders.",
        usage=".scanleads [query]"
    )
    async def cmd_scanleads(self, message: Message, args: list):
        query = " ".join(args) if args else "ищу разработчик бот"
        await message.edit(f"`Scanning Telegram for freelance orders matching: '{query}'...`")

        results = []
        try:
            res = await self.client(SearchGlobalRequest(
                q=query,
                filter=InputMessagesFilterEmpty(),
                min_date=None,
                max_date=None,
                offset_rate=0,
                offset_peer=self.client.me,
                offset_id=0,
                limit=15
            ))
            
            for m in getattr(res, "messages", []):
                text = getattr(m, "message", "") or ""
                # Check blacklist
                if any(bad in text.lower() for bad in BLACK_LIST):
                    continue
                snippet = text.replace("\n", " ").strip()[:90]
                date_str = m.date.strftime("%H:%M") if m.date else ""
                results.append(f"[{date_str}] `{snippet}...`")

            if not results:
                await message.edit(self.ui.warning(f"No clean leads found for `{query}`."))
                return

            card = self.ui.list_items(
                title=f"LIVE LEADS: {query}",
                items=results[:8],
                icon="fire"
            )
            await message.edit(card)
        except Exception as e:
            await message.edit(self.ui.error(f"Lead scan error: {e}"))

    @command(
        name="addkeyword",
        description="Add a keyword to the live lead monitoring filter.",
        usage=".addkeyword <word>"
    )
    async def cmd_addkeyword(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.addkeyword <word>`"))
            return

        word = args[0].lower()
        keywords = self.get_config("keywords", DEFAULT_KEYWORDS)
        if word not in keywords:
            keywords.append(word)
            self.set_config("keywords", keywords)
            await message.edit(self.ui.success(f"Added keyword: `{word}`"))
        else:
            await message.edit(self.ui.info(f"Keyword `{word}` already present."))

    @command(
        name="delkeyword",
        description="Remove a keyword from the live lead filter.",
        usage=".delkeyword <word>"
    )
    async def cmd_delkeyword(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.delkeyword <word>`"))
            return

        word = args[0].lower()
        keywords = self.get_config("keywords", DEFAULT_KEYWORDS)
        if word in keywords:
            keywords.remove(word)
            self.set_config("keywords", keywords)
            await message.edit(self.ui.success(f"Removed keyword: `{word}`"))
        else:
            await message.edit(self.ui.warning(f"Keyword `{word}` not found."))

    @command(
        name="keywords",
        description="List active keywords and alert destination.",
        usage=".keywords"
    )
    async def cmd_keywords(self, message: Message, args: list):
        keywords = self.get_config("keywords", DEFAULT_KEYWORDS)
        dest = self.get_config("alert_target", "Saved Messages (Default)")
        kw_str = ", ".join([f"`{k}`" for k in keywords])

        card = self.ui.card(
            title="LEAD MONITOR SETTINGS",
            fields={
                "Keywords": kw_str,
                "Alert Target": dest,
                "Blacklist": f"{len(BLACK_LIST)} forbidden terms"
            },
            icon="shield"
        )
        await message.edit(card)

    @command(
        name="setalert",
        description="Set Telegram user ID/username to receive hot order alerts.",
        usage=".setalert <@username/id>"
    )
    async def cmd_setalert(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.setalert <@username/id>`"))
            return

        target = args[0]
        self.set_config("alert_target", target)
        await message.edit(self.ui.success(f"Alert notifications routed to: **{target}**"))

    @watcher(incoming=True)
    async def lead_watcher(self, message: Message):
        """Monitor incoming channel/group messages for matched keywords."""
        if not message.text:
            return

        text = message.text.lower()
        # Check blacklist
        if any(b in text for b in BLACK_LIST):
            return

        keywords = self.get_config("keywords", DEFAULT_KEYWORDS)
        matched = [k for k in keywords if k in text]
        if not matched:
            return

        alert_dest = self.get_config("alert_target")
        if not alert_dest:
            return

        sender = await message.get_sender()
        sender_title = getattr(sender, 'first_name', '') or getattr(sender, 'title', 'Unknown')
        sender_uname = f"@{sender.username}" if getattr(sender, 'username', None) else f"ID: {message.sender_id}"

        alert_text = self.ui.card(
            title="HOT LEAD DETECTED",
            fields={
                "Keywords": ", ".join(matched),
                "Source": f"{sender_title} ({sender_uname})",
                "Snippet": message.text[:180] + "..."
            },
            footer="Reply or reach out directly to close the order.",
            icon="fire"
        )
        try:
            await self.client.send_message(alert_dest, alert_text)
        except Exception:
            pass
