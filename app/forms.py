from flask_wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length

class LoginForm (Form):
    openid = TextField('openid',validators = [Required()])
    remember_me = BooleanField ('remember_me', default = False)

#Импортированный Required — это валидатор, функция, которая может быть прикреплена
#к полю, для выполнения валидации данных отправленных пользователем.
# Валидатор Required просто проверяет, что поле не было отправлено пустым.

class EditForm(Form):
    nickname = TextField('nickname', validators=[Required()])
    about_me = TextAreaField ('about_me', validators= [Length(min=0, max= 140)])