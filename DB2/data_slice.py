import mysql.connector
import time
import os
from datetime import datetime

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3307,  # <-- ВАЖНО!
    'database': 'mydatabase',
}


def fetch_data():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")  # <-- сюда свой SQL-запрос
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def save_to_file(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_slice_{timestamp}.txt"
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')

if __name__ == "__main__":
    while True:
        data = fetch_data()
        save_to_file(data)
        time.sleep(300)  # 5 минут