from wheel_of_fortune.game import start_game
import os
import sys

def get_base_path():

    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def main():
    base_path = get_base_path()
    data_path = os.path.join(base_path, 'data')

    if not os.path.exists(data_path):
        print(f"Папка {data_path} не найдена!")
        return

    for filename in os.listdir(data_path):
        file_path = os.path.join(data_path, filename)
        if os.path.isfile(file_path):
            print(f"\nСодержимое файла {filename}:")
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read())
if __name__ == '__main__':
    start_game()

