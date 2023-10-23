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

from io import BytesIO
from django.http import FileResponse, HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from faker import Faker


def create_text(length: int) -> list[str]:
    
    if length < 5:
        length = 5
      # ограничение параметра max_nb_chars в faker.text

    max_num_chars_in_line = length

    text=Faker().text(max_nb_chars=max_num_chars_in_line)

    return text


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:

    length = request.GET.get('length')
    
    if not length:
        return HttpResponseBadRequest('missing lenght')
    
    if not length.isdigit():
        return HttpResponseBadRequest('length must be int')
    
    length = int(length)
    if length > 10000:
        return HttpResponseBadRequest('length must be < 10000')
    
    write_text = create_text(length)
    
    text_file = BytesIO(write_text.encode("utf-8"))
    text_file.seek(0)
    response = FileResponse(text_file,filename="random_text.txt",as_attachment=True)

    return response

    
    
