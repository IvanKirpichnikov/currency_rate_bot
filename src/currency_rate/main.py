from contextlib import aclosing
from pathlib import Path

from aiohttp import ClientSession
from redis.asyncio import Redis

from currency_rate.config import build_config
from currency_rate.gateways.currency_rate import CurrencyRateGateway
from currency_rate.gateways.currency_rate_cache import CurrencyRateCacheGateway


async def run_application(config_path: Path) -> None:
    config = build_config(config_path)
    
    async with (
        ClientSession() as client_session,
        aclosing(Redis.from_url(config.url_redis)) as redis,
    ):
        currency_rate_gateway = CurrencyRateGateway(client_session, config)
        currency_rate_cache_gateway = CurrencyRateCacheGateway(redis)
        data = await currency_rate_gateway.get_currency_rates()
        for datum in data:
            await currency_rate_cache_gateway.set_currency(datum)
