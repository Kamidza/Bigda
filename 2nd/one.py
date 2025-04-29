import psycopg2
import pandas as pd
from datetime import datetime, timedelta

# Определяем период: последние 30 дней
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# Устанавливаем соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    dbname="logsdb",
    user="user",
    password="password",
    host="host.docker.internal",
    port="5432"
)

# SQL-запрос для извлечения логов за указанный период
query = """
SELECT *
FROM logs
WHERE timestamp::date BETWEEN %s AND %s;
"""

# Выполняем запрос и загружаем данные в DataFrame
df = pd.read_sql(query, conn, params=[start_date.date(), end_date.date()])
conn.close()  # Закрываем соединение с базой данных

# Преобразуем столбец 'timestamp' в формат даты
df['date'] = pd.to_datetime(df['timestamp']).dt.date

# Подсчет новых регистраций по дням
registrations = df[df['action_type'] == 'registration'].groupby('date').size().rename("new_accounts")

# Подсчет сообщений по дням
messages = df[df['action_type'] == 'post_message']
total_messages = messages.groupby('date').size().rename("total_messages")

# Подсчет анонимных сообщений и их процент от общего числа сообщений
anon_messages = messages[messages['user_id'].isna()].groupby('date').size().rename("anon_messages")
anon_pct = (anon_messages / total_messages * 100).rename("anon_message_pct").fillna(0)

# Подсчет созданных тем по дням
topics_created = df[df['action_type'] == 'create_topic']
daily_topics = topics_created.groupby('date').size().rename("new_topics")

# Кумулятивное количество тем и процентное изменение по дням
cumulative_topics = daily_topics.cumsum()
topic_change_pct = cumulative_topics.pct_change().fillna(0) * 100
topic_change_pct = topic_change_pct.rename("topic_change_pct")

# Объединяем все результаты в один DataFrame и заполняем пропуски нулями
result = pd.concat([registrations, anon_pct, total_messages, topic_change_pct], axis=1).fillna(0)

# Округляем значения до двух знаков после запятой и сбрасываем индексы
result = result.round(2).reset_index().rename(columns={"date": "day"})

# Сохраняем результат в CSV файл
result.to_csv("/workspace/aggregated_logs.csv", index=False)
print("Файл aggregated_logs.csv создан.")