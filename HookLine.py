import os
import sys
import time
import ctypes
import requests
import json

# ====================== Windows API ======================
def center_console_window():
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            time.sleep(0.4)
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if not hwnd:
                return

        os.system("mode con: cols=125 lines=38")
        time.sleep(0.3)

        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        SWP_NOSIZE = 0x0001
        SWP_NOZORDER = 0x0004
        HWND_TOP = 0

        window_width = 125 * 8
        window_height = 38 * 16

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 60

        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOP, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER
        )

    
        time.sleep(0.15)
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOP, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER
        )

    except Exception as e:
        print(f"Центрирование не сработало: {e}")
        pass


# ====================== Цвета в стиле Discord ======================
class Colors:
    RESET = '\033[0m'
    BLURPLE = '\033[38;5;63m'
    WHITE = '\033[97m'
    LIGHT_GRAY = '\033[38;5;251m'
    GRAY = '\033[38;5;245m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def type_animation(text, delay=0.035, color=Colors.RESET):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Colors.RESET)


def print_ascii_art():
    art = r"""
    __  __            __   __    _          
   / / / /___  ____  / /__/ /   (_)___  ___ 
  / /_/ / __ \/ __ \/ //_/ /   / / __ \/ _ \
 / __  / /_/ / /_/ / ,< / /___/ / / / /  __/
/_/ /_/\____/\____/_/|_/_____/_/_/ /_/\___/ 
    """
    print(Colors.BLURPLE + art + Colors.RESET)


def main_menu():
    while True:
        clear()
        print_ascii_art()
        
        print("\n")
        print(Colors.WHITE + "[1]" + Colors.LIGHT_GRAY + " Информация об утилите" + Colors.RESET)
        print(Colors.WHITE + "[2]" + Colors.LIGHT_GRAY + " Отправить сообщение через webhook" + Colors.RESET)
        print(Colors.WHITE + "[3]" + Colors.LIGHT_GRAY + " Выход из утилиты" + Colors.RESET)
        print()
        
        choice = input(Colors.BLURPLE + "Выберите пункт в меню: " + Colors.RESET).strip()

        if choice == "1":
            show_info()
        elif choice == "2":
            send_message()
        elif choice == "3":
            exit_utility()
        else:
            print(Colors.RED + "\nНеверный выбор!" + Colors.RESET)
            input(Colors.GRAY + "Нажмите Enter..." + Colors.RESET)


def show_info():
    clear()
    type_animation("Разработчик: @drugserenity", 0.04, Colors.BLURPLE)
    type_animation("Версия: 1.3", 0.04, Colors.BLURPLE)
    print ()
    type_animation("HookLine — утилита для отправки сообщений через Discord Webhook", 0.04, Colors.BLURPLE)
    print("\n")
    type_animation("Утилита предназначена для быстрой отправки сообщений через Webhook в канал Discord.", 0.03, Colors.WHITE)
    print("\n" + Colors.LIGHT_GRAY + "Возможности у режимов отправки сообщений:" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Отправить одно сообщение" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Отправить несколько сообщений" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Спам режим" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Поддержка webhook" + Colors.RESET)
    print()
    print("\n" + Colors.LIGHT_GRAY + "Визуалы:" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Простой и красивый интерфейс" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Анимации печати" + Colors.RESET)
    print(Colors.LIGHT_GRAY + "• Центрированное окно" + Colors.RESET)
    
    print(Colors.WHITE + "\nНажмите Enter для возврата в главное меню..." + Colors.RESET)
    input()


