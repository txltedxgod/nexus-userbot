import os
import sys
import inspect
import importlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any, Type
from telethon import events
from telethon.tl.custom import Message

from nexus.logger import get_logger
from nexus.database import Database
from nexus.ui import ui, LuxuryUI

logger = get_logger("loader")

@dataclass
class CommandMeta:
    func: Callable
    name: str
    description: str
    usage: str
    aliases: List[str] = field(default_factory=list)
    only_owner: bool = True
    module_name: str = ""

@dataclass
class WatcherMeta:
    func: Callable
    event_type: str = "new_message"
    incoming: bool = True
    outgoing: bool = False
    module_name: str = ""

class BaseModule:
    """
    Base class for all Nexus Userbot modules.
    Provides database access, UI rendering, logging, and lifecycle events.
    """
    name: str = "UnnamedModule"
    description: str = "No description provided."
    author: str = "nexus"
    version: str = "1.0.0"

    def __init__(self, client: Any, db: Database):
        self.client = client
        self.db = db
        self.ui: LuxuryUI = ui
        self.logger = get_logger(self.name.lower())
        self._commands: Dict[str, CommandMeta] = {}
        self._watchers: List[WatcherMeta] = []

    async def on_load(self):
        """Called immediately after module is loaded."""
        pass

    async def on_unload(self):
        """Called right before module is unloaded."""
        pass

    def get_config(self, key: str, default: Any = None) -> Any:
        return self.db.get(self.name.lower(), key, default)

    def set_config(self, key: str, value: Any) -> None:
        self.db.set(self.name.lower(), key, value)

    def del_config(self, key: str) -> bool:
        return self.db.delete(self.name.lower(), key)

def module(name: str, description: str = "", author: str = "txltedxgod", version: str = "1.0.0"):
    """Class decorator to define a Nexus module."""
    def decorator(cls: Type[BaseModule]):
        cls.name = name
        cls.description = description
        cls.author = author
        cls.version = version
        return cls
    return decorator

def command(
    name: Optional[str] = None,
    description: str = "No help provided",
    usage: str = "",
    aliases: Optional[List[str]] = None,
    only_owner: bool = True
):
    """Method decorator to register a module command."""
    def decorator(func: Callable):
        cmd_name = name or func.__name__
        func._cmd_meta = CommandMeta(
            func=func,
            name=cmd_name,
            description=description,
            usage=usage or f".{cmd_name}",
            aliases=aliases or [],
            only_owner=only_owner
        )
        return func
    return decorator

def watcher(incoming: bool = True, outgoing: bool = False):
    """Method decorator to register an event watcher."""
    def decorator(func: Callable):
        func._watcher_meta = WatcherMeta(
            func=func,
            incoming=incoming,
            outgoing=outgoing
        )
        return func
    return decorator

class ModuleManager:
    """
    Dynamic Module Manager: Handles hot-reloading, registry,
    event hooks, and command routing.
    """
    def __init__(self, client: Any, db: Database):
        self.client = client
        self.db = db
        self.modules: Dict[str, BaseModule] = {}
        self.commands: Dict[str, CommandMeta] = {}
        self.watchers: List[WatcherMeta] = []

    def register_module(self, mod_instance: BaseModule):
        mod_name = mod_instance.name.lower()
        if mod_name in self.modules:
            self.unregister_module(mod_name)

        # Inspect commands and watchers
        for attr_name in dir(mod_instance):
            attr = getattr(mod_instance, attr_name)
            if hasattr(attr, "_cmd_meta"):
                meta: CommandMeta = getattr(attr, "_cmd_meta")
                meta.module_name = mod_name
                self.commands[meta.name.lower()] = meta
                for alias in meta.aliases:
                    self.commands[alias.lower()] = meta
                mod_instance._commands[meta.name.lower()] = meta
            elif hasattr(attr, "_watcher_meta"):
                w_meta: WatcherMeta = getattr(attr, "_watcher_meta")
                w_meta.module_name = mod_name
                self.watchers.append(w_meta)
                mod_instance._watchers.append(w_meta)

        self.modules[mod_name] = mod_instance
        logger.info(f"Registered module: '{mod_instance.name}' (Commands: {len(mod_instance._commands)}, Watchers: {len(mod_instance._watchers)})")

    def unregister_module(self, mod_name: str) -> bool:
        mod_name = mod_name.lower()
        if mod_name not in self.modules:
            return False

        mod_instance = self.modules[mod_name]
        # Remove commands
        to_del = [k for k, v in self.commands.items() if v.module_name == mod_name]
        for k in to_del:
            del self.commands[k]

        # Remove watchers
        self.watchers = [w for w in self.watchers if w.module_name != mod_name]

        del self.modules[mod_name]
        logger.info(f"Unregistered module: '{mod_name}'")
        return True

    def load_module_from_file(self, filepath: Path) -> Optional[BaseModule]:
        module_path = str(filepath.resolve())
        module_name = filepath.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            logger.error(f"Failed to create spec for {module_path}")
            return None

        py_mod = importlib.util.module_from_spec(spec)
        sys.modules[f"nexus.modules.{module_name}"] = py_mod
        try:
            spec.loader.exec_module(py_mod)
        except Exception as e:
            logger.error(f"Error loading module from {filepath}: {e}", exc_info=True)
            return None

        # Find subclasses of BaseModule
        for _, obj in inspect.getmembers(py_mod):
            if inspect.isclass(obj) and issubclass(obj, BaseModule) and obj is not BaseModule:
                instance = obj(self.client, self.db)
                self.register_module(instance)
                return instance

        logger.warning(f"No BaseModule subclass found in {filepath}")
        return None

    def load_all_from_directory(self, dir_path: Path):
        if not dir_path.exists():
            return
        for file in sorted(dir_path.glob("*.py")):
            if file.name.startswith("__"):
                continue
            self.load_module_from_file(file)
