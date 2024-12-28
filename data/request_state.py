import sqlalchemy

from data.db_session import SqlAlchemyBase


class RequestState(SqlAlchemyBase):
    __tablename__ = "request_state"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