def send_message():
    clear()
    type_animation("Вставьте ссылку на Webhook", 0.04, Colors.BLURPLE)
    webhook_url = input(Colors.WHITE + "> " + Colors.RESET).strip()

    if not webhook_url.startswith(("https://discord.com/api/webhooks/", "https://discordapp.com/api/webhooks/")):
        type_animation("Ошибка: Это не похоже на Discord Webhook!", 0.04, Colors.RED)
        time.sleep(2)
        return

    while True:
        clear()
        print(Colors.BLURPLE + "Режимы отправки сообщений\n" + Colors.RESET)
        print(Colors.WHITE + "[1]" + Colors.LIGHT_GRAY + " Отправить одно сообщение" + Colors.RESET)
        print(Colors.WHITE + "[2]" + Colors.LIGHT_GRAY + " Отправить несколько сообщений" + Colors.RESET)
        print(Colors.WHITE + "[3]" + Colors.LIGHT_GRAY + " Спам-режим" + Colors.RESET)
        print(Colors.WHITE + "\nНажмите Enter чтобы вернуться в главное меню\n" + Colors.RESET)

        choice = input(Colors.BLURPLE + "Выберите режим: " + Colors.RESET).strip()

        if not choice:
            return  # Возврат в главное меню

        if choice == "1":
            send_single_message(webhook_url)
        elif choice == "2":
            send_multiple_messages(webhook_url)
        elif choice == "3":
            send_spam_mode(webhook_url)
        else:
            type_animation("Неверный выбор!", 0.04, Colors.RED)
            time.sleep(1)


# ==================== Вспомогательные функции ====================

def send_single_message(webhook_url):
    clear()
    type_animation("Напишите сообщение", 0.04, Colors.BLURPLE)
    message = input(Colors.WHITE + "> " + Colors.RESET).strip()

    if not message:
        return

    send_message_to_webhook(webhook_url, message)
    print(Colors.LIGHT_GRAY + "\nНажмите Enter для возврата..." + Colors.RESET)
    input()


def send_multiple_messages(webhook_url):
    while True:
        clear()
        type_animation("Напишите сообщение (пустая строка = выход)", 0.04, Colors.BLURPLE)
        message = input(Colors.WHITE + "> " + Colors.RESET).strip()

        if not message:
            type_animation("Выход из режима...", 0.04, Colors.LIGHT_GRAY)
            time.sleep(1)
            return

        send_message_to_webhook(webhook_url, message)
        print(Colors.LIGHT_GRAY + "\nНажмите Enter чтобы отправить ещё одно..." + Colors.RESET)
        input()


def send_spam_mode(webhook_url):
    clear()
    type_animation("СПАМ-РЕЖИМ", 0.06, Colors.RED)
    print(Colors.LIGHT_GRAY + "Напишите сообщение, которое будет спамиться.\n" + Colors.RESET)
    
    message = input(Colors.WHITE + "> " + Colors.RESET).strip()
    if not message:
        return

    clear()
    type_animation("Спам запущен! Нажмите Ctrl + C чтобы остановить.", 0.05, Colors.RED)
    print(Colors.LIGHT_GRAY + "Сообщение: " + message[:100] + ("..." if len(message) > 100 else "") + Colors.RESET + "\n")

    try:
        while True:
            send_message_to_webhook(webhook_url, message, show_success=False)
            time.sleep(0.35)
    except KeyboardInterrupt:
        clear()
        type_animation("Спам остановлен.", 0.05, Colors.GREEN)
        time.sleep(1.5)


def send_message_to_webhook(webhook_url, message, show_success=True):
    try:
        data = {"content": message}
        response = requests.post(
            webhook_url, 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if show_success and response.status_code in (200, 204):
            type_animation("Сообщение успешно отправлено!", 0.05, Colors.GREEN + Colors.BOLD)
        elif response.status_code not in (200, 204):
            type_animation(f"Ошибка! Код: {response.status_code}", 0.04, Colors.RED)
    except Exception as e:
        if show_success:
            type_animation("Ошибка отправки!", 0.04, Colors.RED)


def exit_utility():
    clear()
    type_animation("HookLine завершил свою работу.", 0.08, Colors.GREEN + Colors.BOLD)
    time.sleep(2)
    sys.exit(0)


if __name__ == "__main__":
    center_console_window()
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        print(Colors.GREEN + "\nДо свидания!" + Colors.RESET)
        time.sleep(0.8)