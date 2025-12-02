from fastapi import APIRouter

from ieinfo.application.usecase.ie_info_usecase import IEInfoUseCase

ie_info_router = APIRouter()
usecase = IEInfoUseCase().get_instance()
