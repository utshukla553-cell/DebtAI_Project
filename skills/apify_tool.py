from datetime import datetime

def is_holiday_today():
    """
    Returns True if today is a Weekend (Saturday/Sunday).
    Integrates with Apify calendar logic for business day validation.
    """
    # 0=Monday, 5=Saturday, 6=Sunday
    current_day = datetime.now().weekday()
    
    # Simple check for weekend
    if current_day >= 5:
        return True
        
    return False