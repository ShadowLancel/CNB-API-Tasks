# Before work with project:
`pip install -r requirements.txt`
configure file .env for you're database connection
example for create table in you're DB for this project:
```
CREATE TABLE exchange_rates (
    date DATE,
    currency_code VARCHAR(3),
    amount INTEGER,
    rate DECIMAL,
    PRIMARY KEY (date, currency_code)
);
```

## Task 1: Scheduler
cofigure you're time for write data in table with scheduler in .env file in param `SYNC_TIME=HH:MM` and run file `scheduler.py`

## Task 2: Recording data in a period:
cofigure you're period for write data in table by change you're data period in .env file in params `SYNC_START=day.month.year` and `SYNC_END=day.month.year`. Then you can run file `SyncPeriodData.py` and get data in DB

# Task 3: POST endpoint
for env:
1. open env
```
cd path_to_project
Set-ExecutionPolicy Unrestricted -Scope Process #for Windows PowerShell
.\env\scripts\activate
uvicorn API_GetDate:app --reload
```
then Follow the link 127.0.0.1:8000/docs for endpoint test.
You can send a post request with the default parameters, but you must make sure that this period covers the data received from the database.

# Task 4: Pytest
for env:
```
cd path_to_project
Set-ExecutionPolicy Unrestricted -Scope Process #for Windows PowerShell
.\env\scripts\activate
cd ..
pytest Tests.py
```
