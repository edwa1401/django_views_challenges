"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

from django.http import HttpRequest, JsonResponse
import requests


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> JsonResponse:
    url = f'https://api.github.com/users/{github_username}'

    git_raw_response = requests.get(url)
    git_response = git_raw_response.json()
    if 'name' not in git_response:
        return JsonResponse({}, status=404)
    full_name = git_response['name']
    
    return JsonResponse({'name': full_name})