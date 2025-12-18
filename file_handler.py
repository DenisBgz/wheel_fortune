import random
import os
import sys

def find_words_file():
    """Найти файл words.txt в разных местах"""
    
    # Список всех возможных мест
    search_paths = []
    
    # 1. Для exe файла (PyInstaller)
    if getattr(sys, 'frozen', False):
        # Временная папка PyInstaller
        if hasattr(sys, '_MEIPASS'):
            search_paths.append(os.path.join(sys._MEIPASS, 'wheel_of_fortune', 'data', 'words.txt'))
            search_paths.append(os.path.join(sys._MEIPASS, 'data', 'words.txt'))
            search_paths.append(os.path.join(sys._MEIPASS, 'words.txt'))
        
        # Рядом с exe
        exe_dir = os.path.dirname(sys.executable)
        search_paths.append(os.path.join(exe_dir, 'wheel_of_fortune', 'data', 'words.txt'))
        search_paths.append(os.path.join(exe_dir, 'data', 'words.txt'))
        search_paths.append(os.path.join(exe_dir, 'words.txt'))
    
    # 2. Для скрипта Python
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths.append(os.path.join(script_dir, 'data', 'words.txt'))
    
    # 3. Текущая рабочая директория
    search_paths.extend([
        'words.txt',
        'data/words.txt',
        './words.txt',
        './data/words.txt',
    ])
    
    # Ищем файл
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None

def random_word_generator():
    """Генератор слов из файла"""
    words_file = find_words_file()
    
    if not words_file:
        print("Файл words.txt не найден!")
        print("Пожалуйста, поместите words.txt в одну из этих папок:")
        print("1. Рядом с программой")
        print("2. В папке data рядом с программой")
        print("3. В папке wheel_of_fortune/data")
        
        # Используем запасные слова
        backup_words = ["яблоко", "банан", "компьютер", "телефон", "дом"]
        print(f"Используем запасные слова: {len(backup_words)} слов")
        random.shuffle(backup_words)
        for word in backup_words:
            yield word
        return
    
    print(f"Используется файл: {words_file}")
    
    try:
        with open(words_file, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return
    
    if not words:
        print("Файл words.txt пустой!")
        return
    
    print(f"Загружено слов: {len(words)}")
    
    # Перемешиваем и выдаём
    random.shuffle(words)
    for word in words:
        yield word

def load_record():
    """Загрузить рекорд"""
    # Простая реализация
    return 0

def save_record(record: int):
    """Сохранить рекорд"""
    print(f"Новый рекорд: {record} слов")