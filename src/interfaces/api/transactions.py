from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.domain import models
from src.application import schemas
from src.interfaces.api.auth import get_current_user
from src.infrastructure.database import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/transactions", tags=["transactions"])

# Mock 거래내역 데이터
MOCK_TRANSACTIONS = [
    {"id": 1, "description": "스타벅스 커피", "amount": -5500, "category": "카페", "date": (datetime.now() - timedelta(days=0)).isoformat()},
    {"id": 2, "description": "급여", "amount": 3500000, "category": "수입", "date": (datetime.now() - timedelta(days=1)).isoformat()},
    {"id": 3, "description": "배달의민족", "amount": -28000, "category": "배달음식", "date": (datetime.now() - timedelta(days=1)).isoformat()},
    {"id": 4, "description": "카카오택시", "amount": -15000, "category": "택시비", "date": (datetime.now() - timedelta(days=2)).isoformat()},
    {"id": 5, "description": "GS25 편의점", "amount": -8500, "category": "편의점", "date": (datetime.now() - timedelta(days=2)).isoformat()},
    {"id": 6, "description": "넷플릭스 구독", "amount": -17000, "category": "구독", "date": (datetime.now() - timedelta(days=3)).isoformat()},
    {"id": 7, "description": "쿠팡 쇼핑", "amount": -89000, "category": "쇼핑", "date": (datetime.now() - timedelta(days=4)).isoformat()},
    {"id": 8, "description": "이마트 장보기", "amount": -156000, "category": "마트", "date": (datetime.now() - timedelta(days=5)).isoformat()},
    {"id": 9, "description": "월세", "amount": -700000, "category": "주거비", "date": (datetime.now() - timedelta(days=7)).isoformat()},
    {"id": 10, "description": "카카오뱅크 적금", "amount": -300000, "category": "저축", "date": (datetime.now() - timedelta(days=7)).isoformat()},
]

@router.get("/")
def get_transactions(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Mock 데이터 반환 (실서비스에서는 DB 조회)
    return MOCK_TRANSACTIONS

@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.dict(), user_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == current_user.id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted"}

