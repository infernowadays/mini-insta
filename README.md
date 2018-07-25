# Project mini-insta - Проект стажировки в компании Indev Group

mini-insta - backend для социальной сети, клонирующей часть функционала всеми известного Instagram'a. 
Данный проект выполнен в учебных целях для получения навыков работы с Django REST framework Python3.

Возможности проекта:
- Регистрация и вход пользователей через систему приложения
- Регистрация и вход пользователей через социальные сети(0Auth) Facebook, GitHub
- Просмотр новостей
- Создание постов
- Оценивание и комментирование постов

## Installation
Debian or Ubuntu:

#### Get project from GitHub
```
$ git clone https://github.com/maximus1998g/mini-insta.git
```

#### Python installation
```
$ sudo apt install python3.6
```

#### Virtual environment
```
$ python3 -m venv env

```

#### Django & necessary packages installation
```
$ source env/bin/activate
(env) ~$ python3 -m pip install --upgrade pip
(env) ~$ pip install -r requirements.txt
```

#### Run project
```
(env) ~/mini-insta$ python manage.py runserver
```
