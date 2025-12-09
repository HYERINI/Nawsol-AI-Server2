from typing import List

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import Session

from config.database.session import get_db_session
from product.application.port.product_repository_port import ProductRepositoryPort
from product.domain.product_etf import ProductEtf
from product.infrastructure.orm.product_bond import ProductBondORM
from product.infrastructure.orm.product_etf import ProductETFORM
from product.infrastructure.orm.product_fund import ProductFundORM


class ProductRepositoryImpl(ProductRepositoryPort):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'db'):
            self.db: Session = get_db_session()

    async def get_etf_data_by_date(self, date:str) -> List[ProductETFORM]:
        rows = (self.db.query(ProductETFORM).
                filter(func.date_format(ProductETFORM.basDt, "%Y%m%d") == date).
                all())

        return [
            ProductETFORM(
                id=row.id,
                fltRt=row.fltRt,
                nav=row.nav,
                mkp=row.mkp,
                hipr=row.hipr,
                lopr=row.lopr,
                trqu=row.trqu,
                trPrc=row.trPrc,
                mrktTotAmt=row.mrktTotAmt,
                nPptTotAmt=row.nPptTotAmt,
                stLstgCnt=row.stLstgCnt,
                bssIdxIdxNm=row.bssIdxIdxNm,
                bssIdxClpr=row.bssIdxClpr,
                basDt=row.basDt,
                clpr=row.clpr,
                vs=row.vs
            )
            for row in rows
        ]

    async def save_etf_batch(self, etf_list: List[ProductEtf]) -> List[ProductEtf]:

        if not etf_list:
            return []

        new_etf_list = []

        for etfs in etf_list:

            etfs_date_only = etfs.basDt.date() if hasattr(etfs.basDt, 'basDt') else etfs.basDt

            existing = self.db.query(ProductETFORM).filter(
                and_(
                    ProductETFORM.basDt == etfs.basDt,
                    # datetime을 날짜만 비교
                    func.DATE(ProductETFORM.basDt) == etfs_date_only,
                )
            ).first()

            # 중복이 없으면 추가
            if not existing:
                new_etf_list.append(etfs)

        if not new_etf_list:
            return etf_list

        orm_list = [
            ProductETFORM(
                fltRt=etf.fltRt,
                nav=etf.nav,
                mkp=etf.mkp,
                hipr=etf.hipr,
                lopr=etf.lopr,
                trqu=etf.trqu,
                trPrc=etf.trPrc,
                mrktTotAmt=etf.mrktTotAmt,
                nPptTotAmt=etf.nPptTotAmt,
                stLstgCnt=etf.stLstgCnt,
                bssIdxIdxNm=etf.bssIdxIdxNm,
                bssIdxClpr=etf.bssIdxClpr,
                basDt=etf.basDt,
                clpr=etf.clpr,
                vs=etf.vs
            )
            for etf in new_etf_list
        ]

        self.db.add_all(orm_list)
        self.db.commit()

        for orm_item in orm_list:
            self.db.refresh(orm_item)

        return etf_list

    async def get_fund_data_by_date(self, date:str) -> List[ProductFundORM]:
        rows = (self.db.query(ProductFundORM).
                filter(func.date_format(ProductFundORM.basDt, "%Y%m%d") == date).
                all())
        return [
            ProductFundORM(
                id=row.id,
                baseDt = row.baseDt,
                srtnCd = row.srtnCd,
                fndNm = row.fndNm,
                ctg = row.ctg,
                setpDt = row.setpDt,
                fndTp = row.fndTp,
                prdClsfCd = row.prdClsfCd,
                asoStdCd = row.asoStdCd,
            )
            for row in rows
        ]

    async def get_bond_data_by_date(self, date:str) -> List[ProductBondORM]:
        rows = (self.db.query(ProductBondORM).
                filter(func.date_format(ProductBondORM.basDt, "%Y%m%d") == date).
                all())

        return [
            ProductBondORM(
                id = row.id,
                baseDt = row.baseDt,
                crno = row.crno,
                bondIsurNm = row.bondIsurNm,
                bondIssuDt = row.bondIssuDt,
                scrsItmsKcd = row.scrsItmsKcd,
                scrsItmsKcdNm = row.scrsItmsKcdNm,
                isinCd = row.isinCd,
                isinCdNm = row.isinCdNm,
                bondIssuFrmtNm = row.bondIssuFrmtNm,
                bondExprDt = row.bondExprDt,
                bondIssuCurCd = row.bondIssuCurCd,
                bondIssuCurCdNm = row.bondIssuCurCdNm,
                bondPymtAmt = row.bondPymtAmt,
                bondIssuAmt = row.bondIssuAmt,
                bondSrfcInrt = row.bondSrfcInrt,
                irtChngDcd = row.irtChngDcd,
                irtChngDcdNm = row.irtChngDcdNm,
                bondIntTcd = row.bondIntTcd,
                bondIntTcdNm = row.bondIntTcdNm,
            )
            for row in rows
        ]
