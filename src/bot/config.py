import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from adaptix import load


@dataclass(frozen=True, slots=True)
class BotConfig:
    url_redis: str
    token: str = field(repr=False)


def build_config(path: Path) -> BotConfig:
    with path.open('rb') as file:
        data = tomllib.load(file)
    
    return load(data, BotConfig)
