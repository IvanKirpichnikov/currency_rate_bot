from decimal import Decimal

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from pydantic import BaseModel

from bot.adapters.currency_rate import CurrencyRateGateway
from bot.adapters.exchange import ExchangeAdapter, NotFoundCurrencyError
from bot.command_mk2 import CommandMk2


router = Router()


class ExchangeDs(BaseModel):
    sum: Decimal
    to_code: str
    from_code: str


@router.message(
    CommandMk2(
        'exchange { from_code } { to_code } { sum }',
        response_model=ExchangeDs,
    )
)
async def exchange(
    event: Message,
    exchange_ds: ExchangeDs,
    exchange_adapter: ExchangeAdapter,
) -> None:
    try:
        sum = await exchange_adapter.exchange(
            sum=exchange_ds.sum,
            to_code=exchange_ds.to_code,
            from_code=exchange_ds.from_code,
        )
    except NotFoundCurrencyError as e:
        await event.answer(f'Не найдена валюта по коду "{e.code}"')
        return None
    
    await event.answer(str(sum))


@router.message(Command('rates'))
async def rates(
    event: Message,
    currency_rate_gateway: CurrencyRateGateway,
) -> None:
    rates = await currency_rate_gateway.read_all()
    if not rates:
        await event.answer('Нет данных')
    
    text = ''
    for rate in rates:
        text += f'{rate.code} - {rate.name} - {rate.value}\n'
    
    await event.answer(text)
