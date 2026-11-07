import time
from typing import Optional
from telethon.tl.custom import Message
from telethon.tl.functions.messages import DeleteMessagesRequest
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins

from nexus.loader import BaseModule, module, command
from nexus.utils import parse_args, format_duration

@module(
    name="Admin",
    description="High-speed message purge, pin/unpin, user inspection, and moderation suite.",
    author="txltedxgod",
    version="1.1.0"
)
class AdminModule(BaseModule):
    @command(
        name="purge",
        description="Fast bulk message deletion from replied message down to latest or N messages.",
        usage=".purge [limit]"
    )
    async def cmd_purge(self, message: Message, args: list):
        chat = await message.get_input_chat()
        limit = int(args[0]) if args and args[0].isdigit() else 100
        
        msgs_to_delete = [message.id]
        if message.is_reply:
            reply = await message.get_reply_message()
            async for msg in self.client.iter_messages(chat, min_id=reply.id - 1, max_id=message.id):
                msgs_to_delete.append(msg.id)
                if len(msgs_to_delete) >= limit:
                    break
        else:
            async for msg in self.client.iter_messages(chat, limit=limit):
                msgs_to_delete.append(msg.id)

        try:
            await self.client.delete_messages(chat, msgs_to_delete)
            notice = await self.client.send_message(
                chat,
                self.ui.success(f"Purged **{len(msgs_to_delete)}** messages.", title="PURGE COMPLETE")
            )
            time.sleep(2)
            await notice.delete()
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to purge messages: {e}"))

    @command(
        name="del",
        description="Delete replied message immediately.",
        usage=".del"
    )
    async def cmd_del(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to a message to delete it."))
            return
        reply = await message.get_reply_message()
        try:
            await self.client.delete_messages(message.chat_id, [message.id, reply.id])
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to delete: {e}"))

    @command(
        name="pin",
        description="Pin replied message (silently or with notification).",
        usage=".pin [loud]"
    )
    async def cmd_pin(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to a message to pin it."))
            return
        reply = await message.get_reply_message()
        loud = args and args[0].lower() in ("loud", "notify", "1", "true")
        try:
            await self.client.pin_message(message.chat_id, reply.id, notify=loud)
            await message.edit(self.ui.success(f"Message pinned successfully ({'notified' if loud else 'silent'})."))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to pin message: {e}"))

    @command(
        name="unpin",
        description="Unpin replied or current chat pinned message.",
        usage=".unpin"
    )
    async def cmd_unpin(self, message: Message, args: list):
        try:
            if message.is_reply:
                reply = await message.get_reply_message()
                await self.client.unpin_message(message.chat_id, reply.id)
            else:
                await self.client.unpin_message(message.chat_id)
            await message.edit(self.ui.success("Message unpinned."))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to unpin: {e}"))

    @command(
        name="user",
        description="Inspect detailed Telegram user metadata.",
        usage=".user [reply/username/id]"
    )
    async def cmd_user(self, message: Message, args: list):
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
        else:
            target = await message.get_sender()

        if not target:
            await message.edit(self.ui.warning("User not found."))
            return

        first = getattr(target, 'first_name', '') or ''
        last = getattr(target, 'last_name', '') or ''
        username = f"@{target.username}" if getattr(target, 'username', None) else "None"
        is_bot = "🤖 Bot" if getattr(target, 'bot', False) else "👤 Human"
        is_premium = "💎 Yes" if getattr(target, 'premium', False) else "No"
        is_verified = "✅ Verified" if getattr(target, 'verified', False) else "No"
        is_restricted = "⚠️ Restricted" if getattr(target, 'restricted', False) else "Clean"
        dc_id = getattr(target.photo, 'dc_id', 'Unknown') if getattr(target, 'photo', None) else 'No Photo'

        fields = {
            "Full Name": f"{first} {last}".strip() or "None",
            "Username": username,
            "User ID": target.id,
            "Data Center": f"DC {dc_id}",
            "Entity Type": is_bot,
            "Telegram Premium": is_premium,
            "Verification": is_verified,
            "Restriction": is_restricted
        }
        await message.edit(self.ui.card(title="USER METADATA", fields=fields, icon="shield"))

    @command(
        name="id",
        description="Display chat and sender Telegram IDs.",
        usage=".id"
    )
    async def cmd_id(self, message: Message, args: list):
        chat_id = message.chat_id
        sender_id = message.sender_id
        fields = {
            "Chat ID": f"`{chat_id}`",
            "Sender ID": f"`{sender_id}`"
        }
        if message.is_reply:
            reply = await message.get_reply_message()
            fields["Reply Msg ID"] = f"`{reply.id}`"
            fields["Reply Sender ID"] = f"`{reply.sender_id}`"

        await message.edit(self.ui.card(title="TELEGRAM IDENTIFIERS", fields=fields, icon="terminal"))
