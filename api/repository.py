import sqlite3
from pathlib import Path

from .domain import EntryRequest


class MissingEntry(RuntimeError):
    def __init__(self) -> None:
        super().__init__('Missing stored entry')


def save_entry(database: Path, request: EntryRequest) -> dict[str, object]:
    with sqlite3.connect(database) as connection:
        connection.execute('CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, title TEXT NOT NULL, request_key TEXT UNIQUE NOT NULL)')
        connection.execute('INSERT OR IGNORE INTO entries(title, request_key) VALUES(?, ?)', (request.title, request.key))
        row = connection.execute('SELECT id,title FROM entries WHERE request_key=?', (request.key,)).fetchone()
        if row is None:
            raise MissingEntry()
        return {'entry_id': row[0], 'title': row[1]}
