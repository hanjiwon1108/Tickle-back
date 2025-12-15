from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.domain import models
from src.infrastructure import auth
from src.interfaces.api.auth import get_current_user
from src.infrastructure.database import get_db

router = APIRouter(prefix="/analysis", tags=["analysis"])

# Mock 카테고리별 지출 데이터
MOCK_SPENDING_BY_CATEGORY = [
    {"category": "배달음식", "amount": 320000},
    {"category": "카페", "amount": 85000},
    {"category": "쇼핑", "amount": 250000},
    {"category": "택시비", "amount": 120000},
    {"category": "마트", "amount": 180000},
    {"category": "구독", "amount": 45000},
    {"category": "편의점", "amount": 65000},
    {"category": "주거비", "amount": 700000},
]

@router.get("/spending-by-category")
def get_spending_by_category(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Mock 데이터 반환 (실서비스에서는 DB 조회)
    return MOCK_SPENDING_BY_CATEGORY

@router.get("/monthly-summary")
def get_monthly_summary(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Mock 월간 요약 데이터
    return {
        "total_balance": 12450000,
        "monthly_savings": 850000,
        "investment_return": 15.2
    }

