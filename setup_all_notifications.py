from src.infrastructure.database import SessionLocal
from src.domain import models
from datetime import datetime, timedelta

db = SessionLocal()

# First, check existing data
users = db.query(models.User).all()
notifications = db.query(models.Notification).all()

print("="*50)
print("현재 데이터 확인")
print("="*50)
print(f"\n총 사용자: {len(users)}명")
for user in users:
    user_notifs = [n for n in notifications if n.user_id == user.id]
    print(f"  - {user.name} ({user.email}): {len(user_notifs)}개 알림")

print(f"\n총 알림: {len(notifications)}개")

# Delete all existing notifications first
print("\n기존 알림 삭제 중...")
db.query(models.Notification).delete()
db.commit()

# Add new notifications to all users
if users:
    print(f"\n✅ {len(users)}명의 사용자에게 알림을 추가합니다...\n")
    
    total_added = 0
    for user in users:
        notifications = [
            models.Notification(
                user_id=user.id,
                type="recommendation",
                title="새로운 추천 상품이 있습니다",
                message="최근 지출 패턴을 분석하여 높은 이자율의 정기예금 상품을 추천드립니다.",
                is_read=0,
                created_at=datetime.utcnow()
            ),
            models.Notification(
                user_id=user.id,
                type="alert",
                title="이번 달 커피 지출 증가",
                message="이번 달 카페 지출이 지난 달 대비 15% 증가했습니다. 예산 관리를 고려해보세요.",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(hours=2)
            ),
            models.Notification(
                user_id=user.id,
                type="info",
                title="월간 자산 리포트 준비 완료",
                message="12월 월간 자산 리포트가 준비되었습니다. 분석 페이지에서 확인하세요.",
                is_read=1,
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            models.Notification(
                user_id=user.id,
                type="recommendation",
                title="목표 달성을 위한 저축 계획",
                message="현재 지출 수준으로 계획 중인 저축 목표를 달성하려면 월간 7,000,000원의 저축이 필요합니다.",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(hours=5)
            ),
            models.Notification(
                user_id=user.id,
                type="alert",
                title="구독료 자동 결제 예정",
                message="내일 오전 10시에 구독 서비스(넷플릭스, 스포티파이 등) 자동 결제가 예정되어 있습니다.",
                is_read=1,
                created_at=datetime.utcnow() - timedelta(days=2)
            ),
            models.Notification(
                user_id=user.id,
                type="info",
                title="AI 금융 상담 결과",
                message="금융 상담 AI가 당신의 자산 포트폴리오를 분석했습니다. AI 상담 페이지에서 자세히 확인하세요.",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(hours=12)
            ),
        ]
        
        db.add_all(notifications)
        db.commit()
        total_added += len(notifications)
        print(f"✅ {user.name} ({user.email}): {len(notifications)}개 알림 추가")
    
    print(f"\n총 {total_added}개의 알림이 추가되었습니다!")
    
    # Show final result
    print("\n" + "="*50)
    print("최종 데이터")
    print("="*50)
    final_notifs = db.query(models.Notification).all()
    print(f"\n총 알림: {len(final_notifs)}개")
    for user in users:
        user_notifs = [n for n in final_notifs if n.user_id == user.id]
        print(f"  - {user.name}: {len(user_notifs)}개 알림")
else:
    print("❌ 사용자가 없습니다.")

db.close()
