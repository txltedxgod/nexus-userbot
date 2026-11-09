import asyncio
from telethon.tl.custom import Message
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

from nexus.loader import BaseModule, module, command, watcher

@module(
    name="Reactions",
    description="Automated user reaction watcher, emoji sniper, and visual flex animations.",
    author="txltedxgod",
    version="1.1.0"
)
class ReactionsModule(BaseModule):
    @command(
        name="autoreact",
        description="Bind an automatic reaction to every message sent by a specific user.",
        usage=".autoreact <@user/id> <emoji>"
    )
    async def cmd_autoreact(self, message: Message, args: list):
        if len(args) < 2 and not (message.is_reply and len(args) >= 1):
            await message.edit(self.ui.warning("Usage: `.autoreact @username 🔥` or reply with `.autoreact 🤡`"))
            return

        target_user = None
        emoji = "🔥"

        if message.is_reply:
            reply = await message.get_reply_message()
            target_user = await reply.get_sender()
            emoji = args[0] if args else "🔥"
        else:
            try:
                target_user = await self.client.get_entity(args[0] if not args[0].isdigit() else int(args[0]))
                emoji = args[1]
            except Exception as e:
                await message.edit(self.ui.error(f"Cannot resolve user: {e}"))
                return

        if not target_user:
            await message.edit(self.ui.warning("Target user could not be resolved."))
            return

        rules = self.get_config("auto_react_rules", {})
        target_id_str = str(target_user.id)
        rules[target_id_str] = emoji
        self.set_config("auto_react_rules", rules)

        uname = getattr(target_user, 'username', 'no_username')
        card = self.ui.card(
            title="AUTO-REACTION ACTIVE",
            fields={
                "Target User": f"@{uname} (ID: {target_user.id})",
                "Emoji Bound": emoji,
                "Behavior": "Will instantly react to any message from this user."
            },
            icon="fire"
        )
        await message.edit(card)

    @command(
        name="delreact",
        description="Remove automated reaction rule for a user.",
        usage=".delreact <@user/id>"
    )
    async def cmd_delreact(self, message: Message, args: list):
        target_id_str = ""
        if message.is_reply:
            reply = await message.get_reply_message()
            target_id_str = str(reply.sender_id)
        elif args:
            try:
                entity = await self.client.get_entity(args[0] if not args[0].isdigit() else int(args[0]))
                target_id_str = str(entity.id)
            except Exception:
                target_id_str = args[0]

        rules = self.get_config("auto_react_rules", {})
        if target_id_str in rules:
            del rules[target_id_str]
            self.set_config("auto_react_rules", rules)
            await message.edit(self.ui.success(f"Removed auto-reaction for user ID: `{target_id_str}`"))
        else:
            await message.edit(self.ui.warning("No auto-reaction rule found for this user."))

    @command(
        name="reacts",
        description="List all active auto-reaction rules.",
        usage=".reacts"
    )
    async def cmd_reacts(self, message: Message, args: list):
        rules = self.get_config("auto_react_rules", {})
        if not rules:
            await message.edit(self.ui.info("No active auto-reaction rules registered."))
            return

        items = [f"User `{uid}` ➔ Reaction: {emoji}" for uid, emoji in rules.items()]
        await message.edit(self.ui.list_items("ACTIVE AUTO-REACTION RULES", items, icon="fire"))

    @command(
        name="flex",
        description="Animate an emoji progression flex in the current message.",
        usage=".flex"
    )
    async def cmd_flex(self, message: Message, args: list):
        emojis = ["💎", "⚡", "🔥", "👑", "🚀", "✨", "🦾", "👾", "✦ ɴ ᴇ x ᴜ s ✦"]
        for em in emojis:
            try:
                await message.edit(f"**{em}**")
                await asyncio.sleep(0.3)
            except Exception:
                pass

    @watcher(incoming=True)
    async def auto_reaction_watcher(self, message: Message):
        """Automatically react to messages from rule-bound users."""
        rules = self.get_config("auto_react_rules", {})
        sender_id_str = str(message.sender_id)

        if sender_id_str in rules:
            target_emoji = rules[sender_id_str]
            try:
                await self.client(SendReactionRequest(
                    peer=message.chat_id,
                    msg_id=message.id,
                    reaction=[ReactionEmoji(emoticon=target_emoji)]
                ))
            except Exception as e:
                self.logger.error(f"Failed to apply auto-reaction: {e}")
