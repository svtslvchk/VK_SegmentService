# Сервис сегментации пользователей

## Описание

Этот сервис предназначен для управления пользователями и их принадлежностью к различным сегментам. Он разработан для поддержки аналитических задач. 

Сервис позволяет:

- Создавать и удалять сегменты
- Добавлять пользователей в сегменты и удалять их из них
- Распределять сегмент случайным образом на определённый процент пользователей
- Получать информацию о том, в каких сегментах состоит пользователь

## Инструкция

1. Клонируйте репозиторий

2. Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows

3. Установите зависимости (находятся в файле requirements.txt)

Для этого пропишите в терминале:
pip install -r requirements.txt

4.Запустите сервер

uvicorn main:app --reload

5. Откройте документацию

http://127.0.0.1:8000/docs


## Примеры запросов

-Создание пользователя
POST /users/
Content-Type: application/json

{
  "name": "Alice"
}

-Создание сегмента
POST /segments/
Content-Type: application/json

{
  "name": "MAIL_GPT"
}

-Добавить пользователя в сегмент (связать пользователя и сегмент)
POST /users/assign/
Content-Type: application/json

{
  "user_id": 1,
  "segment_id": 2
}

-Удалить пользователя из сегмента
DELETE /users/unassign/
Content-Type: application/json

{
  "user_id": 1,
  "segment_id": 2
}

-Получить пользователя и его сегменты (по id пользователя)
GET /users/1 # здесь 1 - это id пользователя

-Получить всех пользователей в сегменте (по id сегмента)
GET /segments/by-segment/2 # здесь 2 - это id сегмента

-Распределить сегмент на 30% случайных пользователей
POST /distribute/
Content-Type: application/json

{
  "segment_id": 2,
  "percentage": 30
}




