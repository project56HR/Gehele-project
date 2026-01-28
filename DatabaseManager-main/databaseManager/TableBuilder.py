class TableBuilder:
    """
    A simple chainable table builder for MySQL.
    Supports create, createIfNotExists, alter, drop, dropIfExists operations,
    and column definitions with nullable support.
    """

    def __init__(self, connection):
        """
        Initialize the TableBuilder with a MySQL connection.
        """
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = None
        self.columns = []
        self._last_column_index = None
        self.mode = None  # "create", "alter", "drop"
        self._executed = False
        self._if_exists_safe = False

    def _table_exists(self, table_name):
        """
        Check if the given table exists in the database.
        Returns True if exists, False otherwise.
        """
        self.cursor.execute("SHOW TABLES LIKE %s;", (table_name,))
        return self.cursor.fetchone() is not None

    def createIfNotExists(self, table_name):
        """
        Start creating a table only if it does not exist.
        No error will be thrown if the table already exists.
        """
        self.table_name = table_name
        self.mode = "create"
        self._if_exists_safe = True
        return self

    def create(self, table_name):
        """
        Start creating a new table.
        Raises ValueError if the table already exists.
        """
        if self._table_exists(table_name):
            raise ValueError(f"Table '{table_name}' already exists!")
        self.table_name = table_name
        self.mode = "create"
        self._if_exists_safe = False
        return self

    def table(self, table_name):
        """
        Modify an existing table.
        Raises ValueError if the table does not exist.
        """
        if not self._table_exists(table_name):
            raise ValueError(f"Table '{table_name}' does not exist!")
        self.table_name = table_name
        self.mode = "alter"
        return self

    def drop(self, table_name):
        """
        Drop a table.
        Raises ValueError if the table does not exist.
        """
        if not self._table_exists(table_name):
            raise ValueError(f"Table '{table_name}' does not exist!")
        self._query = f"DROP TABLE {table_name};"
        self.mode = "drop"
        return self

    def dropIfExists(self, table_name):
        """
        Drop a table if it exists.
        No error will be thrown if the table does not exist.
        """
        self._query = f"DROP TABLE IF EXISTS {table_name};"
        self.table_name = table_name
        self.mode = "drop"
        return self

    # --- COLUMN BUILDERS ---
    def increments(self, name):
        """
        Add an auto-increment primary key column.
        """
        self.columns.append(f"{name} INT AUTO_INCREMENT PRIMARY KEY")
        self._last_column_index = len(self.columns) - 1
        return self

    def string(self, name, length=255):
        """
        Add a VARCHAR column with NOT NULL.
        """
        self.columns.append(f"{name} VARCHAR({length}) NOT NULL")
        self._last_column_index = len(self.columns) - 1
        return self

    def integer(self, name):
        """
        Add an INT column with NOT NULL.
        """
        self.columns.append(f"{name} INT NOT NULL")
        self._last_column_index = len(self.columns) - 1
        return self

    def float(self, name):
        """
        Add a FLOAT column with NOT NULL.
        """
        self.columns.append(f"{name} FLOAT NOT NULL")
        self._last_column_index = len(self.columns) - 1
        return self

    def boolean(self, name):
        """
        Add a BOOLEAN column with NOT NULL and default 0.
        """
        self.columns.append(f"{name} BOOLEAN NOT NULL DEFAULT 0")
        self._last_column_index = len(self.columns) - 1
        return self

    def datetime(self, name):
        """
        Add a DATETIME column with NOT NULL.
        """
        self.columns.append(f"{name} DATETIME NOT NULL")
        self._last_column_index = len(self.columns) - 1
        return self

    def datetimeDefaultCurrent(self, name):
        """
        Add a DATETIME column with DEFAULT CURRENT_TIMESTAMP.
        """
        self.columns.append(f"{name} DATETIME DEFAULT CURRENT_TIMESTAMP")
        self._last_column_index = len(self.columns) - 1
        return self

    def nullable(self):
        """
        Mark the last added column as nullable.
        """
        if self._last_column_index is not None:
            self.columns[self._last_column_index] = self.columns[self._last_column_index].replace("NOT NULL", "NULL")
        return self

    def timestamps(self):
        """
        Add created_at and updated_at columns with CURRENT_TIMESTAMP defaults.
        """
        self.columns.append("created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        self._last_column_index = len(self.columns) - 1
        self.columns.append("updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        self._last_column_index = len(self.columns) - 1
        return self

    def execute(self):
        """
        Execute the built table query.
        Returns True on success, raises RuntimeError or ValueError on error.
        """
        if self._executed:
            raise RuntimeError("This schema builder has already executed a query.")
        if not self.table_name:
            raise RuntimeError("No table name defined.")

        table_exists = self._table_exists(self.table_name)

        if self.mode == "create":
            if table_exists and not self._if_exists_safe:
                raise ValueError(f"Table '{self.table_name}' already exists!")
            if not self.columns:
                raise RuntimeError("No columns defined for CREATE TABLE.")
            cols = ",\n    ".join(self.columns)
            if self._if_exists_safe:
                self._query = f"CREATE TABLE IF NOT EXISTS {self.table_name} (\n    {cols}\n);"
            else:
                self._query = f"CREATE TABLE {self.table_name} (\n    {cols}\n);"
        elif self.mode == "alter":
            if not self.columns:
                raise RuntimeError("No ALTER statement built.")
            self._query = f"ALTER TABLE {self.table_name} " + ", ".join(
                [f"ADD COLUMN {c}" for c in self.columns]
            ) + ";"
        elif self.mode == "drop":
            pass
        else:
            raise RuntimeError("No operation specified (create, alter, drop).")

        self.cursor.execute(self._query)
        self.connection.commit()
        self._executed = True
        return True

    def hasTable(self, table_name):
        """
        Check if a table exists.
        Returns True if exists, False otherwise.
        """
        return self._table_exists(table_name)
