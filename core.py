import sqlite3
from datetime import datetime, date


class Records:
    def __init__(self, rows):
        self.data = rows

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for row in self.data:
            yield Record(row)


class Record:
    def __init__(self, row):
        self.data = row


class EasyLite:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.tables = []

    def connect(self):
        return sqlite3.connect(self.db_name)

    def query(self, sql: str):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return Records(cursor.fetchall())

    def create_table(self, table_name, *, auto_increment=True, **kwargs):
        fields = {}
        for k, v in kwargs.items():
            fields[k] = py_type_to_sqlite_type(v)
        fields_iter = (f'{name} {field_type}' for name, field_type in fields.items())
        fields_sql = ', '.join(fields_iter)
        if not auto_increment:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name}({fields_sql})"
        else:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {fields_sql})"
        self.query(sql)

    def drop_table(self, table_name):
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.query(sql)

    def insert(self, table_name, **kwargs):
        fields_str = ', '.join(kwargs.keys())
        values = kwargs.copy()
        for k, value in values.items():
            if isinstance(value, datetime):
                values[k] = (value.strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(value, date):
                values[k] = (value.strftime("%Y-%m-%d"))
        values_str = ', '.join(repr(v) for v in values.values())
        sql = f'INSERT INTO {table_name}({fields_str}) VALUES ({values_str})'
        self.query(sql)


def py_type_to_sqlite_type(py_type):
    sqlite_type = None
    if py_type in (str, datetime, date):
        sqlite_type = 'TEXT'
    elif py_type is int:
        sqlite_type = 'INTEGER'
    elif py_type is float:
        sqlite_type = 'REAL'
    elif py_type is bytes:
        sqlite_type = 'BLOB'
    return sqlite_type
