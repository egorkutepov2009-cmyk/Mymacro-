import os
import sys
import time
import random
import threading
import keyboard
import mouse
import pyautogui

# === НАСТРОЙКИ ===
# Имя файла со скриншотом кнопки «Играть снова»
BUTTON_IMAGE = "play_again.png"

# Точность совпадения картинки (от 0.1 до 1.0).
# 0.8 = 80% совпадения (оптимально, если в игре есть легкие эффекты/подсветка)
CONFIDENCE_LEVEL = 0.8

# Список случайных действий
ACTIONS = [
    'w', 'a', 's', 'd',
    'space',
    '1', '2', '3', '4', '5',
    'mouse5'
]
# =================

running = False

def get_resource_path(filename):
    """Находит путь к картинке рядом с .py или .exe файлом."""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

def check_and_click_button():
    """Ищет кнопку на экране по скриншоту и кликает по её центру."""
    image_path = get_resource_path(BUTTON_IMAGE)
    if not os.path.exists(image_path):
        print(f"[Ошибка] Файл {BUTTON_IMAGE} не найден рядом с программой!")
        return False

    try:
        # Ищем кнопку на экране с использованием OpenCV (confidence)
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=CONFIDENCE_LEVEL,
            grayscale=True  # Ускоряет поиск и игнорирует мелкие сдвиги оттенков
        )
        if location is not None:
            x, y = int(location.x), int(location.y)
            mouse.move(x, y, absolute=True, duration=0.2)
            time.sleep(0.1)
            mouse.click(button='left')
            print(f"[Кнопка найдена] Клик по координатам ({x}, {y})")
            return True
    except pyautogui.ImageNotFoundException:
        # Кнопки сейчас нет на экране — просто идём дальше
        pass
    except Exception as e:
        print(f"[Ошибка поиска]: {e}")

    return False

def macro_loop():
    global running
    while True:
        if running:
            # 1. Сначала проверяем, не появилась ли кнопка «Играть снова»
            clicked = check_and_click_button()

            # 2. Если кнопки нет — выполняем случайное действие из списка
            if not clicked:
                action = random.choice(ACTIONS)
                if action == 'mouse5':
                    mouse.click(button='x2')
                else:
                    keyboard.press(action)
                    time.sleep(random.uniform(0.05, 0.12))
                    keyboard.release(action)

                print(f"Выполнено: {action}")

            # Пауза 3 секунды с проверкой остановки
            for _ in range(30):
                if not running:
                    break
                time.sleep(0.1)
        else:
            time.sleep(0.1)

def toggle_macro():
    global running
    running = not running
    status = "ЗАПУЩЕН" if running else "ОСТАНОВЛЕН"
    print(f"\n[Макрос {status}]")

threading.Thread(target=macro_loop, daemon=True).start()
keyboard.add_hotkey('F6', toggle_macro)

print("Программа готова.")
print(f"Убедись, что файл '{BUTTON_IMAGE}' лежит в одной папке с программой.")
print("F6 — Старт / Пауза")
print("F8 — Выход из программы")

keyboard.wait('F8')
