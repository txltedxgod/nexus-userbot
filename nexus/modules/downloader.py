import os
import io
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps
from telethon.tl.custom import Message

from nexus.loader import BaseModule, module, command

@module(
    name="Downloader",
    description="Universal media downloader (TikTok/Reels/Shorts) and instant demotivator meme generator.",
    author="txltedxgod",
    version="1.1.0"
)
class DownloaderModule(BaseModule):
    @command(
        name="dem",
        description="Generate a classic demotivator meme from a replied photo.",
        usage=".dem <top text> [| <bottom text>]"
    )
    async def cmd_dem(self, message: Message, args: list):
        if not message.is_reply:
            await message.edit(self.ui.warning("Reply to an image: `.dem <header> | <footer text>`"))
            return

        reply = await message.get_reply_message()
        if not reply.photo and not (reply.document and "image" in reply.document.mime_type):
            await message.edit(self.ui.error("Replied message does not contain an image."))
            return

        full_text = " ".join(args) if args else "DEMOTIVATOR | bottom text"
        parts = [p.strip() for p in full_text.split("|", 1)]
        top_text = parts[0]
        bot_text = parts[1] if len(parts) > 1 else ""

        await message.edit("`Generating demotivator canvas...`")

        # Download image into memory
        img_bytes = await self.client.download_media(reply, file=bytes)
        if not img_bytes:
            await message.edit(self.ui.error("Failed to download image bytes."))
            return

        base_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Resize keeping aspect ratio
        base_img.thumbnail((700, 700), Image.Resampling.LANCZOS)
        bw, bh = base_img.size

        # Create black canvas with borders
        canvas_w = bw + 120
        canvas_h = bh + 180 + (40 if bot_text else 0)
        canvas = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))

        # Draw white border around inner photo
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([56, 46, canvas_w - 56, bh + 54], outline=(255, 255, 255), width=3)
        draw.rectangle([58, 48, canvas_w - 58, bh + 52], outline=(0, 0, 0), width=2)

        # Paste base photo
        canvas.paste(base_img, (60, 50))

        # Try to use standard font or default
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_sub = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            font_title = ImageFont.load_default()
            font_sub = font_title

        # Draw top title
        title_bbox = draw.textbbox((0, 0), top_text, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((canvas_w - title_w) // 2, bh + 75), top_text, fill=(255, 255, 255), font=font_title)

        # Draw subtitle if present
        if bot_text:
            sub_bbox = draw.textbbox((0, 0), bot_text, font=font_sub)
            sub_w = sub_bbox[2] - sub_bbox[0]
            draw.text(((canvas_w - sub_w) // 2, bh + 125), bot_text, fill=(200, 200, 200), font=font_sub)

        # Save to buffer
        out_buf = io.BytesIO()
        out_buf.name = "demotivator.png"
        canvas.save(out_buf, "PNG")
        out_buf.seek(0)

        await self.client.send_file(message.chat_id, out_buf, reply_to=reply.id)
        await message.delete()

    @command(
        name="dl",
        description="Download clean video without watermarks from TikTok, Reels, Shorts, Twitter/X.",
        usage=".dl <video_url>"
    )
    async def cmd_dl(self, message: Message, args: list):
        url = args[0] if args else ""
        if not url and message.is_reply:
            reply = await message.get_reply_message()
            url = reply.text or ""

        if not url or not url.startswith("http"):
            await message.edit(self.ui.warning("Usage: `.dl <video_url>` (TikTok, Reels, Shorts, X)"))
            return

        await message.edit(f"`Bypassing watermarks and processing video stream from {url[:30]}...`")

        # Cobalt API endpoint
        cobalt_api = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": url}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(cobalt_api, json=payload, headers=headers, timeout=25) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        download_url = data.get("url")
                        if download_url:
                            # Stream download video
                            async with session.get(download_url, timeout=40) as v_resp:
                                if v_resp.status == 200:
                                    v_bytes = await v_resp.read()
                                    v_file = io.BytesIO(v_bytes)
                                    v_file.name = "downloaded_video.mp4"
                                    caption = f"🎬 **DOWNLOADED STREAM**\n{self.ui.theme['bullet']} **Source:** `{url[:40]}...`"
                                    await self.client.send_file(message.chat_id, v_file, caption=caption)
                                    await message.delete()
                                    return
                    
            await message.edit(self.ui.error("Media extractor could not fetch video stream (API rate limited or private)."))
        except Exception as e:
            await message.edit(self.ui.error(f"Download failed: {e}"))
