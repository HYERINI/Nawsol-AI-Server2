from abc import ABC, abstractmethod
from typing import List

from ecos.domain.ecos import Ecos
from ecos.domain.ecos_interest import EcosInterest


class EcosRepositoryPort(ABC):

    @abstractmethod
    async def save_exchange_rate(self, ecos: Ecos) -> Ecos:
        pass

    @abstractmethod
    async def save_exchange_rates_batch(self, ecos_list: List[Ecos]) -> List[Ecos]:
        pass

    @abstractmethod
    def get_exchange_rate_by_date(self, date: str) -> List[Ecos]:
        pass

    @abstractmethod
    async def save_interest_rate(self, ecos: EcosInterest) -> EcosInterest:
        pass

    @abstractmethod
    async def save_interest_rates_batch(self, ecos_list: List[EcosInterest]) -> List[EcosInterest]:
        pass
