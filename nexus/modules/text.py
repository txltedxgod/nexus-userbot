import asyncio
import random
import aiohttp
from telethon.tl.custom import Message

from nexus.loader import BaseModule, module, command

RU_EN = {
    'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
    'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's',
    'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
    'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
    'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', '.': '/'
}
EN_RU = {v: k for k, v in RU_EN.items()}

@module(
    name="Text",
    description="Animated typewriter, text formatting, transliteration, and pastebin uploader.",
    author="txltedxgod",
    version="1.1.0"
)
class TextModule(BaseModule):
    @command(
        name="type",
        description="Simulate realistic animated typewriter effect with blinking cursor.",
        usage=".type <text to type>"
    )
    async def cmd_type(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.type <text to type>`"))
            return

        text = " ".join(args)
        current = ""
        cursor = "▌"
        
        # Animate characters with pacing
        for char in text:
            current += char
            try:
                await message.edit(f"`{current}{cursor}`")
                await asyncio.sleep(random.uniform(0.04, 0.09))
            except Exception:
                pass
        
        # Remove cursor at completion
        try:
            await message.edit(f"`{current}`")
        except Exception:
            pass

    @command(
        name="paste",
        description="Upload text or code snippet to Hastebin/Spacebin and get a shareable link.",
        usage=".paste [text/reply]"
    )
    async def cmd_paste(self, message: Message, args: list):
        content = ""
        if message.is_reply:
            reply = await message.get_reply_message()
            content = reply.text or ""
        elif args:
            content = " ".join(args)

        if not content:
            await message.edit(self.ui.warning("Reply to a message with text or supply text: `.paste <code/text>`"))
            return

        await message.edit("`Uploading to pastebin...`")
        
        url = "https://hastebin.com/documents"
        headers = {"User-Agent": "NexusUserbot/1.0"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=content.encode("utf-8"), headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        key = data.get("key")
                        raw_url = f"https://hastebin.com/{key}"
                        card = self.ui.card(
                            title="PASTE CREATED",
                            fields={
                                "Service": "Hastebin",
                                "Characters": len(content),
                                "Direct URL": raw_url
                            },
                            icon="link"
                        )
                        await message.edit(card)
                        return
                    else:
                        raise Exception(f"HTTP {resp.status}")
        except Exception as e:
            # Fallback to local snippet
            await message.edit(self.ui.error(f"Failed to upload paste: {e}"))

    @command(
        name="hide",
        description="Wrap text into Telegram spoiler tags.",
        usage=".hide <text>"
    )
    async def cmd_hide(self, message: Message, args: list):
        text = " ".join(args)
        if not text and message.is_reply:
            reply = await message.get_reply_message()
            text = reply.text or ""

        if not text:
            await message.edit(self.ui.warning("Usage: `.hide <text>`"))
            return

        await message.edit(f"||{text}||")

    @command(
        name="translit",
        description="Switch text layout between Russian and English.",
        usage=".translit [text/reply]"
    )
    async def cmd_translit(self, message: Message, args: list):
        text = " ".join(args)
        if not text and message.is_reply:
            reply = await message.get_reply_message()
            text = reply.text or ""

        if not text:
            await message.edit(self.ui.warning("Usage: `.translit <text>`"))
            return

        # Determine dominant language
        ru_count = sum(1 for c in text.lower() if c in RU_EN)
        en_count = sum(1 for c in text.lower() if c in EN_RU)

        mapping = RU_EN if ru_count >= en_count else EN_RU
        result = []
        for c in text:
            low = c.lower()
            if low in mapping:
                replaced = mapping[low]
                result.append(replaced.upper() if c.isupper() else replaced)
            else:
                result.append(c)

        await message.edit("".join(result))

    @command(
        name="quote",
        description="Format text or replied message into a luxury quoted block.",
        usage=".quote [text/reply]"
    )
    async def cmd_quote(self, message: Message, args: list):
        author = "Anonymous"
        quote_text = ""
        
        if message.is_reply:
            reply = await message.get_reply_message()
            sender = await reply.get_sender()
            author = getattr(sender, 'first_name', 'User') if sender else "User"
            quote_text = reply.text or ""
        elif args:
            quote_text = " ".join(args)
            author = self.client.me.first_name if self.client.me else "Me"

        if not quote_text:
            await message.edit(self.ui.warning("No quote content found."))
            return

        quoted = (
            f"❝\n"
            f"{quote_text}\n"
            f"❞ — **{author}**"
        )
        await message.edit(quoted)
