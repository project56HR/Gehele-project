from datetime import datetime, time, timedelta

from databaseManager.DatabaseManager import DatabaseManager

from fastapi import FastAPI, HTTPException, Depends

import threading
lock = threading.Lock()

# Create the FastAPI app
app = FastAPI()

def get_db():
    db = DatabaseManager(user="root", password="root", host="mysql-windgen")
    db.startDB()
    db.createTables()
    try:
        yield db
    finally:
        db.closeDB()


@app.get("/")
def read_root():
    return {"message": "Welcome to the the Database API!"}


@app.get("/get/voltage/day/{day}")
def get_voltage_by_hour(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        # Parse the input date (format: DD-MM-YYYY)
        day_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_of_day = datetime.combine(day_date.date(), time.min)
    end_of_day = datetime.combine(day_date.date(), time.max)

    rows = (
        db.table("voltage_data")
        .select("DATE_FORMAT(created_at, '%H:00') AS hour")
        .where("created_at", ">=", start_of_day)
        .where("created_at", "<=", end_of_day)
        .groupBy("DATE_FORMAT(created_at, '%H:00')")
        .orderBy("DATE_FORMAT(created_at, '%H:00')", "ASC")
        .sum("value", "total")
        .get()
    )
    return [{row["hour"]: row["total"] for row in rows}]

@app.get("/get/voltage/week/{day}")
def get_voltage_by_day_of_week(day: str, db: DatabaseManager = Depends(get_db)):
    """
    Aggregates voltage totals per day for the 7-day period ending on the given day.
    """
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=6)
    start_of_week = datetime.combine(start_date.date(), time.min)
    end_of_week = datetime.combine(end_date.date(), time.max)

    rows = (
        db.table("voltage_data")
        .select("DATE_FORMAT(created_at, '%d-%m-%Y') AS day")
        .where("created_at", ">=", start_of_week)
        .where("created_at", "<=", end_of_week)
        .groupBy("DATE_FORMAT(created_at, '%d-%m-%Y')")
        .orderBy("DATE_FORMAT(created_at, '%d-%m-%Y')", "ASC")
        .sum("value", "total")
        .get()
    )
    return [{row["day"]: row["total"] for row in rows}]


@app.get("/get/voltage/year/{day}")
def get_voltage_by_month(day: str, db: DatabaseManager = Depends(get_db)):
    """
    Aggregates voltage totals per month for the 12-month period ending on the given day.
    """
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=365)
    start_of_year = datetime.combine(start_date.date(), time.min)
    end_of_year = datetime.combine(end_date.date(), time.max)

    rows = (
        db.table("voltage_data")
        .select("DATE_FORMAT(created_at, '%m-%Y') AS month")
        .where("created_at", ">=", start_of_year)
        .where("created_at", "<=", end_of_year)
        .groupBy("DATE_FORMAT(created_at, '%m-%Y')")
        .orderBy("DATE_FORMAT(created_at, '%m-%Y')", "ASC")
        .sum("value", "total")
        .get()
    )
    return [{row["month"]: row["total"] for row in rows}]