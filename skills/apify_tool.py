from datetime import datetime

def is_holiday_today():
    # 5 = Saturday, 6 = Sunday
    today = datetime.now().weekday()
    if today >= 5:
        return True
    return False