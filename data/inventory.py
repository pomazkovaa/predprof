import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from data.db_session import SqlAlchemyBase


class Inventory(SqlAlchemyBase):
    __tablename__ = "inventory"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    state = sqlalchemy.Column(sqlalchemy.String, nullable=False)

class InventoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    state = SelectField('Состояние',
                        choices=[('Новый', 'Новый'), ('Используемый', 'Используемый'), ('Сломанный', 'Сломанный')],
                        validators=[DataRequired()])
    submit = SubmitField('Добавить')
