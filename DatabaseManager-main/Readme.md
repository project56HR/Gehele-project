# DatabaseManager

A simple MySQL database manager for wind generator statistics.  
Allows easy creation, insertion, retrieval, and deletion of generator data.

## Requirements

- Python 3.8+
- `mysql-connector-python` package

## Install: 
### ssh
```bash
pip install git+ssh://git@github.com/project56HR/DatabaseManager.git
```
### https
```bash
pip install git+https://github.com/project56HR/DatabaseManager.git
```
## Example code

```python
from databaseManager import DatabaseManager

with DatabaseManager("admin", "root", "server") as db:
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
          .limit(5)
          .get()
    )
    print(rows)

    (
        db.table("voltage_data")
        .where("value", ">=", 10)
        .orderBy("id", "ASC")
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


```
---

## Features

### DatabaseManager

```DatabaseManager(user, password, host)```  → create a new database connection.

```startDB()``` → open the database connection.

```closeDB()``` → close the database connection and cursor.

```table(name)``` → start a query on a specific table.

```schema()``` → start a schema builder to create, modify, or drop tables.

```insert(value=...)``` → insert a new row into the current table.

```where(column, operator, value)``` → filter rows by a condition.

```orderBy(column, direction)``` → sort the results.

```limit(n)``` → limit the number of results.

```get()``` → retrieve all matching rows.

```first()``` → retrieve the first matching row.

```delete()``` → delete rows that match the conditions.

```update(**data)``` → update rows that match the conditions.

### TableBuilder

```createIfNotExists(name)``` → create a table only if it does not exist.

```create(name)``` → create a new table; raises error if it already exists.

```drop(name)``` → drop a table; raises error if it does not exist.

```dropIfExists(name)``` → drop a table if it exists; no error if it does not exist.

```increments(name)``` → create an auto-increment primary key column.

```float(name)``` → create a FLOAT column (default NOT NULL).

```integer(name)``` → create an INT column (NOT NULL).

```string(name, length)``` → create a VARCHAR column (NOT NULL).

```boolean(name)``` → create a BOOLEAN column (NOT NULL, default 0).

```datetime(name)``` → create a DATETIME column (NOT NULL).

```datetimeDefaultCurrent(name)``` → create a DATETIME column with default CURRENT_TIMESTAMP.

```nullable()``` → make the last added column nullable.

```timestamps()``` → add created_at and updated_at columns with CURRENT_TIMESTAMP defaults.

```execute()``` → execute the schema query (create, alter, drop).

```hasTable(name)``` → check if a table exists (returns True or False).

### QueryBuilder

```table(name```) → start a query on a specific table.

```select(columns)``` → select specific columns; defaults to all columns ().

```where(column, operator, value)``` → add a WHERE condition.

```whereNull(column)``` → filter rows where the column is NULL.

```whereNotNull(column)``` → filter rows where the column is NOT NULL.

```orderBy(column, direction="ASC")``` → sort results; default is ascending.

```limit(n)``` → limit the number of rows returned.

```get()``` → retrieve all matching rows.

```first()``` → retrieve the first matching row.

```insert(**data)``` → insert a new row with specified column values.

```update(**data)``` → update rows matching the WHERE conditions; requires at least one where().

```delete()``` → delete rows matching the WHERE conditions; requires at least one where().

```sum(column, alias=None)```→ return the sum from the column with alias if supplied

### Important notes:

All functions are chainable. Example: ```db.table("voltage_data").where("value", ">", 10).orderBy("id").limit(5).get()```


```insert()``` and ```update()``` use key=value pairs for column values.

```whereNull()``` and ```whereNotNull()``` do not require a value.

```first()``` is a shortcut for ```limit(1).get()``` and returns a single row as a dictionary.

---

# Contributing
to check for linting error run ruff check . to see the error or add --fix to fix them
