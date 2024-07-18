import tomllib
from dataclasses import dataclass
from pathlib import Path

from adaptix import load


@dataclass(frozen=True, slots=True)
class CurrencyRateConfig:
    url_api: str
    url_redis: str


def build_config(path: Path) -> CurrencyRateConfig:
    with path.open('rb') as file:
        data = tomllib.load(file)
    
    return load(data, CurrencyRateConfig)
