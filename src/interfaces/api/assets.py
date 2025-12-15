from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.domain import models
from src.application import schemas
from src.interfaces.api.auth import get_current_user
from src.infrastructure.database import get_db

router = APIRouter(prefix="/assets", tags=["assets"])

# Mock 자산 데이터
MOCK_ASSETS = [
    {"id": 1, "name": "카카오뱅크 입출금", "type": "예금", "balance": 2450000, "institution": "카카오뱅크"},
    {"id": 2, "name": "신한은행 정기예금", "type": "예금", "balance": 5000000, "institution": "신한은행"},
    {"id": 3, "name": "토스 26주적금", "type": "적금", "balance": 3200000, "institution": "토스뱅크"},
    {"id": 4, "name": "삼성전자 주식", "type": "주식", "balance": 1500000, "institution": "한국투자증권"},
    {"id": 5, "name": "비트코인", "type": "암호화폐", "balance": 300000, "institution": "업비트"},
]

@router.get("/")
def get_assets(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Mock 데이터 반환 (실서비스에서는 DB 조회)
    return MOCK_ASSETS

@router.post("/", response_model=schemas.AssetResponse)
def create_asset(asset: schemas.AssetCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_asset = models.Asset(**asset.dict(), user_id=current_user.id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.user_id == current_user.id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"message": "Asset deleted"}

