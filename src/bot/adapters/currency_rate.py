import json
from typing import Iterable

from adaptix import load
from redis.asyncio import Redis

from bot.data_structure import CurrencyRateDs


class CurrencyRateGateway:
    def __init__(self, connect: Redis) -> None:
        self._connect = connect
    
    async def read_by_code(self, data: str) -> CurrencyRateDs | None:
        d = await self._connect.get(f'currency:{data}')
        if d is None:
            return None
        return load(json.loads(d), CurrencyRateDs)
    
    async def read_all(self) -> Iterable[CurrencyRateDs]:
        raw_data = []
        async for data in self._connect.scan_iter('currency:*'):
            raw_data.append(json.loads(data))
        return load(raw_data, Iterable[CurrencyRateDs])
