import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from data.db_session import SqlAlchemyBase


class Request(SqlAlchemyBase):
    __tablename__ = "requests"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("request_type.id"), nullable=False)
    type = orm.relationship('RequestType')
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("inventory.id"), nullable=False)
    item = orm.relationship('Inventory')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    user = orm.relationship('User')
    state_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("request_state.id"), nullable=False)
    state = orm.relationship('RequestState')

class RequestForm(FlaskForm):
    type = SelectField('Тип заявки',
                       choices=[(1, 'Выдача'), (2, 'Ремонт'), (3, 'Замена')],
                       validators=[DataRequired()])
    submit = SubmitField('Создать')
