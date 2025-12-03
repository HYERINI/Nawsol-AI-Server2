from fastapi import APIRouter, Body

from ecos.application.factory.fetch_ecos_data_usecase_factory import FetchEcosDataUsecaseFactory

ecos_data_router = APIRouter(tags=["ecos"])

@ecos_data_router.get("/exchange_rate")
async def get_exchange_rate():
    usecase = FetchEcosDataUsecaseFactory.create()
    result = await usecase.get_exchange_rate()

    return {
        "source": result.source,
        "fetched_at": result.fetched_at.timestamp.isoformat(),
        "items": [
            {
                "item_type": item.item_type,
                "time": item.time,
                "value": item.value
            } for item in result.items
        ]
    }

@ecos_data_router.post("/exchange_rate/save")
async def fetch_and_save_exchange_rate(
        start:str | None = Body(None),
        end:str | None = Body(None)
):
    """
    ECOS API에서 환율 데이터를 조회하고 데이터베이스에 저장합니다.
    """
    usecase = FetchEcosDataUsecaseFactory.create()
    saved_entities = await usecase.fetch_and_save_exchange_rate(start, end)
    
    return {
        "message": "환율 데이터가 성공적으로 저장되었습니다.",
        "saved_count": len(saved_entities),
        "items": [
            {
                "exchange_type": entity.exchange_type.value,
                "exchange_rate": entity.exchange_rate,
                "erm_date": entity.erm_date.isoformat(),
                "created_at": entity.created_at.isoformat()
            } for entity in saved_entities
        ]
    }


@ecos_data_router.get("/interest_rate")
async def get_interest_rate():
    usecase = FetchEcosDataUsecaseFactory.create()
    result = await usecase.get_interest_rate()

    return {
        "source": result.source,
        "fetched_at": result.fetched_at.timestamp.isoformat(),
        "items": [
            {
                "item_type": item.item_type,
                "time": item.time,
                "value": item.value
            } for item in result.items
        ]
    }

@ecos_data_router.get("/exchange_rate_by_date/{date}")
async def get_exchange_rate_db(date:str):
    usecase = FetchEcosDataUsecaseFactory.create()
    result = usecase.get_exchange_rate_by_date(date)
    return result

@ecos_data_router.post("/interest_rate/save")
async def fetch_and_save_interest_rate(
        start:str | None = Body(None),
        end:str | None = Body(None)
):
    """
    ECOS API에서 환율 데이터를 조회하고 데이터베이스에 저장합니다.
    """
    usecase = FetchEcosDataUsecaseFactory.create()
    saved_entities = await usecase.fetch_and_save_interest_rate(start, end)

    return {
        "message": "금리 데이터가 성공적으로 저장되었습니다.",
        "saved_count": len(saved_entities),
        "items": [
            {
                "exchange_type": entity.interest_type,
                "exchange_rate": entity.interest_rate,
                "erm_date": entity.erm_date.isoformat(),
                "created_at": entity.created_at.isoformat()
            } for entity in saved_entities
        ]
    }