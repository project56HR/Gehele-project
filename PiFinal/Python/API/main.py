from datetime import datetime, time, timedelta
from fastapi import FastAPI, HTTPException, Depends
from databaseManager.DatabaseManager import DatabaseManager

app = FastAPI()

def get_db():
    db = DatabaseManager(
        user="appuser",
        password="apppass",
        host="mysql",
        database="wind_generator_stats"
    )
    db.startDB()
    db.createTables()
    try:
        yield db
    finally:
        db.closeDB()


def compute_average(rows):
    if not rows:
        return 0.0
    return round(sum(r["value"] for r in rows) / len(rows), 2)

def compute_kwh(rows):
    if len(rows) < 2:
        return 0.0
    first_ts = rows[0]["created_at"]
    last_ts = rows[-1]["created_at"]
    total_seconds = (last_ts - first_ts).total_seconds()
    avg_watt = compute_average(rows)
    kwh = (avg_watt * total_seconds / 3600) / 1000
    return round(kwh, 4)


@app.get("/get/voltage/day/{day}")
def get_voltage_by_hour(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        day_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    result = []
    for hour in range(24):
        start = datetime.combine(day_date.date(), time(hour, 0, 0))
        end = datetime.combine(day_date.date(), time(hour, 59, 59))
        rows = db.table("voltage_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({f"{hour:02d}:00": compute_average(rows)})
    return result


@app.get("/get/voltage/week/{day}")
def get_voltage_by_day_of_week(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=6)
    result = []
    for n in range(7):
        current_day = start_date + timedelta(days=n)
        start = datetime.combine(current_day.date(), time.min)
        end = datetime.combine(current_day.date(), time.max)
        rows = db.table("voltage_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({current_day.strftime("%d-%m-%Y"): compute_average(rows)})
    return result


@app.get("/get/voltage/year/{day}")
def get_voltage_by_month(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=365)
    result = []
    current = start_date.replace(day=1)
    while current <= end_date:
        start = datetime.combine(current.date(), time.min)
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1, day=1)
        else:
            next_month = current.replace(month=current.month + 1, day=1)
        end = datetime.combine((next_month - timedelta(seconds=1)).date(), time.max)
        rows = db.table("voltage_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({current.strftime("%m-%Y"): compute_average(rows)})
        current = next_month
    return result


# =========================
# AMP ENDPOINTS (average)
# =========================
@app.get("/get/amp/day/{day}")
def get_amp_by_hour(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        day_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    result = []
    for hour in range(24):
        start = datetime.combine(day_date.date(), time(hour, 0, 0))
        end = datetime.combine(day_date.date(), time(hour, 59, 59))
        rows = db.table("amp_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({f"{hour:02d}:00": compute_average(rows)})
    return result


@app.get("/get/amp/week/{day}")
def get_amp_by_day_of_week(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=6)
    result = []
    for n in range(7):
        current_day = start_date + timedelta(days=n)
        start = datetime.combine(current_day.date(), time.min)
        end = datetime.combine(current_day.date(), time.max)
        rows = db.table("amp_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({current_day.strftime("%d-%m-%Y"): compute_average(rows)})
    return result


@app.get("/get/amp/year/{day}")
def get_amp_by_month(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    start_date = end_date - timedelta(days=365)
    result = []
    current = start_date.replace(day=1)
    while current <= end_date:
        start = datetime.combine(current.date(), time.min)
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1, day=1)
        else:
            next_month = current.replace(month=current.month + 1, day=1)
        end = datetime.combine((next_month - timedelta(seconds=1)).date(), time.max)
        rows = db.table("amp_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        result.append({current.strftime("%m-%Y"): compute_average(rows)})
        current = next_month
    return result


@app.get("/get/watt/day/{day}")
def get_watt_kwh_by_hour(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        day_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")

    result = []
    for hour in range(24):
        start = datetime.combine(day_date.date(), time(hour, 0, 0))
        end = datetime.combine(day_date.date(), time(hour, 59, 59))
        rows = db.table("watt_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        kwh = compute_kwh(rows)
        result.append({f"{hour:02d}:00": kwh})
    return result

@app.get("/get/watt/week/{day}")
def get_watt_kwh_by_day(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")
    start_date = end_date - timedelta(days=6)
    result = []
    for n in range(7):
        current_day = start_date + timedelta(days=n)
        start = datetime.combine(current_day.date(), time.min)
        end = datetime.combine(current_day.date(), time.max)
        rows = db.table("watt_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        kwh = compute_kwh(rows)
        result.append({current_day.strftime("%d-%m-%Y"): kwh})
    return result

@app.get("/get/watt/year/{day}")
def get_watt_kwh_by_month(day: str, db: DatabaseManager = Depends(get_db)):
    try:
        end_date = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")
    start_date = end_date - timedelta(days=365)
    result = []
    current = start_date.replace(day=1)
    while current <= end_date:
        start = datetime.combine(current.date(), time.min)
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1, day=1)
        else:
            next_month = current.replace(month=current.month + 1, day=1)
        end = datetime.combine((next_month - timedelta(seconds=1)).date(), time.max)
        rows = db.table("watt_data")\
                 .where("created_at", ">=", start)\
                 .where("created_at", "<=", end)\
                 .orderBy("created_at", "ASC")\
                 .get()
        kwh = compute_kwh(rows)
        result.append({current.strftime("%m-%Y"): kwh})
        current = next_month
    return result
