from .file_handler import random_word_generator, load_record, save_record
from .decorators import timer, log_errors
from .utils import mask_word, hearts
import logging
import linecache

logging.basicConfig(
    filename="game.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

@log_errors
@timer
def start_game():
    while True:  
        print("=== ПОЛЕ ЧУДЕС ===")
        logger.info("Игра запущена")
        record = load_record()
        print(f"🏆 Ваш лучший рекорд: {record} слов")

        levels = {'1': 7, '2': 5, '3': 3}
        while True:
            level = input(
                "Выберите уровень сложности:\n"
                "1. Легкий: 7 жизней\n"
                "2. Средний: 5 жизней\n"
                "3. Сложный: 3 жизни\n"
                "Ваш выбор: "
            ).strip()
            if level in levels:
                lives_start = levels[level]
                break
            print("Некорректный ввод, попробуйте еще раз.")

        words_gen = random_word_generator()
        guessed_count = 0

        try:
            # ИСПРАВЛЕНО: добавлены кавычки вокруг words.txt
            with open("data/words.txt", encoding="utf-8") as f:
                total_words = sum(1 for _ in f)
        except FileNotFoundError:
            print("Файл со словами не найден. Игра невозможна.")
            
            play_again = input("\nХотите попробовать снова? (да/нет): ").lower().strip()
            if play_again != "да":
                print("\n=== ИГРА ОКОНЧЕНА ===")
                print("Спасибо за игру! До новых встреч!")
                return
            else:
                print("\n" + "="*40)
                continue

        for word_index, word in enumerate(words_gen, start=1):
            guessed_letters = set()
            lives = lives_start

            print(f"\nСлово №{word_index} из {total_words}")
            print(mask_word(word, guessed_letters))
            print(f"Количество жизней: {hearts(lives)}")

            while lives > 0:
                guess = input("Назовите букву или слово целиком: ").lower().strip()

                if not guess.isalpha():
                    print("Ошибка: вводите только буквы.")
                    continue
                
                # Если введено слово целиком
                if len(guess) > 1:
                    if guess != word:
                        print("Ошибка: Назовите букву или слово целиком!")
                        continue
                    
                    if guess == word:
                        print("Вы угадали слово целиком!")
                        guessed_count += 1
                        logger.info(f"Слово {word} успешно угадано")
                        break
                    else:
                        print("💔 ИГРА ОКОНЧЕНА! 💔")
                        print("Вы неверно назвали слово")
                        print(f"Загаданное слово было: {word.upper()}")
                        end_game(guessed_count, total_words, record)
                        
                        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
                        if play_again != "да":
                            print("\n=== ИГРА ОКОНЧЕНА ===")
                            print("Спасибо за игру! До новых встреч!")
                            return
                        else:
                            break  


               
                if len(guess) == 1:
                    
                    if guess in guessed_letters:
                        print(f'Букву "{guess}" вы уже называли. Вы теряете жизнь!')
                        lives -= 1 
                        print(f"Количество жизней: {hearts(lives)}")
                        continue  
                    
                   
                    guessed_letters.add(guess)
                    
                    
                    if guess in word:
                        print(f'Буква "{guess}" есть в слове!')
                        masked = mask_word(word, guessed_letters)
                        print(masked)

                        
                        if masked == word:
                            print("Вы полностью открыли слово!")
                            guessed_count += 1
                            logger.info(f"Слово {word} успешно угадано")
                            break
                        else:
                            print(f"Количество жизней: {hearts(lives)}")
                    else:
                       
                        lives -= 1
                        print(f'Буквы "{guess}" нет в слове.')
                        print(f"Количество жизней: {hearts(lives)}")

            if lives == 0:
                print("💔 ИГРА ОКОНЧЕНА! 💔")
                print("У вас закончились жизни.")
                print(f"Загаданное слово было: {word.upper()}")
                break

            if word_index < total_words:
                again = input("Хотите сыграть еще? (да/нет): ").lower().strip()
                if again != "да":
                    break
            else:
                print("\n🎉 ПОЗДРАВЛЯЕМ! 🎉")
                print(f"Вы прошли всю игру и угадали все {total_words} слов(а)!")
                break

        
        print("\n" + "="*40)
        end_game(guessed_count, total_words, record)
        

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
        if play_again != "да":
            print("\n=== ИГРА ОКОНЧЕНА ===")
            print("Спасибо за игру! До новых встреч!")
            break


def end_game(guessed_count: int, total_words: int, record: int) -> None:
    logger.info(f"Игра завершена. Угадано слов: {guessed_count}.")
    print("\n📊 Ваша статистика:")
    print(f"Угадано слов: {guessed_count} из {total_words}")

    if guessed_count > record:
        print("🎊 НОВЫЙ РЕКОРД! 🎊")
        print(f"Предыдущий рекорд: {record} слов")
        print(f"Новый рекорд: {guessed_count} слов")
        save_record(guessed_count)
    else:
        print(f"Ваш лучший рекорд: {record} слов")

    linecache.clearcache()