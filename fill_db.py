import os
from data import db_session
from data.users import User


def main():
    if not os.path.exists("db"):
        os.makedirs("db")
        db_session.global_init("db/base.sqlite")

        user = User()
        user.login = 'admin'
        user.set_password("12345678")
        user.is_admin = True

        session = db_session.create_session()
        session.add(user)
        session.commit()
    else:
        print("База уже существует!")


if __name__ == '__main__':
    main()