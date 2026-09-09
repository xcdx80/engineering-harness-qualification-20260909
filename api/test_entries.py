from pathlib import Path

import pytest

from .domain import validate_request
from .repository import save_entry


def test_stored_entry_and_duplicate_request(tmp_path: Path) -> None:
    request = validate_request({'title': ' verified ', 'key': 'one'})
    database = tmp_path / 'entries.sqlite'
    first = save_entry(database, request)
    assert first == {'id': 1, 'title': 'verified'}
    assert save_entry(database, request) == first


def test_invalid_payload_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_request({'title': '', 'key': 'one'})


def test_concurrent_duplicate_requests_store_one_row(tmp_path: Path) -> None:
    import sqlite3
    from concurrent.futures import ThreadPoolExecutor

    database = tmp_path / 'concurrent.sqlite'
    request = validate_request({'title': 'concurrent', 'key': 'same'})
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: save_entry(database, request), range(8)))
    assert all(result == results[0] for result in results)
    connection = sqlite3.connect(database)
    try:
        assert connection.execute('SELECT COUNT(*) FROM entries').fetchone() == (1,)
    finally:
        connection.close()


@pytest.mark.parametrize('fails', [False, True])
def test_connection_closes_on_success_and_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fails: bool) -> None:
    import sqlite3

    from . import repository

    class TrackedConnection(sqlite3.Connection):
        closed = False

        def close(self) -> None:
            self.closed = True
            super().close()

    connection = TrackedConnection(str(tmp_path / 'closure.sqlite'))
    if fails:
        connection.execute('CREATE TABLE entries (wrong_column TEXT)')
    monkeypatch.setattr(repository.sqlite3, 'connect', lambda _: connection)
    request = validate_request({'title': 'tracked', 'key': 'one'})
    if fails:
        with pytest.raises(sqlite3.OperationalError):
            save_entry(tmp_path / 'closure.sqlite', request)
    else:
        assert save_entry(tmp_path / 'closure.sqlite', request)['title'] == 'tracked'
    assert connection.closed


def test_response_matches_published_contract(tmp_path: Path) -> None:
    import json

    contract = json.loads((Path(__file__).parent.parent / 'entry-contract.json').read_text())
    result = save_entry(tmp_path / 'contract.sqlite', validate_request({'title': 'contract', 'key': 'contract'}))
    assert set(result) == set(contract['required']) == set(contract['properties'])
    assert isinstance(result['id'], int)
    assert isinstance(result['title'], str)
