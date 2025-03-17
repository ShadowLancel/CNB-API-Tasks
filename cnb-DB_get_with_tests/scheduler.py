from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
from dotenv import load_dotenv
from SyncPeriodData import sync_period_data

load_dotenv()

def scheduled_sync():
    # Получаем сегодняшнюю дату в формате "dd.mm.yyyy"
    today = datetime.today().strftime("%d.%m.%Y")
    allowed_currencies = os.getenv("SYNC_CURRENCIES", "AUD,USD,EUR").split(",")
    print(f"Синхронизация данных за {today}")
    sync_period_data(today, today, allowed_currencies)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    sync_time = os.getenv("SYNC_TIME")
    hour, minute = map(int, sync_time.split(":"))

    # Добавляем задачу: каждый день в указанное время
    scheduler.add_job(scheduled_sync, 'cron', hour=hour, minute=minute)
    print(f"Планировщик запущен. Синхронизация каждый день в {sync_time}")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Планировщик остановлен.")