from decimal import Decimal
from typing import cast, Iterable
from xml.etree.ElementTree import Element, fromstring

from aiohttp import ClientSession

from currency_rate.config import CurrencyRateConfig
from currency_rate.dto import CurrencyRateDTO


def currency_rate_data_mapper(data: str) -> Iterable[CurrencyRateDTO]:
    xml_data = fromstring(data)
    raw_data = []
    for valute in next(xml_data.iter()):
        raw_data.append(
            CurrencyRateDTO(
                name=cast(str, cast(Element, valute.find('Name')).text),
                code=cast(str, cast(Element, valute.find('CharCode')).text),
                value=Decimal(cast(str, cast(Element, valute.find('VunitRate')).text).replace(',', '.')),
            )
        )
    return raw_data


class CurrencyRateGateway:
    def __init__(
        self,
        session: ClientSession,
        config: CurrencyRateConfig,
    ) -> None:
        self._config = config
        self._session = session
    
    async def get_currency_rates(self) -> Iterable[CurrencyRateDTO]:
        async with self._session.get(self._config.url_api) as request:
            data = await request.text()
            return currency_rate_data_mapper(data)
