import psycopg2
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def check_existing_rate(conn, date: date, currency_code: str):
    cursor = conn.cursor()
    query = "SELECT 1 FROM exchange_rates WHERE date = %s AND currency_code = %s LIMIT 1"
    cursor.execute(query, (date, currency_code))
    result = cursor.fetchone()
    return result is not None

def insert_exchange_rate(connection, date: date, currency_code: str, amount: int, rate: float):
    """Вставляет данные о курсе валют в базу."""
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO exchange_rates (date, currency_code, amount, rate) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (date, currency_code, amount, rate)
        )
    connection.commit()

def get_aggregated_rates(connection, start_date: date, end_date: date, currencies):
    """Получает агрегированные данные о курсах валют за период."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT currency_code, MIN(rate), MAX(rate), AVG(rate)
            FROM exchange_rates
            WHERE date >= %s AND date <= %s AND currency_code = ANY(%s)
            GROUP BY currency_code
        """, (start_date, end_date, currencies))
        return cursor.fetchall()