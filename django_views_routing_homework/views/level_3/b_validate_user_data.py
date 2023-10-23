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
from typing import Any
from django.forms import ValidationError
from django.http import HttpRequest, JsonResponse
from django.core.validators import validate_email


def validate_full_name(data: dict[str, Any]) -> None:
    full_name = data.get('full_name')
    if not full_name:
        raise ValidationError('no full_name')
    
    if len(full_name) < 5 or len(full_name) > 256:
        raise ValidationError('incorrected full_name lengs (not less then 4 not more then 256)')


def to_validate_email(data: dict[str, Any]) -> None:
    email = data.get('email')
    if not email:
        raise ValidationError('no email')
    validate_email(email)


def validate_registered_from(data: dict[str, Any]) -> None:
    source_of_registration = {'website', 'mobile_app'}
    registered_from = data.get('registered_from')
    if not registered_from:
        raise ValidationError('no registered_from')
    if registered_from not in source_of_registration:
        raise ValidationError('incorrect source of registration')


def valide_age(data: dict[str, Any]) -> None:
    age = data.get('age')
    if not age:
        return None
    try:
        int(age)
    except ValueError:
        raise ValidationError("age should be int")
    

def validate_if_no_other_fields(data: dict[str, Any]) -> None:
    num_keys = len(data.keys())
    if num_keys > 4:
        raise ValidationError('redundant fields')


def get_result_of_validation(data: dict[str, Any]) -> None:
    validate_full_name(data)
    to_validate_email(data)
    validate_registered_from(data)
    valide_age(data)
    validate_if_no_other_fields(data)
    

def validate_user_data_view(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse('Bad Request', status=400, safe=False)
    
    try:
        get_result_of_validation(data)
    except ValidationError:
        return JsonResponse({"is_valid":"false"}, status=200, safe=False)
    
    return JsonResponse({"is_valid":"true"}, status=200, safe=False)