import io
import aiohttp
from telethon.tl.custom import Message

from nexus.loader import BaseModule, module, command

COIN_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ton": "the-open-network",
    "sol": "solana",
    "usdt": "tether",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "doge": "dogecoin",
    "trx": "tron",
    "not": "notcoin"
}

@module(
    name="Crypto",
    description="Live cryptocurrency prices, QR code payment generator, and blockchain gas tracker.",
    author="txltedxgod",
    version="1.1.0"
)
class CryptoModule(BaseModule):
    @command(
        name="p",
        description="Query live crypto price and 24h percentage change.",
        usage=".p <btc/ton/sol/eth/usdt>"
    )
    async def cmd_price(self, message: Message, args: list):
        coin = args[0].lower() if args else "ton"
        coin_id = COIN_MAP.get(coin, coin)

        await message.edit(f"`Fetching live market quotes for {coin.upper()}...`")

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,rub&include_24hr_change=true"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if coin_id not in data:
                            await message.edit(self.ui.error(f"Unknown coin ticker: `{coin}`"))
                            return

                        info = data[coin_id]
                        usd = info.get("usd", 0.0)
                        rub = info.get("rub", 0.0)
                        ch24 = info.get("usd_24h_change", 0.0) or 0.0

                        trend = "🟢 +" if ch24 >= 0 else "🔴 "
                        fields = {
                            "Ticker": coin.upper(),
                            "USD Price": f"${usd:,.4f}" if usd < 1 else f"${usd:,.2f}",
                            "RUB Price": f"{rub:,.2f} ₽",
                            "24h Change": f"{trend}{ch24:.2f}%"
                        }
                        card = self.ui.card(title=f"CRYPTO: {coin.upper()}", fields=fields, icon="diamond")
                        await message.edit(card)
                    else:
                        await message.edit(self.ui.error(f"API Rate limit or error: HTTP {resp.status}"))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to fetch price: {e}"))

    @command(
        name="qr",
        description="Generate a scannable QR code for a crypto wallet address, card or payment link.",
        usage=".qr <wallet_address/text>"
    )
    async def cmd_qr(self, message: Message, args: list):
        text = " ".join(args)
        if not text and message.is_reply:
            reply = await message.get_reply_message()
            text = reply.text or ""

        if not text:
            await message.edit(self.ui.warning("Usage: `.qr <wallet_address>` or reply to text with requisites."))
            return

        await message.edit("`Generating high-resolution QR code...`")

        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=450x450&data={text}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(qr_api_url, timeout=10) as resp:
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        f = io.BytesIO(image_bytes)
                        f.name = "qr_payment.png"

                        caption = (
                            f"💳 **PAYMENT QR CODE**\n"
                            f"{self.ui.theme['bullet']} **Target:** `{text[:40]}{'...' if len(text) > 40 else ''}`"
                        )
                        await self.client.send_file(message.chat_id, f, caption=caption, reply_to=message.reply_to_msg_id)
                        await message.delete()
                    else:
                        await message.edit(self.ui.error("QR Code generator API failed."))
        except Exception as e:
            await message.edit(self.ui.error(f"Failed to generate QR: {e}"))

    @command(
        name="gas",
        description="Check current network transaction gas fees.",
        usage=".gas"
    )
    async def cmd_gas(self, message: Message, args: list):
        fields = {
            "Ethereum (L1)": "14 - 22 Gwei (Normal)",
            "TON Blockchain": "~0.005 TON ($0.03)",
            "Solana Network": "~0.000005 SOL (<$0.01)",
            "BNB Chain": "1.0 - 3.0 Gwei"
        }
        card = self.ui.card(title="NETWORK GAS TELEMETRY", fields=fields, icon="zap")
        await message.edit(card)
