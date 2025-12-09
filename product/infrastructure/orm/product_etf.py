from datetime import datetime

from sqlalchemy import Column, String, BigInteger, DateTime, Integer, Float

from config.database.session import Base


class ProductETFORM(Base):
    __tablename__ = "product_etf"
    id = Column(Integer, primary_key=True, index=True)
    fltRt = Column(Float, nullable=True)               # 등락율
    nav = Column(Float, nullable=True)                 # 순자산가치(NAV)
    mkp = Column(Integer, nullable=True)               # 시가
    hipr = Column(Integer, nullable=True)              # 고가
    lopr = Column(Integer, nullable=True)              # 저가
    trqu = Column(Integer, nullable=True)              # 거래량
    trPrc = Column(BigInteger, nullable=True)                # 거래대금
    mrktTotAmt = Column(BigInteger, nullable=True)           # 시가총액
    nPptTotAmt = Column(BigInteger, nullable=True)            # 순자산총액
    stLstgCnt = Column(BigInteger, nullable=True)            # 상장좌수
    bssIdxIdxNm = Column(String(255), nullable=True)   # 기초지수_지수명
    bssIdxClpr = Column(Float, nullable=True)          # 기초지수_종가
    basDt = Column(DateTime, default=datetime.utcnow)  # 기준일자
    clpr = Column(Integer, nullable=True)               # 종가
    vs = Column(Integer, nullable=True)                # 대비

    def __repr__(self):
        return f"<ProductETFORM id={self.id}>"