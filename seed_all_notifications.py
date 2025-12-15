from src.infrastructure.database import SessionLocal
from src.domain import models
from datetime import datetime, timedelta

db = SessionLocal()

# 모든 사용자에게 알림 추가
users = db.query(models.User).all()

for user in users:
    # 이미 알림이 있는 사용자는 스킵
    existing = db.query(models.Notification).filter(models.Notification.user_id == user.id).first()
    if existing:
        print(f'✓ User ID {user.id} ({user.name})는 이미 알림이 있습니다.')
        continue
    
    notifications = [
        models.Notification(
            user_id=user.id,
            type='recommendation',
            title='새로운 추천 상품이 있습니다',
            message='최근 지출 패턴을 분석하여 높은 이자율의 정기예금 상품을 추천드립니다.',
            is_read=0,
            created_at=datetime.utcnow()
        ),
        models.Notification(
            user_id=user.id,
            type='alert',
            title='이번 달 커피 지출 증가',
            message='이번 달 카페 지출이 지난 달 대비 15% 증가했습니다. 예산 관리를 고려해보세요.',
            is_read=0,
            created_at=datetime.utcnow() - timedelta(hours=2)
        ),
        models.Notification(
            user_id=user.id,
            type='info',
            title='월간 자산 리포트 준비 완료',
            message='12월 월간 자산 리포트가 준비되었습니다. 분석 페이지에서 확인하세요.',
            is_read=1,
            created_at=datetime.utcnow() - timedelta(days=1)
        ),
        models.Notification(
            user_id=user.id,
            type='recommendation',
            title='목표 달성을 위한 저축 계획',
            message='현재 지출 수준으로 계획 중인 저축 목표를 달성하려면 월간 7,000,000원의 저축이 필요합니다.',
            is_read=0,
            created_at=datetime.utcnow() - timedelta(hours=5)
        ),
        models.Notification(
            user_id=user.id,
            type='alert',
            title='구독료 자동 결제 예정',
            message='내일 오전 10시에 구독 서비스(넷플릭스, 스포티파이 등) 자동 결제가 예정되어 있습니다.',
            is_read=1,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        models.Notification(
            user_id=user.id,
            type='info',
            title='AI 금융 상담 결과',
            message='금융 상담 AI가 당신의 자산 포트폴리오를 분석했습니다. AI 상담 페이지에서 자세히 확인하세요.',
            is_read=0,
            created_at=datetime.utcnow() - timedelta(hours=12)
        ),
    ]
    
    db.add_all(notifications)
    db.commit()
    print(f'✓ User ID {user.id} ({user.name})에 6개의 알림이 추가되었습니다.')

db.close()
print('\n✅ 모든 사용자에게 알림 데이터가 추가되었습니다!')
