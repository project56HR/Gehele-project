from databaseManager.DatabaseManager import DatabaseManager
from datetime import datetime, timedelta
import random

# Use your DatabaseManager
with DatabaseManager(user="appuser", password="apppass", host="mysql", database="wind_generator_stats") as db:
    db.createTables()  # ensure tables exist

    start_date = datetime(datetime.now().year, 1, 1)  # Jan 1 of current year
    for i in range(365):
        entry_date = start_date + timedelta(days=i)
        valueVolt = random.randint(9, 11)  # random 9, 10, 11
        valueAMP = random.randint(1, 3)  # random 1, 3
        valueWatt = valueVolt * valueAMP
        db.table("voltage_data").insert(value=valueVolt, created_at=entry_date)
        db.table("amp_data").insert(value=valueAMP, created_at=entry_date)
        db.table("watt_data").insert(value=valueWatt, created_at=entry_date)


    print("Inserted 365 entries into voltage_data, one per day.")
