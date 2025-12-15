from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.domain import models
from src.application import schemas
from src.interfaces.api.auth import get_current_user
from src.infrastructure.database import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/unread-count")
def get_unread_count(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications
    """
    count = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == 0
    ).count()
    return {"unread_count": count}

@router.get("/", response_model=List[schemas.NotificationResponse])
def get_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    unread_only: bool = False
):
    """
    Get user's notifications
    - unread_only: If True, only return unread notifications
    """
    query = db.query(models.Notification).filter(models.Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(models.Notification.is_read == 0)
    
    notifications = query.order_by(models.Notification.created_at.desc()).all()
    return notifications

@router.get("/{notification_id}", response_model=schemas.NotificationResponse)
def get_notification(
    notification_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific notification
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return notification

@router.post("/", response_model=schemas.NotificationResponse)
def create_notification(
    notification: schemas.NotificationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create new notification (for testing/admin purposes)
    """
    db_notification = models.Notification(
        user_id=current_user.id,
        type=notification.type,
        title=notification.title,
        message=notification.message,
        is_read=0
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark notification as read
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = 1
    db.commit()
    db.refresh(notification)
    return {"message": "Notification marked as read"}

@router.put("/read-all")
def mark_all_as_read(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all unread notifications as read
    """
    db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == 0
    ).update({"is_read": 1})
    db.commit()
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete notification
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted"}

@router.delete("/")
def delete_all_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete all notifications for current user
    """
    db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "All notifications deleted"}
