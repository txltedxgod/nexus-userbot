import os
import tempfile
from pathlib import Path
from telethon.tl.custom import Message
from telethon.tl.types import (
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    DocumentAttributeFilename
)

from nexus.loader import BaseModule, module, command
from nexus.utils import format_bytes, format_duration

@module(
    name="Media",
    description="Video to circular note converter, voice synthesizer, and metadata inspector.",
    author="txltedxgod",
    version="1.1.0"
)
class MediaModule(BaseModule):
    @command(
        name="circle",
        description="Convert a rectangular video into a circular Telegram video note.",
        usage=".circle [reply to video]"
    )
    async def cmd_circle(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to a video file: `.circle`"))
            return

        reply = await message.get_reply_message()
        if not reply.video and not (reply.document and "video" in reply.document.mime_type):
            await message.edit(self.ui.error("Replied message does not contain a video."))
            return

        await message.edit("`Converting video to circular video note...`")
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = await self.client.download_media(reply, file=tmp_dir)
            if not file_path or not os.path.exists(file_path):
                await message.edit(self.ui.error("Failed to download media."))
                return

            # Extract video attribute
            duration = 10
            w, h = 360, 360
            for attr in getattr(reply.document, "attributes", []):
                if isinstance(attr, DocumentAttributeVideo):
                    duration = int(attr.duration)
                    w = attr.w
                    h = attr.h
                    break

            try:
                # Send as round video note
                await self.client.send_file(
                    message.chat_id,
                    file_path,
                    video_note=True,
                    attributes=[DocumentAttributeVideo(
                        duration=duration,
                        w=min(w, h),
                        h=min(w, h),
                        round_message=True
                    )]
                )
                await message.delete()
            except Exception as e:
                await message.edit(self.ui.error(f"Failed to convert video note: {e}"))

    @command(
        name="voice",
        description="Convert audio or video file into a Telegram voice message with waveform.",
        usage=".voice [reply to audio/video]"
    )
    async def cmd_voice(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to an audio/video message: `.voice`"))
            return

        reply = await message.get_reply_message()
        if not reply.media:
            await message.edit(self.ui.error("Replied message has no media."))
            return

        await message.edit("`Converting audio to voice note...`")
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = await self.client.download_media(reply, file=tmp_dir)
            if not file_path or not os.path.exists(file_path):
                await message.edit(self.ui.error("Failed to download audio."))
                return

            duration = 0
            for attr in getattr(reply.document, "attributes", []):
                if isinstance(attr, (DocumentAttributeAudio, DocumentAttributeVideo)):
                    duration = int(getattr(attr, "duration", 0))
                    break

            try:
                await self.client.send_file(
                    message.chat_id,
                    file_path,
                    voice_note=True,
                    attributes=[DocumentAttributeAudio(
                        duration=duration,
                        voice=True
                    )]
                )
                await message.delete()
            except Exception as e:
                await message.edit(self.ui.error(f"Failed to send voice note: {e}"))

    @command(
        name="mediainfo",
        description="Inspect technical metadata of replied media file.",
        usage=".mediainfo [reply to media]"
    )
    async def cmd_mediainfo(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to a media message to inspect."))
            return

        reply = await message.get_reply_message()
        if not reply.media:
            await message.edit(self.ui.error("No media attached to replied message."))
            return

        doc = getattr(reply, "document", None)
        fields = {}
        if doc:
            fields["Mime-Type"] = doc.mime_type
            fields["File Size"] = format_bytes(doc.size)
            fields["DC ID"] = getattr(doc, "dc_id", "Unknown")
            for attr in doc.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    fields["Filename"] = attr.file_name
                elif isinstance(attr, DocumentAttributeVideo):
                    fields["Resolution"] = f"{attr.w}x{attr.h}"
                    fields["Duration"] = format_duration(attr.duration)
                elif isinstance(attr, DocumentAttributeAudio):
                    fields["Audio Title"] = attr.title or "Unknown"
                    fields["Performer"] = attr.performer or "Unknown"
                    fields["Duration"] = format_duration(attr.duration)
        elif reply.photo:
            fields["Media Type"] = "Photo"
            fields["DC ID"] = getattr(reply.photo, "dc_id", "Unknown")
            fields["Date"] = str(reply.photo.date)

        await message.edit(self.ui.card(title="MEDIA METADATA", fields=fields, icon="stats"))
