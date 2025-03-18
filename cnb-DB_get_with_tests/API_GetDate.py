from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import get_db_connection, get_aggregated_rates
from datetime import datetime

app = FastAPI()

class ReportRequest(BaseModel):
    start_date: str = Field(default="10.03.2025",description="Формат DD.MM.YYYY")
    end_date: str = Field(default="17.03.2025", description="Формат DD.MM.YYYY")
    currencies: list[str] = Field(default=["USD", "EUR"], description="Список валют")

@app.post("/report")
def get_report(request: ReportRequest):
    """Генерирует отчет с агрегированными данными о курсах валют."""
    start_date_obj = datetime.strptime(request.start_date, "%d.%m.%Y").date()
    end_date_obj = datetime.strptime(request.end_date, "%d.%m.%Y").date()
    
    connection = get_db_connection()
    results = get_aggregated_rates(connection, start_date_obj, end_date_obj, request.currencies)
    report = {}
    for currency, min_rate, max_rate, avg_rate in results:
        report[currency] = {
            "min": round(min_rate, 4),
            "max": round(max_rate, 4),
            "avg": round(avg_rate, 4)
        }
    connection.close()
    return report