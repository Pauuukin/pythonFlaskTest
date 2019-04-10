#!flask/bin/python

from app import app
app.run(debug=True) #app - переменная класса Flask

#Скрипт мпортирует переменную app
# и вызывает метод run чтобы запустить сервер