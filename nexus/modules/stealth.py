import time
from telethon.tl.custom import Message
from telethon import events

from nexus.loader import BaseModule, module, command, watcher

@module(
    name="Stealth",
    description="DM blackhole mute (auto-delete incoming messages), ghost mode, and anti-delete logger.",
    author="txltedxgod",
    version="1.2.0"
)
class StealthModule(BaseModule):
    def __init__(self, client, db):
        super().__init__(client, db)
        # In-memory message cache for anti-delete tracking (id -> message_dict)
        self.message_cache = {}

    async def on_load(self):
        if self.get_config("dmmuted") is None:
            self.set_config("dmmuted", [])
        if self.get_config("antidel_enabled") is None:
            self.set_config("antidel_enabled", True)

    @command(
        name="dmmute",
        description="Mute user in direct messages: any incoming message from them is silently deleted on arrival.",
        usage=".dmmute [reply/username/id]"
    )
    async def cmd_dmmute(self, message: Message, args: list):
        target = None
        if message.is_reply:
            reply = await message.get_reply_message()
            target = await reply.get_sender()
        elif args:
            try:
                target = await self.client.get_entity(args[0] if not args[0].isdigit() else int(args[0]))
            except Exception as e:
                await message.edit(self.ui.error(f"Cannot resolve user: {e}"))
                return
        elif message.is_private:
            target = await message.get_chat()

        if not target:
            await message.edit(self.ui.warning("Specify a target user: `.dmmute @username` or reply."))
            return

        muted_list = self.get_config("dmmuted", [])
        target_id = target.id
        uname = getattr(target, 'username', 'no_username')

        if target_id not in muted_list:
            muted_list.append(target_id)
            self.set_config("dmmuted", muted_list)
            card = self.ui.card(
                title="DM BLACKHOLE MUTE",
                fields={
                    "Status": "🌑 Active (Auto-Delete)",
                    "Target ID": target_id,
                    "Username": f"@{uname}" if uname else "None",
                    "Effect": "All incoming DMs from this user will be instantly vaporized."
                },
                icon="shield"
            )
            await message.edit(card)
        else:
            await message.edit(self.ui.info(f"User `{target_id}` is already blackhole-muted."))

    @command(
        name="undmmute",
        description="Unmute user from DM blackhole list.",
        usage=".undmmute [reply/username/id]"
    )
    async def cmd_undmmute(self, message: Message, args: list):
        target = None
        if message.is_reply:
            reply = await message.get_reply_message()
            target = await reply.get_sender()
        elif args:
            try:
                target = await self.client.get_entity(args[0] if not args[0].isdigit() else int(args[0]))
            except Exception as e:
                await message.edit(self.ui.error(f"Cannot resolve user: {e}"))
                return
        elif message.is_private:
            target = await message.get_chat()

        if not target:
            await message.edit(self.ui.warning("Specify user: `.undmmute @username` or reply."))
            return

        muted_list = self.get_config("dmmuted", [])
        target_id = target.id

        if target_id in muted_list:
            muted_list.remove(target_id)
            self.set_config("dmmuted", muted_list)
            await message.edit(self.ui.success(f"User `{target_id}` removed from DM blackhole mute."))
        else:
            await message.edit(self.ui.warning(f"User `{target_id}` was not muted."))

    @command(
        name="dmmuted",
        description="List all users currently muted in DMs.",
        usage=".dmmuted"
    )
    async def cmd_dmmuted(self, message: Message, args: list):
        muted_list = self.get_config("dmmuted", [])
        if not muted_list:
            await message.edit(self.ui.info("No users are currently blackhole-muted in DMs."))
            return

        items = [f"User ID: `{uid}` (Blackholed)" for uid in muted_list]
        card = self.ui.list_items("BLACKHOLE MUTED USERS", items, icon="lock")
        await message.edit(card)

    @command(
        name="antidel",
        description="Toggle anti-delete logger (logs deleted messages to Saved Messages).",
        usage=".antidel [on/off]"
    )
    async def cmd_antidel(self, message: Message, args: list):
        if not args:
            curr = self.get_config("antidel_enabled", True)
            await message.edit(self.ui.info(f"Anti-Delete Logger: **{'ENABLED' if curr else 'DISABLED'}**\nUsage: `.antidel on/off`"))
            return

        state = args[0].lower() in ("on", "1", "true", "enable")
        self.set_config("antidel_enabled", state)
        await message.edit(self.ui.success(f"Anti-Delete Logger set to: **{'ENABLED' if state else 'DISABLED'}**"))

    @watcher(incoming=True)
    async def dm_mute_and_cache_watcher(self, message: Message):
        """Silently intercept messages: auto-delete from muted users and cache for anti-delete."""
        sender_id = message.sender_id
        is_dm = message.is_private

        # 1. Check DM blackhole mute
        muted_list = self.get_config("dmmuted", [])
        if is_dm and sender_id in muted_list:
            try:
                await message.delete()
                self.logger.info(f"Vaporized incoming DM from blackholed user ID: {sender_id}")
                return
            except Exception as e:
                self.logger.error(f"Failed to auto-delete DM from {sender_id}: {e}")

        # 2. Cache incoming message for anti-delete if enabled
        if self.get_config("antidel_enabled", True) and message.id:
            sender = await message.get_sender()
            first = getattr(sender, 'first_name', 'User') if sender else "User"
            uname = getattr(sender, 'username', None)
            
            self.message_cache[message.id] = {
                "text": message.text or "[media/non-text]",
                "sender": f"{first} (@{uname})" if uname else first,
                "sender_id": sender_id,
                "chat_id": message.chat_id,
                "date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            # Limit memory cache to latest 1000 messages
            if len(self.message_cache) > 1000:
                oldest_id = next(iter(self.message_cache))
                del self.message_cache[oldest_id]
