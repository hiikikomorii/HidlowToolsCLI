import ctypes
import sys

try:
    import json, urllib.request
    import random
    import requests
    import time
    import re
    from colorama import Fore, Style
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
    import platform, socket, psutil
    from tqdm import tqdm
    from datetime import date,datetime
    from faker import Faker
    from pynput.keyboard import Controller, Key
    import qrcode
    import psutil
    import os
    from modules.main_func.cli_func import clear_cmd_func, check_internet, send_request, logo, logo_main_text, faker_logo_text, currency_logo_text, sysinfo_func
    from modules.main_func.cli_func import faker_jp, faker_es, faker_ru, faker_eng
    from modules.main_func.cli_func import ip_api, coordinates_api, qrcode_mk, scanphone, flask_server_open, troll_open, btc_api, ton_api, gpt_converter

    GREEN = "\x1b[32m"
    print(f"{GREEN}all modules have been installed")
    time.sleep(0.1)
    os.system("cls")

except ModuleNotFoundError as e:
    if e.name == "modules.main_func":
        ctypes.windll.user32.MessageBoxW(0, f"Сборка повреждена\nпуть {e.name} не найден\nПроверьте совместимость", "CLI FUNC", 0x10)
        sys.exit()

    ctypes.windll.user32.MessageBoxW(0, f"Модуль {e.name} не найден.\nУстановите нужный модуль\nи перезапустите сборку", "hidlowtoolsCLI-NoModule", 0x10)
    sys.exit()

keyboard = Controller()
keyboard.press(Key.f11)
keyboard.release(Key.f11)

sysinfo_func()
logo()
logo_main_text()
time.sleep(0.1)

def main_number():
    clear_cmd_func()
    logo()
    user_iput = input(f"{Fore.LIGHTBLUE_EX}Введите номер-телефона: ")
    phone = re.sub(r"\D", "", user_iput)

    if check_internet():
        print(f"\n{Fore.LIGHTGREEN_EX}Интернет-соединение установлено.\n")
        a = scanphone(phone)
        print(a)
        input(f"{Fore.BLUE}Enter: {Fore.RESET}")
        os.system("cls")
        time.sleep(0.1)
        logo()
        logo_main_text()
    else:
        print(f"{Fore.RED}Отсутствует интернет-соединение!{Fore.RESET}")
        input(f"{Fore.BLUE}Enter: {Fore.RESET}")
        os.system("cls")
        time.sleep(0.1)
        logo()
        logo_main_text()

def currency_choice():
    clear_cmd_func()
    logo()
    currency_logo_text()
    while True:
        userchoice = input(f"{Fore.BLUE}> {Fore.RESET}").strip()
        if userchoice == "1":
            ton_api()
        elif userchoice == "2":
            btc_api()
        elif userchoice == "3":
            clear_cmd_func()
            logo()
            logo_main_text()
            break
        else:
            print(f"{Fore.RED}[ERROR] {Fore.LIGHTRED_EX}номер функции не найден")

def faker_choice():
    clear_cmd_func()
    logo()
    faker_logo_text()
    while True:
        userchoicefaker = input(f"{Fore.BLUE}> {Fore.RESET}").strip()
        if userchoicefaker == "1":
            faker_ru()
        elif userchoicefaker == "2":
            faker_eng()
        elif userchoicefaker == "3":
            faker_es()
        elif userchoicefaker == "4":
            faker_jp()
        elif userchoicefaker == "5":
            clear_cmd_func()
            logo()
            logo_main_text()
            break
        else:
            print(f"{Fore.RED}[ERROR] {Fore.LIGHTRED_EX}номер функции не найден")


def exit_adapter():
    sys.exit()

def prepare_clear():
    clear_cmd_func()
    logo()
    logo_main_text()

def main_menu():
    commands = {
        "1": main_number,
        "2": coordinates_api,
        "3": ip_api,
        "4": qrcode_mk,
        "5": flask_server_open,
        "6": troll_open,
        "7": faker_choice,
        "8": currency_choice,
        "9": gpt_converter,
        "10": exit_adapter,
        "clear": prepare_clear
    }

    while True:
        cmd = input(f"{Fore.BLUE}> {Style.RESET_ALL}").strip()
        if not cmd:
            pass
        if cmd:
            try:
                commands[cmd]()
            except Exception:
                print(f"{Fore.RED}[ERROR] {Fore.LIGHTRED_EX}номер функции не найден")
        else:
            pass


if __name__ == '__main__':
    main_menu()