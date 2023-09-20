import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Путь к исходной папке, которую нужно мониторить
source_folder = ' '

# Путь к папке, в которую нужно копировать новые файлы
destination_folder = ' '

# Путь к файлу, в котором будет храниться дата первого запуска программы
first_run_file = 'first_run.txt'

# Создаем класс-обработчик событий
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.first_run_time = self.get_first_run_time()

    def get_first_run_time(self):
        if os.path.exists(first_run_file):
            with open(first_run_file, 'r') as file:
                return float(file.read())
        else:
            # Если файл с датой первого запуска не существует, создаем его и записываем текущее время
            current_time = time.time()
            with open(first_run_file, 'w') as file:
                file.write(str(current_time))
            return current_time

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            destination_file = os.path.join(destination_folder, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.txt'):
                file_creation_time = os.path.getctime(file_path)
                # Проверяем, был ли файл создан после первого запуска программы
                if file_creation_time > self.first_run_time and file_name.endswith('.txt'):
                    shutil.copy(file_path, destination_file)
                    print(f"Скопирован новый файл: {file_name}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(60)  # Проверяем каждую минуту
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
