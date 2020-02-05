from flask_login import UserMixin


class User(UserMixin):
    pass


users = [
    {'id': 'admin', 'password': '12345'}
]


def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user
