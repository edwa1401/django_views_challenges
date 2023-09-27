"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
import json
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed, QueryDict
from typing import Any
import re


def is_valid_full_name(full_name: str) -> bool:
    return len(full_name) >= 5 and len(full_name)<= 256

def is_valid_email(email: str) -> bool:
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) is not None

def is_valid_registered_from(registered_from: str) -> bool:
    return registered_from == 'website' or registered_from == 'mobile_app'

def is_valid_age(age: str | None) -> bool:
    if age is None:
        return True
    try:
        int(age)
        return True
    except ValueError:
        return False

def check_no_other_fields(request_: QueryDict) -> bool:
    num_keys = len(request_.keys())
    return num_keys <= 4

def get_result_of_validation(
        data: dict[str, str],
        full_name: str,
        email: str,
        registered_from: str,
        age: str | None) -> dict[str, str]:
    
    if not is_valid_full_name(full_name):
        return {'is_valid:false'}
    if not is_valid_email(email):
        return {'is_valid:false'}
    if not is_valid_registered_from(registered_from):
        return {'is_valid:false'}
    if not is_valid_age(age):
        return {'is_valid:false'}
    if not check_no_other_fields(data):
        return {'is_valid:false'}
    else:
        return {'is_valid:true'}
    

def validate_user_data_view(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':

        data: QueryDict = request.POST
        full_name: str = data['full_name']
        email: str = data['email']
        registered_from: str = data['registered_from']
        if 'age' in data.keys():
            age: str = data['age']
        else:
            age = None
        if not all([full_name, email, registered_from]):
            return HttpResponseBadRequest()
    
        content = get_result_of_validation(data, full_name, email, registered_from, age)
        
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    return HttpResponse(content)
