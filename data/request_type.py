import sqlalchemy

from data.db_session import SqlAlchemyBase


class RequestType(SqlAlchemyBase):
    __tablename__ = "request_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
