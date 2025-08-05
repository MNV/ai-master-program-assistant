import os
import sqlite3
import yaml
from typing import Any, Dict


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Читает YAML-конфиг (bot_token, db_path и т.п.)
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_db_connection(config: Dict[str, Any] = None) -> sqlite3.Connection:
    """
    Возвращает sqlite3.Connection, создавая файл, если нужно.
    Путь к БД берется из конфига: ключ "db_path".
    """
    if config is None:
        config = load_config()

    db_path = config.get("db_path", "src/data/processed/courses.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Инициализирует схему БД, создавая таблицу courses, если её нет.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program TEXT NOT NULL,
            semester INTEGER NOT NULL,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            type TEXT NOT NULL
        )
        """
    )
    conn.commit()
