import pytest
from fastapi.testclient import TestClient
from API_GetDate import app
from SyncPeriodData import sync_period_data
from database import get_db_connection, insert_exchange_rate
from datetime import datetime

client = TestClient(app)

def test_report_generation():
    """Тестирует генерацию отчета по курсам валют."""
    connection = get_db_connection()

    date1 = datetime.strptime("11.03.2025", "%d.%m.%Y").date()
    date2 = datetime.strptime("12.03.2025", "%d.%m.%Y").date()
    
    insert_exchange_rate(connection, date1, "USD", 1, 22.123)
    insert_exchange_rate(connection, date2, "USD", 1, 22.456)
    connection.close()

    response = client.post("/report", json={"start_date": "11.03.2025", "end_date": "12.03.2025", "currencies": ["USD"]})
    data = response.json()
    
    assert "USD" in data
    assert data["USD"]["min"] > 0
    assert data["USD"]["max"] > 0
    assert round(data["USD"]["avg"], 3) > 0

def test_sync_period_data():
    # Очистим данные
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM exchange_rates")
    connection.commit()

    allowed_currencies = ["USD", "EUR"]
    sync_period_data("14.03.2025", "17.03.2025", allowed_currencies)

    # Проверка данных в БД
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM exchange_rates WHERE date = '2025-03-14'")
        count = cursor.fetchone()[0]
    connection.close()
    
    assert count > 0

    # Уберём за собой мусор
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM exchange_rates")
    connection.commit()