import os
import time

# Путь к папке с файлами
directory = r'H:\Bigda\DB2'  # <-- поставил r перед строкой для Windows пути

def cleanup_old_files():
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 3600:
            os.remove(file_path)
            print(f"Удален файл: {file_path}")

if __name__ == "__main__":
    while True:
        cleanup_old_files()
        time.sleep(3600)  # 1 час