import requests
from datetime import datetime, timedelta
from database import get_db_connection, insert_exchange_rate, check_existing_rate
from dotenv import load_dotenv
import os

load_dotenv()

def sync_period_data(start_date, end_date, allowed_currencies):
    conn = get_db_connection()
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(end_date, "%d.%m.%Y")
    current = start

    while current <= end:
        date_str = current.strftime("%d.%m.%Y")
        url = f"https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt?date={date_str}"
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            if len(lines) < 3:
                print(f"Нет данных для {date_str}")
                current += timedelta(days=1)
                continue
            date_from_api = " ".join(lines[0].split()[0:3])
            date_obj = datetime.strptime(date_from_api, "%d %b %Y").date()
            for line in lines[2:]:
                parts = line.split("|")
                if len(parts) >= 5:
                    currency_code = parts[3]
                    if currency_code not in allowed_currencies:
                        continue
                    amount = int(parts[2])
                    rate = float(parts[4].replace(",", "."))
                    
                    if check_existing_rate(conn, date_obj, currency_code):
                        print(f"Данные для {date_obj} и {currency_code} уже сохранены.")
                        continue
                    
                    insert_exchange_rate(conn, date_obj, currency_code, amount, rate)
                    print(f"Сохранено: {date_obj.strftime('%d.%m.%Y')} - {currency_code}: amount={amount}, rate={rate}")
        else:
            print(f"Ошибка запроса для {date_str}: {response.status_code}")
        current += timedelta(days=1)
    conn.close()

if __name__ == "__main__":
    currencies = os.getenv("SYNC_CURRENCIES").split(",")
    start_date = os.getenv("SYNC_START")
    end_date = os.getenv("SYNC_END")
    sync_period_data(start_date, end_date, currencies)