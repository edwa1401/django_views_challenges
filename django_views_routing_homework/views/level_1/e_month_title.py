from django.http import HttpResponse, HttpResponseNotFound


"""
Вьюха get_month_title_view возвращает название месяца по его номеру. 
Вся логика работы должна происходить в функции get_month_title_by_number.

Задания:
    1. Напишите логику получения названия месяца по его номеру в функции get_month_title_by_number
    2. Если месяца по номеру нет, то должен возвращаться ответ типа HttpResponseNotFound c любым сообщением об ошибке
    3. Добавьте путь в файле urls.py, чтобы при открытии http://127.0.0.1:8000/month-title/13/ 
       вызывалась вьюха get_month_title_view. Например http://127.0.0.1:8000/month-title/3/ 
"""

MONTHS = {
    1: 'january',
    2: 'february',
    3: 'march',
    4: 'april',
    5: 'may',
    6: 'june',
    7: 'july',
    8: 'august',
    9: 'september',
    10: 'october',
    11: 'november',
    12: 'december'
}

def get_month_title_by_number(month_number: int) -> str | None:

    if month_number in MONTHS.keys():
        return MONTHS[month_number]
    else:
        return None


def get_month_title_view(request, month_number: int):
    month = get_month_title_by_number(month_number=month_number)
    if month:
        return HttpResponse(month)

    return HttpResponseNotFound('Месяца с таким номером не существует')
