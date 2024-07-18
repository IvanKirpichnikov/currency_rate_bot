from redis.asyncio import Redis

from currency_rate.dto import CurrencyRateDTO


class CurrencyRateCacheGateway:
    def __init__(self, connect: Redis) -> None:
        self._connect = connect
    
    async def set_currency(self, data: CurrencyRateDTO) -> None:
        await self._connect.set(
            f'currency:{data.code}',
            data.serialization(),
        )
