from src.infrastructure.database import SessionLocal
from src.domain import models

db = SessionLocal()

# Show all users
users = db.query(models.User).all()
print("=== 모든 사용자 ===")
for user in users:
    print(f"ID: {user.id}, Email: {user.email}, Name: {user.name}")

# Show all notifications
notifications = db.query(models.Notification).all()
print(f"\n=== 모든 알림 ({len(notifications)}개) ===")
for notif in notifications:
    print(f"User ID: {notif.user_id}, Title: {notif.title}, Read: {notif.is_read}")

db.close()
