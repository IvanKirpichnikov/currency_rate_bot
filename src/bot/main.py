from contextlib import aclosing
from pathlib import Path

from aiogram import Bot, Dispatcher
from redis.asyncio import Redis

from bot.adapters.currency_rate import CurrencyRateGateway
from bot.adapters.exchange import ExchangeAdapter
from bot.config import build_config
from bot.handlers import router


async def run_application(config_path: Path) -> None:
    config = build_config(config_path)
    bot = Bot(config.token)
    disp = Dispatcher()
    
    async with aclosing(Redis.from_url(config.url_redis, decode_responses=True)) as redis:
        currency_rate_gateway = CurrencyRateGateway(redis)
        exchange_adapter = ExchangeAdapter(currency_rate_gateway)
        
        disp.include_router(router)
        
        disp['exchange_adapter'] = exchange_adapter
        disp['currency_rate_gateway'] = currency_rate_gateway
        
        await disp.start_polling(bot)
