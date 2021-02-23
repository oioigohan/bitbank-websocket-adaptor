from typing import List
from dataclasses import dataclass


@dataclass
class StatusType:
    NORMAL = 'NORMAL'
    BUSY = 'BUSY'
    VERY_BUSY = 'VERY_BUSY'
    HALT = 'HALT'


@dataclass
class ContractType:
    FIRST_RIGHT_FULL = 'FIRST_RIGHT_FULL'  # 本完全約定
    FIRST_LC_FULL = 'FIRST_LC_FULL'  # LC完全約定
    # FIRST_RIGHT_SEMI = 'FIRST_RIGHT_SEMI'  # 本半約定
    # FIRST_LC_SEMI = 'FIRST_LC_SEMI'  # LC半約定
    SECONDARY_RIGHT_FULL = 'SECONDARY_RIGHT_FULL'  # 本完全約定
    SECONDARY_LC_FULL = 'SECONDARY_LC_FULL'  # LC完全約定
    # SECONDARY_RIGHT_SEMI = 'SECONDARY_RIGHT_SEMI'  # 本半約定
    # SECONDARY_LC_SEMI = 'SECONDARY_LC_SEMI'  # LC半約定
    # SECONDARY_LC_SEPARETE = 'SECONDARY_LC_SEPARETE'  # LC分割約定(異なる価格で分割されて約定)
    # SECONDARY_RIGHT_SEMI_SEPARETE = 'SECONDARY_RIGHT_SEMI_SEPARETE'  # 本分割半約定
    # SECONDARY_LC_SEMI_SEPARETE = 'SECONDARY_LC_SEMI_SEPARETE'  # LC分割半約定
    RESUME_FULL = 'RESUME_FULL'  # 復帰注文完全約定
    # RESUME_SEPARETE = 'RESUME_SEPARETE'  # 復帰注文分割約定(異なる価格で分割されて約定)
