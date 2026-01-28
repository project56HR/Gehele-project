from databaseManager import DatabaseManager

with DatabaseManager("admin", "root", "192.168.2.121") as db:
    #dropping if exist tables
    db.schema().dropIfExists("voltage_data").execute()
    db.schema().dropIfExists("amp_data").execute()
    db.schema().dropIfExists("watt_data").execute()

    db.createTables()
    # insert dummyData
    db.table("voltage_data").insert(value=10)
    db.table("voltage_data").insert(value=11)
    db.table("voltage_data").insert(value=9)

#get dummy data
    rows = (
        db.table("voltage_data")
          .where("value", ">=", 10)
          .orderBy("id", "ASC")
          .sum("value", "total")
          .get()
    )
    print(rows)

    (
        db.table("voltage_data")
        .where("value", ">=", 10)
        .delete()
    )

    rows = (
        db.table("voltage_data")
        .where("value", ">=", 10)
        .orderBy("id", "ASC")
        .limit(5)
        .get()
    )
    print(rows)
