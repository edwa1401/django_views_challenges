"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from faker import Faker


def create_text(length: int) -> list[str]:
    max_num_chars_in_line = length
    if length < 5:
        length = 5
      # ограничение параметра max_nb_chars в faker.text

    text=Faker().texts(max_nb_chars=max_num_chars_in_line)
    return text

# попробовал две разных функции Faker использовать, обе не дают текст заданной длины (по числу символов),
# взял words как более простой

def create_words(num_words: int) -> str:
    text = Faker().words(num_words)
    return '\n'.join(text)

def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:

    length: str = request.GET.get('length')
    
    if not length:
        return HttpResponseForbidden('missing lenght')
    
    if not length.isdigit():
        return HttpResponseBadRequest('length must be int')
    
    length = int(length)
    if length > 256:
        return HttpResponseForbidden('length must be < 256')

    response = HttpResponse(
        content_type='text/plain',
        headers={'Content-Disposition': 'attachment; filename="random_text.txt"'},
    )
    write_text = create_words(length)
    response.write(write_text)

    return response

    
    
