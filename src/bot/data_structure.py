from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class CurrencyRateDs:
    code: str
    name: str
    value: Decimal
