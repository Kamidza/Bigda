-- Создание таблицы пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы тем форума
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_by_user_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);

-- Создание таблицы сообщений
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic_id INT NOT NULL,
    user_id INT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Создание таблицы логов действий
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INT NULL,
    action_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    server_response VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);