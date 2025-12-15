from fastapi import APIRouter, Depends, HTTPException
from src.application.services.public_data import public_data_service
from typing import Dict, Any
from src.interfaces.api.auth import get_current_user

router = APIRouter(
    prefix="/public-data",
    tags=["public-data"],
    responses={404: {"description": "Not found"}},
)

@router.get("/deposits")
async def get_deposit_products(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    return await public_data_service.get_deposit_products()

@router.get("/savings")
async def get_saving_products(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    return await public_data_service.get_saving_products()
