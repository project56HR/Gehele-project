from datetime import datetime, time
try:
    from databaseManager.databaseManager import DatabaseManager
except Exception:
    from databaseManager import DatabaseManager

from fastapi import FastAPI, HTTPException


# Create the FastAPI app
app = FastAPI()
db = DatabaseManager(user="admin", password="root", host="192.168.2.121")
db.startDB()
@app.get("/")
def read_root():
    return {"message": "Welcome to the the Database API!"}


@app.get("/get/voltage/day/{day}")
def get_voltage_by_hour(day: str):
    try:
        # Parse the input date (format: DD-MM-YYYY)
        day_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_of_day = datetime.combine(day_date.date(), time.min)
    end_of_day = datetime.combine(day_date.date(), time.max)

    # Use QueryBuilder with SUM and GROUP BY
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
    print(rows)
    # Convert results to format [{"00:00": 123, "01:00": 456, ...}]
    hourly_data = [{row["hour"]: row["total"] for row in rows}]
    return hourly_data