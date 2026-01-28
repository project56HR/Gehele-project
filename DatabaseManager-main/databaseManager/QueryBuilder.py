class QueryBuilder:
    def __init__(self, connection, table):
        self.connection = connection
        self.cursor = connection.cursor(dictionary=True)
        self.table = table
        self.columns = "*"
        self.conditions = []
        self.params = []
        self.order_clause = ""
        self.limit_clause = ""

    def select(self, *columns):
        """Select specific columns."""
        if columns:
            self.columns = ", ".join(columns)
        return self

    def where(self, column, operator, value):
        """Add WHERE condition."""
        self.conditions.append(f"{column} {operator} %s")
        self.params.append(value)
        return self

    def whereNull(self, column):
        self.conditions.append(f"{column} IS NULL")
        return self

    def whereNotNull(self, column):
        self.conditions.append(f"{column} IS NOT NULL")
        return self

    def orderBy(self, column, direction="ASC"):
        self.order_clause = f"ORDER BY {column} {direction}"
        return self

    def limit(self, n):
        self.limit_clause = f"LIMIT {n}"
        return self

    def get(self):
        where_clause = " AND ".join(self.conditions) if self.conditions else "1"
        query = f"SELECT {self.columns} FROM {self.table} WHERE {where_clause} "

        if hasattr(self, "group_clause") and self.group_clause:
            query += f"{self.group_clause} "
        if self.order_clause:
            query += f"{self.order_clause} "
        if self.limit_clause:
            query += f"{self.limit_clause} "
        query += ";"

        self.cursor.execute(query, self.params)
        return self.cursor.fetchall()

    def first(self):
        """Return only the first record."""
        self.limit(1)
        rows = self.get()
        return rows[0] if rows else None

    def insert(self, **data):
        """Insert a new record."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders});"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def groupBy(self, *columns):
        """Add GROUP BY clause."""
        self.group_clause = f"GROUP BY {', '.join(columns)}"
        return self

    def update(self, **data):
        """Update records matching WHERE clause."""
        if not self.conditions:
            raise ValueError("Update requires at least one WHERE condition to prevent mass updates.")

        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        query = f"UPDATE {self.table} SET {set_clause} WHERE {' AND '.join(self.conditions)};"
        self.cursor.execute(query, values + self.params)
        self.connection.commit()
        return self.cursor.rowcount

    def delete(self):
        """Delete records matching WHERE clause."""
        if not self.conditions:
            raise ValueError("Delete requires at least one WHERE condition to prevent mass deletes.")
        query = f"DELETE FROM {self.table} WHERE {' AND '.join(self.conditions)};"
        self.cursor.execute(query, self.params)
        self.connection.commit()
        return self.cursor.rowcount

    def sum(self, column, alias=None):
        alias_part = f" AS {alias}" if alias else ""
        # If already selecting something, add to it
        if self.columns == "*" or not self.columns:
            self.columns = f"SUM({column}){alias_part}"
        else:
            self.columns += f", SUM({column}){alias_part}"
        return self


