import random
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

# Определение типов действий
ACTION_TYPES = [
    "first_visit",
    "register",
    "login",
    "logout",
    "create_topic",
    "view_topic",
    "delete_topic",
    "write_message"
]

# Генерация данных
def generate_logs(start_date, days=30):
    user_ids = []
    topic_ids = []
    now = start_date

    for day in range(days):
        date = now + timedelta(days=day)

        actions_today = []

        # 1. Первый заход
        for _ in range(random.randint(5, 10)):
            actions_today.append(("first_visit", None, "success", date))

        # 2. Регистрация
        for _ in range(random.randint(5, 10)):
            username = f"user_{random.randint(1000, 9999)}"
            cursor.execute("INSERT INTO users (username, registered_at) VALUES (%s, %s) RETURNING id", (username, date))
            user_id = cursor.fetchone()[0]
            user_ids.append(user_id)
            actions_today.append(("register", user_id, "success", date))

        # 3. Логин
        for _ in range(random.randint(5, 10)):
            user_id = random.choice(user_ids)
            actions_today.append(("login", user_id, "success", date))

        # 4. Логаут
        for _ in range(random.randint(5, 10)):
            user_id = random.choice(user_ids)
            actions_today.append(("logout", user_id, "success", date))

        # 5. Создание темы
        error_count = 0
        for _ in range(random.randint(5, 10)):
            if random.random() < 0.2 and error_count < 2:  # 20% шанса на ошибку и нужно сделать минимум 2 ошибки
                actions_today.append(("create_topic", None, "error_no_login", date))
                error_count += 1
            else:
                user_id = random.choice(user_ids)
                title = f"Topic {random.randint(1000, 9999)}"
                cursor.execute("INSERT INTO topics (title, created_by_user_id, created_at) VALUES (%s, %s, %s) RETURNING id", (title, user_id, date))
                topic_id = cursor.fetchone()[0]
                topic_ids.append(topic_id)
                actions_today.append(("create_topic", user_id, "success", date))

        # 6. Заход в тему
        for _ in range(random.randint(5, 10)):
            if topic_ids:
                topic_id = random.choice(topic_ids)
                user_id = random.choice(user_ids)
                actions_today.append(("view_topic", user_id, "success", date))

        # 7. Удаление темы
        for _ in range(random.randint(5, 10)):
            if topic_ids:
                topic_id = random.choice(topic_ids)
                user_id = random.choice(user_ids)
                cursor.execute("UPDATE topics SET deleted_at = %s WHERE id = %s", (date, topic_id))
                actions_today.append(("delete_topic", user_id, "success", date))

        # 8. Написание сообщения
        for _ in range(random.randint(5, 10)):
            if topic_ids:
                topic_id = random.choice(topic_ids)
                if random.random() < 0.5:  # 50% шанс на анонимное сообщение
                    user_id = None
                else:
                    user_id = random.choice(user_ids)
                content = f"Message {random.randint(1000, 9999)}"
                cursor.execute("INSERT INTO messages (topic_id, user_id, content, created_at) VALUES (%s, %s, %s, %s)", (topic_id, user_id, content, date))
                actions_today.append(("write_message", user_id, "success", date))

        # Запись логов в базу
        for action_type, user_id, server_response, created_at in actions_today:
            cursor.execute("""
                INSERT INTO logs (user_id, action_type, server_response, created_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, action_type, server_response, created_at))

        conn.commit()
    print("Генерация данных завершена.")
    if __name__ == "__main__":
        start_date = datetime(2025, 4, 1)
        generate_logs(start_date)
        cursor.close()
        conn.close()