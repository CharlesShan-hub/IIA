import sqlite3

class Storage:
    def __init__(self, db_name='main'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._ensure_connection()

    def _ensure_connection(self):
        if not self.connection:
            self.connection = sqlite3.connect(f"{self.db_name}.db")
            self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        self._ensure_connection()
        columns_str = ', '.join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        self.connection.commit()

    def insert_data(self, table_name, data):
        self._ensure_connection()
        placeholders = ', '.join(['?' for _ in range(len(data))])
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.connection.commit()

    def select_data(self, table_name, condition=None):
        self._ensure_connection()
        if condition:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
        else:
            self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def update_data(self, table_name, new_data, condition):
        self._ensure_connection()
        set_clause = ', '.join([f"{key} = ?" for key in new_data.keys()])
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}", list(new_data.values()))
        self.connection.commit()

    def delete_data(self, table_name, condition):
        self._ensure_connection()
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.connection.commit()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

# Example usage
# storage = Storage()
# storage.create_table('users', ['id INTEGER PRIMARY KEY', 'name TEXT', 'age INTEGER'])
# storage.insert_data('users', (1, 'Alice', 30))
# storage.insert_data('users', (2, 'Bob', 25))
# print(storage.select_data('users'))
# storage.update_data('users', {'age': 26}, 'name = "Bob"')
# print(storage.select_data('users'))
# storage.delete_data('users', 'name = "Alice"')
# print(storage.select_data('users'))
# storage.close_connection()
