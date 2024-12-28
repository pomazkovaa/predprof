import os
from data import db_session
from data.request_state import RequestState
from data.request_type import RequestType
from data.state import State
from data.users import User


def main():
    if not os.path.exists("db"):
        os.makedirs("db")
        db_session.global_init("db/base.sqlite")
        session = db_session.create_session()

        user = User()
        user.login = 'admin'
        user.set_password("12345678")
        user.is_admin = True
        session.add(user)

        for name in ['Новый', 'Используемый', 'Сломанный']:
            state = State()
            state.name = name
            session.add(state)

        for name in ['Выдача', 'Ремонт', 'Замена']:
            request_type = RequestType()
            request_type.name = name
            session.add(request_type)

        for name in ['На рассмотрении', 'Одобрено', 'Отклонено']:
            request_state = RequestState()
            request_state.name = name
            session.add(request_state)

        session.commit()
    else:
        print("База уже существует!")


if __name__ == '__main__':
    main()