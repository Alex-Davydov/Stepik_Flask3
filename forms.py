from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField, validators

from helper_data import goals


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', validators=[validators.InputRequired()])
    phone = StringField('Ваш телефон', validators=[validators.InputRequired(),
                                                   validators.Length(min=6, max=12,
                                                                     message='Телефонный номер должен быть от 6 до 11 символов')])
    clientWeekday = HiddenField('clientWeekday')
    clientTime = HiddenField('clientTime')
    clientTeacher = HiddenField('clientTeacher')
    submit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    goal = RadioField('Какая цель занятий?', choices=(goals.items()))
    time = RadioField('Сколько времени есть?', choices=(('1-2', '1-2 часа в неделю'), ('3-5', '3-5 часов в неделю'),
                                                        ('5-7', '5-7 часов в неделю'), ('7-10', '7-10 часов в неделю')))
    name = StringField('Вас зовут', validators=[validators.InputRequired()])
    phone = StringField('Ваш телефон', validators=[validators.InputRequired(),
                                                   validators.Length(min=6, max=12,
                                                                     message='Телефонный номер должен быть от 6 до 12 символов')])
    submit = SubmitField('Найдите мне преподавателя')
