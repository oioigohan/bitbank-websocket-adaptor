from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Message:
    data: dict = None


@dataclass_json
@dataclass
class Response:
    message: Message = None
    room_name: str = None
