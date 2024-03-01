# Установите psycopg2, если еще не установлен
# pip install psycopg2

import psycopg2

try:
    # Подключение к базе данных PostgreSQL
    connection = psycopg2.connect(
        dbname='my_page',
        user='erik',
        password='Erikman2002',
        host='localhost',
        port='5432'
    )

    # Создание курсора
    cursor = connection.cursor()

    # Создание базы данных elderco
    cursor.execute("CREATE DATABASE my_page")

    # Закрытие курсора
    cursor.close()

    # Подтверждение транзакции
    connection.commit()

    print("All Done!")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Закрытие подключения
    if connection:
        connection.close()
