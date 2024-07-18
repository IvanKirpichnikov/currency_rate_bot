import json
from dataclasses import dataclass
from decimal import Decimal

from adaptix import dump


@dataclass(frozen=True, slots=True)
class CurrencyRateDTO:
    code: str
    name: str
    value: Decimal
    
    def serialization(self) -> str:
        return json.dumps(dump(self))
