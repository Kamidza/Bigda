import random
import string
import time
import redis
import json

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    # Генерация случайного сообщения
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    message_data = {'message': message}
    
    # Отправка сообщения в Redis (сериализация в JSON)
    r.lpush('messages', json.dumps(message_data))
    
    print(f"Sent: {message}")
    time.sleep(60)  # Ждать 1 минуту
