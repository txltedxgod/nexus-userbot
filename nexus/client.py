import time
from typing import Optional
from telethon import TelegramClient, events
from telethon.tl.custom import Message

from nexus.config import config
from nexus.database import Database
from nexus.logger import get_logger
from nexus.loader import ModuleManager
from nexus.ui import ui
from nexus.utils import parse_args

logger = get_logger("client")

class NexusClient(TelegramClient):
    """
    Core Nexus Userbot Client wrapping Telethon TelegramClient.
    Provides automated command dispatching, dynamic prefix resolution,
    and event routing to registered watchers with AyuGram compatibility.
    """
    def __init__(
        self,
        session_name: str = config.SESSION_NAME,
        api_id: int = config.API_ID,
        api_hash: str = config.API_HASH,
        database_path = config.DATABASE_PATH
    ):
        super().__init__(
            session_name,
            api_id,
            api_hash,
            device_model=config.DEVICE_MODEL,
            system_version=config.SYSTEM_VERSION,
            app_version=config.APP_VERSION,
            lang_code=config.LANG_CODE,
            system_lang_code=config.SYSTEM_LANG_CODE
        )
        self.db = Database(database_path)
        self.modules = ModuleManager(self, self.db)
        self.me = None
        self.start_time = time.time()
        self._setup_event_handlers()

    @property
    def prefix(self) -> str:
        return self.db.get("core", "prefix", config.DEFAULT_PREFIX)

    def set_prefix(self, new_prefix: str) -> None:
        self.db.set("core", "prefix", new_prefix)

    def _setup_event_handlers(self):
        @self.on(events.NewMessage(outgoing=True))
        async def on_outgoing_message(event: events.NewMessage.Event):
            msg: Message = event.message
            if not msg.text:
                return

            prefix = self.prefix
            if msg.text.startswith(prefix) and len(msg.text) > len(prefix):
                parts = msg.text[len(prefix):].split(maxsplit=1)
                cmd_name = parts[0].lower()
                raw_args = parts[1] if len(parts) > 1 else ""

                if cmd_name in self.modules.commands:
                    cmd_meta = self.modules.commands[cmd_name]
                    try:
                        args = parse_args(raw_args)
                        await cmd_meta.func(msg, args)
                    except Exception as e:
                        logger.error(f"Error executing command '{cmd_name}': {e}", exc_info=True)
                        try:
                            await msg.edit(ui.error(f"Command '{cmd_name}' failed: {e}"))
                        except Exception:
                            pass

        @self.on(events.NewMessage(incoming=True))
        async def on_incoming_message(event: events.NewMessage.Event):
            msg: Message = event.message
            for watcher in self.modules.watchers:
                if watcher.incoming:
                    try:
                        await watcher.func(msg)
                    except Exception as e:
                        logger.error(f"Watcher in '{watcher.module_name}' failed: {e}", exc_info=True)

    async def initialize(self):
        """Connect, fetch owner identity, and load modules."""
        logger.info(f"Connecting to Telegram with device profile: {config.DEVICE_MODEL}...")
        await self.connect()
        if not await self.is_user_authorized():
            logger.warning("Client is not authorized. Please run authentication first.")
            return False

        self.me = await self.get_me()
        logger.info(f"Authorized as: {self.me.first_name} (@{self.me.username or 'None'}) [ID: {self.me.id}]")
        
        # Load all built-in modules
        self.modules.load_all_from_directory(config.MODULES_DIR)
        logger.info(f"Loaded {len(self.modules.modules)} modules ({len(self.modules.commands)} commands)")
        return True
