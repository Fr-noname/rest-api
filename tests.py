import datetime

from requests import get, post, delete


def main():
    print('get')

    print(get('http://127.0.0.1:5000/api/jobs').json())  # работает
    print(get('http://127.0.0.1:5000/api/job/1').json())  # работает
    print(get('http://127.0.0.1:5000/api/job/9999999999999999').json())  # ошибка Bad request
    print(get('http://127.0.0.1:5000/api/job/r').json())  # ошибка 404, т.к. передаем строку, а не число

    print('post')

    print(post('http://127.0.0.1:5000/api/jobs/post', json={}).json())  # ошибка Empty request

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'title': 'Заголовок'}).json())  # ошибка Bad request, левые данные

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'id': 2,}).json())  # ошибка Bad request, недостаточно данных

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'id': 2,
                     'team_leader': 1,
                     'job': 'none',
                     'work_size': 12,
                     'collaborators': '1',
                     'start_date': '2025-05-17 00:00:00',
                     'end_date': '2025-05-17 00:00:00',
                     'is_finished': True}).json())  # работает.
    print(get('http://127.0.0.1:5000/api/jobs').json())  # добавили работу, проверка

    print('delete')

    print(delete('http://localhost:5000/api/jobs/del/999').json())  # работы с id = 999 нет в базе
    print(delete('http://localhost:5000/api/jobs/del').json())  # ошибка 404, т.к. ничего не передаём
    print(delete('http://localhost:5000/api/jobs/del/r').json())  # ошибка 404, т.к. передаем строку, а не число

    print(get('http://127.0.0.1:5000/api/jobs').json())  # все работы до удаления работы с id 1
    print(delete('http://localhost:5000/api/jobs/del/1').json())
    print(get('http://127.0.0.1:5000/api/jobs').json())  # все работы после удаления работы с id 1

    print('вернём сё на круги своя')

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'id': 1,
                     'team_leader': 1,
                     'job': 'ывфв',
                     'work_size': 24,
                     'collaborators': '1',
                     'start_date': '1-05-17 00:00:00',
                     'end_date': '1000000000-05-19 00:00:00',
                     'is_finished': True}).json())  # Вернем новость с id == 1 для будущих поколений.
    print(delete('http://localhost:5000/api/jobs/del/2').json())  # удалим работу для будущих поколений


if __name__ == '__main__':
    main()
