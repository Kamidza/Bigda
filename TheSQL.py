import sqlite3
from collections.abc import Collection, Iterable, Iterator


class TableData(Collection):
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def _execute_query(self, query: str, params: dict = None):
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            return cursor

    def __len__(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        cursor = self._execute_query(query)
        return cursor.fetchone()[0]

    def __getitem__(self, name: str) -> dict:
        query = f"SELECT * FROM {self.table_name} WHERE name = :name"
        cursor = self._execute_query(query, {"name": name})
        row = cursor.fetchone()
        if row is None:
            raise KeyError(f"Запись с именем '{name}' не найдена")
        return dict(row)

    def __contains__(self, name: str) -> bool:
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE name = :name)"
        cursor = self._execute_query(query, {"name": name})
        return cursor.fetchone()[0] == 1

    def __iter__(self) -> Iterator[dict]:
        query = f"SELECT * FROM {self.table_name} ORDER BY name"
        cursor = self._execute_query(query)
        return (dict(row) for row in cursor)

if __name__ == "__main__":
    presidents = TableData(database_name="/Users/blooomy/Desktop/example.sqlite", table_name="presidents")

    print(f"Количество записей: {len(presidents)}")

    print("\nПроверка наличия президента 'Yeltsin':")
    print('Yeltsin' in presidents)

    print("\nПолучение данных о 'Yeltsin':")
    print(presidents['Yeltsin'])

    print("\nВывод всех президентов:")
    for president in presidents:
        print(president["name"])