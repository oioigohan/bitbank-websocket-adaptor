from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DepthDiff:
    a: List[List] = None
    b: List[List] = None
    timestamp: int = None
    sequenceId: str = None