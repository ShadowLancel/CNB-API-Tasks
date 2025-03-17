from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import get_db_connection, get_aggregated_rates
from datetime import datetime

app = FastAPI()

class ReportRequest(BaseModel):
    start_date: str = Field(..., description="Формат DD.MM.YYYY", example="10.03.2025")
    end_date: str = Field(..., description="Формат DD.MM.YYYY", example="17.03.2025")
    currencies: list[str] = Field(..., description="Список валют", example=["USD", "EUR"])
    
    # переопределение схемы
    @classmethod
    def model_json_schema(cls, **kwargs):
        schema = super().model_json_schema(**kwargs)
        schema["properties"] = {
            "start_date": schema["properties"]["start_date"],
            "end_date": schema["properties"]["end_date"],
            "currencies": schema["properties"]["currencies"]
        }
        schema["examples"] = [
            {
                "start_date": "10.03.2025",
                "end_date": "17.03.2025",
                "currencies": ["USD", "EUR"]
            }
        ]
        return schema

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