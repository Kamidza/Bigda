import csv
import psycopg2
from datetime import datetime, timedelta 

# Настройки подключения к БД
conn = psycopg2.connect(
    dbname='forum_logs',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()


def get_data_for_date(date):
    # Считаем количество новых аккаунтов
    cursor.execute("""
        SELECT COUNT(*) FROM users WHERE registered_at = %s
    """, (date,))
    new_accounts = cursor.fetchone()[0]

    # Считаем количество сообщений и количество сообщений анонимов
    cursor.execute("""
        SELECT COUNT(*), COUNT(CASE WHEN user_id IS NULL THEN 1 END)
        FROM messages WHERE created_at::date = %s
    """, (date,))
    total_messages, anonymous_messages = cursor.fetchone()

    # Считаем количество тем, созданных за день
    cursor.execute("""
        SELECT COUNT(*) FROM topics WHERE created_at::date = %s
    """, (date,))
    new_topics = cursor.fetchone()[0]

    # Считаем количество тем на предыдущий день для процентного изменения
    prev_date = date - timedelta(days=1)
    cursor.execute("""
        SELECT COUNT(*) FROM topics WHERE created_at::date = %s
    """, (prev_date,))
    prev_topics = cursor.fetchone()[0] or 0  # Чтобы избежать деления на 0

    # Процентное изменение количества тем
    topic_growth_percentage = ((new_topics - prev_topics) / prev_topics) * 100 if prev_topics else 0

    return {
        'date': date,
        'new_accounts': new_accounts,
        'total_messages': total_messages,
        'anonymous_messages_percent': (anonymous_messages / total_messages * 100) if total_messages else 0,
        'topic_growth_percentage': topic_growth_percentage
    }

def aggregate_data(start_date, end_date):
    current_date = start_date
    aggregated_data = []

    while current_date <= end_date:
        data = get_data_for_date(current_date)
        aggregated_data.append(data)
        current_date += timedelta(days=1)

    return aggregated_data

def write_to_csv(aggregated_data, filename='aggregated_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'new_accounts', 'total_messages', 'anonymous_messages_percent', 'topic_growth_percentage'])
        writer.writeheader()
        for data in aggregated_data:
            writer.writerow(data)

if __name__ == "__main__":
    start_date = datetime(2025, 4, 1)
    end_date = datetime(2025, 4, 30)
    aggregated_data = aggregate_data(start_date, end_date)
    write_to_csv(aggregated_data)

    cursor.close()
    conn.close()
    print(f"Данные агрегации успешно записаны в файл 'aggregated_data.csv'.")