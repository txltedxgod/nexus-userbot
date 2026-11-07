import sqlite3
import json
import threading
from pathlib import Path
from typing import Any, Dict, Optional
from contextlib import contextmanager

from nexus.logger import get_logger

logger = get_logger("database")

class Database:
    """
    Thread-safe SQLite Key-Value Storage with module namespacing.
    Supports atomic operations, JSON serialization, and default values.
    Properly closes connections to prevent Windows file locking.
    """
    def __init__(self, db_path: Path):
        self.db_path = str(db_path)
        self._lock = threading.Lock()
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._lock, self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS kv_store (
                    module TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (module, key)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kv_module ON kv_store(module)")
            conn.commit()
            logger.debug(f"Database initialized at {self.db_path}")

    def get(self, module: str, key: str, default: Any = None) -> Any:
        with self._lock, self._get_connection() as conn:
            cur = conn.execute(
                "SELECT value FROM kv_store WHERE module = ? AND key = ?",
                (module, key)
            )
            row = cur.fetchone()
            if row:
                try:
                    return json.loads(row["value"])
                except (json.JSONDecodeError, TypeError):
                    return row["value"]
            return default

    def set(self, module: str, key: str, value: Any) -> None:
        serialized = json.dumps(value, ensure_ascii=False)
        with self._lock, self._get_connection() as conn:
            conn.execute("""
                INSERT INTO kv_store (module, key, value, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(module, key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (module, key, serialized))
            conn.commit()

    def delete(self, module: str, key: str) -> bool:
        with self._lock, self._get_connection() as conn:
            cur = conn.execute(
                "DELETE FROM kv_store WHERE module = ? AND key = ?",
                (module, key)
            )
            conn.commit()
            return cur.rowcount > 0

    def get_all(self, module: str) -> Dict[str, Any]:
        result = {}
        with self._lock, self._get_connection() as conn:
            cur = conn.execute(
                "SELECT key, value FROM kv_store WHERE module = ?",
                (module,)
            )
            for row in cur.fetchall():
                try:
                    result[row["key"]] = json.loads(row["value"])
                except (json.JSONDecodeError, TypeError):
                    result[row["key"]] = row["value"]
        return result

    def clear(self, module: str) -> int:
        with self._lock, self._get_connection() as conn:
            cur = conn.execute("DELETE FROM kv_store WHERE module = ?", (module,))
            conn.commit()
            return cur.rowcount
