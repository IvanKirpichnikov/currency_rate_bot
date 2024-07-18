from decimal import Decimal

from bot.adapters.currency_rate import CurrencyRateGateway


class NotFoundCurrencyError(Exception):
    def __init__(self, msg: str, code: str) -> None:
        super().__init__(msg)
        self.code = code


class ExchangeAdapter:
    def __init__(self, gateway: CurrencyRateGateway) -> None:
        self._gateway = gateway
    
    async def exchange(self, sum: Decimal, from_code: str, to_code: str) -> Decimal:
        from_ = await self._gateway.read_by_code(from_code)
        if from_ is None:
            raise NotFoundCurrencyError(
                'Not found currency by code %r' % from_code,
                from_code,
            )
        
        if to_code == 'RUB':
            return sum * from_.value
        
        to = await self._gateway.read_by_code(to_code)
        if to is None:
            raise NotFoundCurrencyError(
                'Not found currency by code %r' % to_code,
                to_code,
            )
        return sum * from_.value * (1 / to.value)
