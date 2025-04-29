pipeline {
    agent any  // Используем любой доступный агент для выполнения

    environment {
        VENV_PATH = '/workspace/.venv'  // Указываем путь к виртуальному окружению
    }

    triggers {
        cron('H 5 * * *') 
    }

    stages {
        stage('Setup venv & Install requirements') {
            steps {
                // Шаг для создания виртуального окружения и установки зависимостей
                sh '''
                    # Создаем виртуальное окружение
                    python3 -m venv $VENV_PATH
                    
                    # Активируем виртуальное окружение
                    . $VENV_PATH/bin/activate
                    
                    # Обновляем pip до последней версии
                    pip install --upgrade pip
                    
                    # Устанавливаем необходимые библиотеки
                    pip install psycopg2-binary pandas
                '''
            }
        }
        stage('Run ETL') {
            steps {
                // Шаг для активации виртуального окружения и запуска ETL скрипта
                sh '''
                    # Активируем виртуальное окружение
                    . $VENV_PATH/bin/activate
                    
                    # Запускаем ETL скрипт
                    python /workspace/etl.py
                '''
            }
        }
    }
}