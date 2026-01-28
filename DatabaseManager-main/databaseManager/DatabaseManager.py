import mysql.connector
from mysql.connector import Error

from databaseManager.QueryBuilder import QueryBuilder
from databaseManager.TableBuilder import TableBuilder


class DatabaseManager:
    def __init__(self, user, password, host='127.0.0.1', database='wind_generator_stats'):
        self.cnx_user = user
        self.cnx_password = password
        self.cnx_host = host
        self.cnx_database = database
        self.cnx = None
        self.cursor = None

    def startDB(self):
        """Start the database connection."""
        try:
            self.cnx = mysql.connector.connect(
                user=self.cnx_user,
                password=self.cnx_password,
                host=self.cnx_host,
                database=self.cnx_database,
                autocommit= True  # <- ensures latest data is always visible

            )
            self.cursor = self.cnx.cursor(dictionary=True)
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.cnx = None
            self.cursor = None
            raise Exception("Error connecting to database.")

    def closeDB(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.cnx:
            self.cnx.close()
            self.cnx = None
            print("Database connection closed.")

    def createTables(self):
        """
        Create the three measurement tables if they don't exist:
        - voltage_data
        - watt_data
        - amp_data
        Returns True on success, False on error.
        """
        if not self.cnx or not self.cursor:
            raise RuntimeError("Database is not started. Call startDB() or use the context manager.")
        try:
            (
                self.schema().createIfNotExists("voltage_data")
                    .increments("id")
                    .float("value")
                    .timestamps()
                    .execute()
            )

            (
                self.schema().createIfNotExists("amp_data")
                    .increments("id")
                    .float("value")
                    .timestamps()
                    .execute()
                )

            (
                self.schema().createIfNotExists("watt_data")
                    .increments("id")
                    .float("value")
                    .timestamps()
                    .execute()
            )
            print("Tables ensured: voltage_data, watt_data, amp_data.")
            return True
        except Error as e:
            print(f"Error creating tables: {e}")
            return False

    def table(self, name: str):
        """Return a Laravel-like query builder for the table."""
        if not self.cnx:
            raise RuntimeError("Database is not started. Call startDB() or use the context manager.")
        return QueryBuilder(self.cnx, name)

    def schema(self):
        """Return the schema/table builder."""
        if not self.cnx:
            raise RuntimeError("Database not connected. Use with-context or startDB().")
        return TableBuilder(self.cnx)

    def __enter__(self):
        self.startDB()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeDB()
