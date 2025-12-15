#!/bin/bash

echo "=== 현재 데이터 확인 ==="
python3 check_data.py

echo ""
echo "=== 알림 추가 ==="
python3 seed_notifications.py

echo ""
echo "=== 최종 데이터 확인 ==="
python3 check_data.py
