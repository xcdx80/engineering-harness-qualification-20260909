from dataclasses import dataclass


class InvalidPayload(TypeError):
    def __init__(self) -> None:
        super().__init__('Expected an object')


class MissingField(ValueError):
    def __init__(self, field: str) -> None:
        super().__init__(f'{field} is required')


@dataclass(frozen=True)
class EntryRequest:
    title: str
    key: str


def validate_request(value: object) -> EntryRequest:
    if not isinstance(value, dict):
        raise InvalidPayload()
    title, key = value.get('title'), value.get('key')
    if not isinstance(title, str) or not title.strip():
        raise MissingField('Title')
    if not isinstance(key, str) or not key:
        raise MissingField('key')
    return EntryRequest(title.strip(), key)
