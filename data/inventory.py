import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Inventory(SqlAlchemyBase):
    __tablename__ = "inventory"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    state_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("state.id"), nullable=False)
    state = orm.relationship('State')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    user = orm.relationship('User')


class InventoryAddForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class InventoryEditForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    state = SelectField('Состояние',
                        choices=[(1, 'Новый'), (2, 'Используемый'), (3, 'Сломанный')],
                        coerce=int, validators=[DataRequired()])
    user = SelectField('Закрепить за пользователем', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Изменить')
