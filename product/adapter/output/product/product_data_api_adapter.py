from datetime import datetime
from typing import List

from ecos.domain.value_object.timestamp import Timestamp
from product.domain.product_etf import ProductEtf
from product.domain.product_etf_data import ProductEtfData
from product.domain.value_object.product_source import ProductSource
from product.infrastructure.api.data_go_client import DataGoClient


class ProductDataApiAdapter:
    def __init__(self):
        self.client = DataGoClient()
    pass

    async def get_etf_data(self) -> ProductEtfData:
        raw_items = await self.client.get_etf_data()
        items: List[ProductEtf] = [
            ProductEtf(
                fltRt=item.get("fltRt"),
                nav=item.get("nav"),
                mkp=item.get("mkp"),
                hipr=item.get("hipr"),
                lopr=item.get("lopr"),
                trqu=item.get("trqu"),
                trPrc=item.get("trPrc"),
                mrktTotAmt=item.get("mrktTotAmt"),
                nPptTotAmt=item.get("nPptTotAmt"),
                stLstgCnt=item.get("stLstgCnt"),
                bssIdxIdxNm=item.get("bssIdxIdxNm"),
                bssIdxClpr=item.get("bssIdxClpr"),
                basDt=item.get("basDt"),
                clpr=item.get("clpr"),
                vs=item.get("vs"),
            )
            for item in raw_items
        ]
        return ProductEtfData(
            items=items,
            source=ProductSource("PRODUCT_ETF"),
            fetched_at=Timestamp(datetime.now())
        )