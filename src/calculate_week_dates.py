import datetime
from typing import Optional


def get_next_week_range(base_date: Optional[datetime.date] = None):
    """
    Изчислява датите за следващия понеделник и следващата неделя
    спрямо дадена дата (или днешната, ако не е посочена).

    Връща низ във формат 'DD-MM-DD-MM'.
    """
    
    # 1. Ако не е подадена дата, вземи днешната
    if base_date is None:
        today = datetime.date.today()
    else:
        today = base_date

    # 2. Намери колко дни има до *следващия* понеделник
    # .weekday() връща: 0 за Понеделник, 1 за Вторник, ..., 6 за Неделя
    # Ако днес е Събота (5), 7 - 5 = 2. Ще добавим 2 дни.
    # Ако днес е Понеделник (0), 7 - 0 = 7. Ще добавим 7 дни.
    # Ако днес е Неделя (6), 7 - 6 = 1. Ще добавим 1 ден.
    days_until_monday = 7 - today.weekday()
    
    # 3. Изчисли датата на следващия понеделник
    next_monday = today + datetime.timedelta(days=days_until_monday)
    
    # 4. Неделята е 6 дни след този понеделник
    next_sunday = next_monday + datetime.timedelta(days=6)
    
    # 5. Форматирай резултата
    monday_str = next_monday.strftime('%d-%m')
    sunday_str = next_sunday.strftime('%d-%m')
    
    return f"{monday_str}-{sunday_str}"
