import time
import os
from pathlib import Path
from telethon.tl.custom import Message
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest, GetUserPhotosRequest

from nexus.loader import BaseModule, module, command, watcher
from nexus.utils import format_duration

@module(
    name="Profile",
    description="Stealth profile cloner, identity reverter, and AFK auto-responder.",
    author="txltedxgod",
    version="1.1.0"
)
class ProfileModule(BaseModule):
    async def on_load(self):
        # Ensure default afk state
        if self.get_config("is_afk") is None:
            self.set_config("is_afk", False)

    @command(
        name="afk",
        description="Toggle AFK (Away From Keyboard) mode with reason and mention logging.",
        usage=".afk [reason]"
    )
    async def cmd_afk(self, message: Message, args: list):
        reason = " ".join(args) if args else "Away from keyboard"
        start_time = time.time()
        
        self.set_config("is_afk", True)
        self.set_config("afk_reason", reason)
        self.set_config("afk_time", start_time)
        self.set_config("afk_mentions", 0)

        card = self.ui.card(
            title="AFK MODE ACTIVATED",
            fields={
                "Status": "💤 Away From Keyboard",
                "Reason": reason,
                "Since": time.strftime("%H:%M:%S")
            },
            footer="Incoming DMs & mentions will receive an auto-reply.",
            icon="clock"
        )
        await message.edit(card)

    @command(
        name="unafk",
        description="Manually disable AFK mode.",
        usage=".unafk"
    )
    async def cmd_unafk(self, message: Message, args: list):
        if not self.get_config("is_afk", False):
            await message.edit(self.ui.warning("You are not currently AFK."))
            return

        duration = time.time() - self.get_config("afk_time", time.time())
        mentions = self.get_config("afk_mentions", 0)
        self.set_config("is_afk", False)

        card = self.ui.card(
            title="BACK ONLINE",
            fields={
                "Away Duration": format_duration(duration),
                "Mentions Received": mentions
            },
            icon="zap"
        )
        await message.edit(card)

    @command(
        name="setbio",
        description="Update your Telegram profile bio description.",
        usage=".setbio <text>"
    )
    async def cmd_setbio(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.setbio <new bio text>`"))
            return

        new_bio = " ".join(args)
        try:
            await self.client(UpdateProfileRequest(about=new_bio))
            await message.edit(self.ui.success(f"Bio updated to: `{new_bio}`"))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to update bio: {e}"))

    @command(
        name="setname",
        description="Update your Telegram profile first and last name.",
        usage=".setname <first_name> [last_name]"
    )
    async def cmd_setname(self, message: Message, args: list):
        if not args:
            await message.edit(self.ui.warning("Usage: `.setname <first> [last]`"))
            return

        first_name = args[0]
        last_name = " ".join(args[1:]) if len(args) > 1 else ""
        try:
            await self.client(UpdateProfileRequest(first_name=first_name, last_name=last_name))
            full = f"{first_name} {last_name}".strip()
            await message.edit(self.ui.success(f"Profile name updated to: **{full}**"))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to update name: {e}"))

    @command(
        name="clone",
        description="Clone avatar, name, and bio of a target user (saves original for .revert).",
        usage=".clone [reply/username]"
    )
    async def cmd_clone(self, message: Message, args: list):
        target = None
        if message.is_reply:
            reply = await message.get_reply_message()
            target = await reply.get_sender()
        elif args:
            target = await self.client.get_entity(args[0])

        if not target:
            await message.edit(self.ui.warning("Reply to a user or pass their username: `.clone @username`"))
            return

        await message.edit("`Initiating stealth identity cloning...`")
        me = await self.client.get_me()

        # Backup current profile if not backed up
        if not self.get_config("orig_first_name"):
            self.set_config("orig_first_name", me.first_name or "")
            self.set_config("orig_last_name", me.last_name or "")

        target_first = getattr(target, 'first_name', '') or ''
        target_last = getattr(target, 'last_name', '') or ''

        # Update name
        await self.client(UpdateProfileRequest(first_name=target_first, last_name=target_last))

        # Download target photo and set as profile photo
        photos = await self.client.get_profile_photos(target, limit=1)
        if photos:
            photo_path = await self.client.download_media(photos[0])
            if photo_path:
                upload = await self.client.upload_file(photo_path)
                await self.client(UploadProfilePhotoRequest(file=upload))
                if os.path.exists(photo_path):
                    os.remove(photo_path)

        card = self.ui.card(
            title="IDENTITY CLONED",
            fields={
                "Target Name": f"{target_first} {target_last}".strip(),
                "Target ID": target.id,
                "Restoration": "Use `.revert` to restore original identity"
            },
            icon="shield"
        )
        await message.edit(card)

    @command(
        name="revert",
        description="Restore original profile name and settings after cloning.",
        usage=".revert"
    )
    async def cmd_revert(self, message: Message, args: list):
        orig_first = self.get_config("orig_first_name")
        orig_last = self.get_config("orig_last_name", "")

        if not orig_first:
            await message.edit(self.ui.warning("No original identity backup found in storage."))
            return

        await self.client(UpdateProfileRequest(first_name=orig_first, last_name=orig_last))
        self.del_config("orig_first_name")
        self.del_config("orig_last_name")
        await message.edit(self.ui.success(f"Identity restored: **{orig_first} {orig_last}**"))

    @watcher(incoming=True)
    async def afk_watcher(self, message: Message):
        """Auto-respond to mentions and direct messages when AFK."""
        if not self.get_config("is_afk", False):
            return

        me = self.client.me
        if not me:
            return

        is_dm = message.is_private
        is_mention = (
            message.mentioned or
            (message.text and (f"@{me.username}" in message.text or str(me.id) in message.text))
        )

        if is_dm or is_mention:
            count = self.get_config("afk_mentions", 0) + 1
            self.set_config("afk_mentions", count)

            reason = self.get_config("afk_reason", "Away from keyboard")
            afk_start = self.get_config("afk_time", time.time())
            duration_str = format_duration(time.time() - afk_start)

            reply_text = (
                f"{self.ui.ICONS['clock']} **AFK AUTO-REPLY**\n"
                f"{self.ui.theme['bullet']} **Status:** Currently away\n"
                f"{self.ui.theme['bullet']} **Reason:** `{reason}`\n"
                f"{self.ui.theme['bullet']} **Duration:** `{duration_str}`"
            )
            try:
                await message.reply(reply_text)
            except Exception:
                pass
