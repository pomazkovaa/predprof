import sqlalchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.simple import SubmitField

from wtforms import StringField, IntegerField

from data.db_session import SqlAlchemyBase


class Procurement(SqlAlchemyBase):
    __tablename__ = "procurement"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    good = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    seller = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class ProcurementAddForm(FlaskForm):
    good = StringField('Товар', validators=[DataRequired()])
    price = IntegerField('Цена, ₽', validators=[DataRequired()])
    seller = StringField('Поставщик', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ProcurementEditForm(FlaskForm):
    good = StringField('Товар', validators=[DataRequired()])
    price = IntegerField('Цена, ₽', validators=[DataRequired()])
    seller = StringField('Поставщик', validators=[DataRequired()])
    submit = SubmitField('Изменить')
