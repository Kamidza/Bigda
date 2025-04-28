import mysql.connector
import clickhouse_connect

# Конфигурация MySQL
mysql_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3307,  # У тебя порт 3307!
    'database': 'mydatabase',
}

# Подключение к ClickHouse (внимание: добавили username и password)
ch_client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='')

def fetch_data_from_mysql():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, message FROM messages")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def insert_into_clickhouse(data):
    if data:
        ch_client.insert('messages', data, column_names=['id', 'timestamp', 'message'])
        print(f"Inserted {len(data)} records into ClickHouse.")
    else:
        print("No data to insert.")

if __name__ == "__main__":
    data = fetch_data_from_mysql()
    insert_into_clickhouse(data)

