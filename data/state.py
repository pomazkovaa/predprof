import sqlalchemy

from data.db_session import SqlAlchemyBase


class State(SqlAlchemyBase):
    __tablename__ = "state"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)