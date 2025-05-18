import datetime

from requests import get, post


def main():
    print('get')

    print(get('http://127.0.0.1:5000/api/jobs').json())
    print(get('http://127.0.0.1:5000/api/job/1').json())
    print(get('http://127.0.0.1:5000/api/job/9999999999999999').json())
    print(get('http://127.0.0.1:5000/api/job/e').json())

    print('post')
    print(post('http://127.0.0.1:5000/api/jobs/post', json={}).json())

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'title': 'Заголовок'}).json())

    print(post('http://127.0.0.1:5000/api/jobs/post',
               json={'id': 1,
                     'team_leader': 1,
                     'job': 'none',
                     'work_size': 12,
                     'collaborators': '1',
                     'start_date': '2025-05-17 00:00:00',
                     'is_finished': True}).json())
    # print(get(ADDRESS).json())


if __name__ == '__main__':
    main()
