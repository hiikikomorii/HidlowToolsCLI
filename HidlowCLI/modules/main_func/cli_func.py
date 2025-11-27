import json, urllib.request
import sys
import random
import requests
import time
import re
from colorama import init, Fore, Style, Back
import phonenumbers
from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
import platform, socket, psutil
from tqdm import tqdm
from faker import Faker
import qrcode
import os
from pynput.keyboard import Controller, Key

desc_text = Fore.LIGHTCYAN_EX + "Initialization"

BLUE = "\x1b[34m"
CYAN = "\x1b[96m"
BLACK= "\x1b[30m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
MAGENTA = "\x1b[35m"
WHITE = "\x1b[37m"

RESET = "\x1b[0m"



user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A305FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"
}

def logo():
    ascii_art = """
                                                                ▀██▀  ▀██▀  ██      ▀██  ▀██                         █▀▀██▀▀█                 ▀██         
                                                                 ██    ██  ▄▄▄    ▄▄ ██   ██    ▄▄▄   ▄▄▄ ▄▄▄ ▄▄▄       ██      ▄▄▄     ▄▄▄    ██   ▄▄▄▄  
                                                                 ██▀▀▀▀██   ██  ▄▀  ▀██   ██  ▄█  ▀█▄  ██  ██  █        ██    ▄█  ▀█▄ ▄█  ▀█▄  ██  ██▄ ▀  
                                                                 ██    ██   ██  █▄   ██   ██  ██   ██   ███ ███         ██    ██   ██ ██   ██  ██  ▄ ▀█▄▄ 
                                                                ▄██▄  ▄██▄ ▄██▄ ▀█▄▄▀██▄ ▄██▄  ▀█▄▄█▀    █   █         ▄██▄    ▀█▄▄█▀  ▀█▄▄█▀ ▄██▄ █▀▄▄█▀
    """
    def print_cyan_to_darkblue(asciii_art):
        lines = asciii_art.split("\n")
        total_lines = len(lines)

        for i, line in enumerate(lines):
            g = int(255 - (i / max(total_lines - 1, 1)) * 255)
            b = int(255 - (i / max(total_lines - 1, 1)) * (255 - 139))
            print(f"\033[38;2;0;{g};{b}m{line}\033[0m")

    print_cyan_to_darkblue(ascii_art)


def logo_main_text():
    print(f"""
                                                                                         {Fore.CYAN}1{Fore.RESET} - {Fore.LIGHTCYAN_EX}Number    {Fore.CYAN}2{Fore.RESET} - {Fore.LIGHTCYAN_EX}Lat/Lon    {Fore.CYAN}3{Fore.RESET} - {Fore.LIGHTCYAN_EX}IP{Fore.RESET}
                                                                                         {Fore.CYAN}4{Fore.RESET} - {Fore.LIGHTCYAN_EX}QRcode    {Fore.CYAN}5{Fore.RESET} - {Fore.LIGHTCYAN_EX}FlaskAPI   {Fore.CYAN}6{Fore.RESET} - {Fore.LIGHTCYAN_EX}Troll{Fore.RESET}
                                                                                         {Fore.CYAN}7{Fore.RESET} - {Fore.LIGHTCYAN_EX}Faker     {Fore.CYAN}8{Fore.RESET} - {Fore.LIGHTCYAN_EX}Currency   {Fore.CYAN}9{Fore.RESET} - {Fore.LIGHTCYAN_EX}GPT CHC{Fore.RESET}
        
                                                                                                       {Fore.RED}10{Fore.RESET} - {Fore.LIGHTRED_EX}Exit{Fore.RESET}

    """)

def faker_logo_text():
    print(f"""
                                                                                                    {Fore.CYAN}1{Fore.RESET} - {Fore.LIGHTCYAN_EX}Russian    {Fore.CYAN}2{Fore.RESET} - {Fore.LIGHTCYAN_EX}English
                                                                                                    {Fore.CYAN}3{Fore.RESET} - {Fore.LIGHTCYAN_EX}Spanish    {Fore.CYAN}4{Fore.RESET} - {Fore.LIGHTCYAN_EX}Japanese

                                                                                                             {Fore.RED}5{Fore.RESET} - {Fore.LIGHTRED_EX}Exit{Fore.RESET}

               """)

def currency_logo_text():
    print(f"""
                                                                                                       {Fore.CYAN}1{Fore.RESET} - {Fore.LIGHTCYAN_EX}TON   {Fore.CYAN}2{Fore.RESET} - {Fore.LIGHTCYAN_EX}BTC

                                                                                                           {Fore.RED}3{Fore.RESET} - {Fore.LIGHTRED_EX}Exit{Fore.RESET}

            """)

#cls
def clear_cmd_func():
    os.system("cls")


def sysinfo_func():
    def typewriter_info(text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    node_info = platform.node()
    os_info = platform.platform()
    mach_info = platform.machine()

    typewriter_info(f"{Fore.BLUE}Node: {node_info}", 0.02)
    typewriter_info(f"{Fore.BLUE}OS: {os_info}", 0.02)
    typewriter_info(f"{Fore.BLUE}Machine: {mach_info}", 0.02)
    time.sleep(0.5)
    clear_cmd_func()


#Faker
def faker_ru():
    init(autoreset=False)
    clear_cmd_func()
    fake = Faker('Ru_ru')
    first_name_ru = fake.first_name()
    last_name_ru = fake.last_name()
    address_ru = fake.address()
    number_ru = fake.phone_number()
    email_ru = fake.email()
    ssn_ru = fake.ssn()
    passwd_ru = fake.password()
    ipv4f = fake.ipv4()

    def typewriter_fakerru(text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()


    typewriter_fakerru(f"{BLUE}Имя: {CYAN}{first_name_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Фамилия: {CYAN}{last_name_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Адрес: {CYAN}{address_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Мобильный номер: {CYAN}{number_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Почта: {CYAN}{email_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Номер соц страховки: {CYAN}{ssn_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Пароль: {CYAN}{passwd_ru}", delay=0.01)
    typewriter_fakerru(f"{BLUE}Айпи: {CYAN}{ipv4f}", delay=0.01)


    input(Fore.BLUE + "Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    faker_logo_text()


def faker_eng():
    clear_cmd_func()
    fake = Faker()
    first_name_eng = fake.first_name()
    last_name_eng = fake.last_name()
    address_eng = fake.address()
    number_eng = fake.phone_number()
    email_eng = fake.email()
    ssn_eng = fake.ssn()
    passwd_eng = fake.password()
    ipv4f = fake.ipv4()

    def typewriter_fakereng(text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    typewriter_fakereng(f"{BLUE}First name: {CYAN}{first_name_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Last name: {CYAN}{last_name_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Address: {CYAN}{address_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Address: {CYAN}{address_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Phone number: {CYAN}{number_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}email: {CYAN}{email_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Ssn: {CYAN}{ssn_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}Password: {CYAN}{passwd_eng}", delay=0.01)
    typewriter_fakereng(f"{BLUE}IP: {CYAN}{ipv4f}", delay=0.01)

    input(Fore.BLUE + "Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    faker_logo_text()



def faker_es():
    clear_cmd_func()
    fake = Faker('es_ES')
    first_name_es = fake.first_name()
    last_name_es = fake.last_name()
    address_es = fake.address()
    number_es = fake.phone_number()
    email_es = fake.email()
    ssn_es = fake.ssn()
    passwd_es = fake.password()
    ipv4f = fake.ipv4()

    def typewriter_fakeres(text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    typewriter_fakeres(f"{BLUE}First name: {CYAN}{first_name_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Last name: {CYAN}{last_name_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Address: {CYAN}{address_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Address: {CYAN}{address_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Phone number: {CYAN}{number_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}email: {CYAN}{email_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Ssn: {CYAN}{ssn_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}Password: {CYAN}{passwd_es}", delay=0.01)
    typewriter_fakeres(f"{BLUE}IP: {CYAN}{ipv4f}", delay=0.01)

    input(Fore.BLUE + "Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    faker_logo_text()

def faker_jp():
    clear_cmd_func()
    fake = Faker('ja_JP')
    first_name_jp = fake.first_name()
    last_name_jp = fake.last_name()
    address_jp = fake.address()
    number_jp = fake.phone_number()
    email_jp = fake.email()
    ssn_jp = fake.ssn()
    passwd_jp = fake.password()
    ipv4f = fake.ipv4()

    def typewriter_fakerjp(text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    typewriter_fakerjp(f"{BLUE}First name: {CYAN}{first_name_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Last name: {CYAN}{last_name_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Address: {CYAN}{address_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Address: {CYAN}{address_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Phone number: {CYAN}{number_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}email: {CYAN}{email_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Ssn: {CYAN}{ssn_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}Password: {CYAN}{passwd_jp}", delay=0.01)
    typewriter_fakerjp(f"{BLUE}IP: {CYAN}{ipv4f}", delay=0.01)

    input(Fore.BLUE + "Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    faker_logo_text()

#api ip
def ip_api():
    ip = input(f"{Fore.BLUE}IP:{Fore.RESET} ").strip()

    url = f"https://ipwhois.app/json/{ip}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    type = data.get("type", "не найдено")
    continent = data.get("continent", "не найдено")
    continent_code = data.get("continent_code", "не найдено")
    countryy = data.get("country", "не найдено")
    country_code = data.get("country_code", "не найдено")
    country_flag = data.get("country_flag", "не найдено")
    country_capital = data.get("country_capital", "не найдено")
    country_phone = data.get("country_phone", "не найдено")
    country_neighbours = data.get("country_neighbours", "не найдено")
    regionn = data.get("region", "не найдено")
    cityy = data.get("city", "не найдено")
    latitudee = data.get("latitude", "не найдено")
    longitudee = data.get("longitude", "не найдено")
    asn = data.get("asn", "не найдено")
    orgg = data.get("org", "не найдено")
    isp = data.get("isp", "не найдено")
    timezone = data.get("timezone", "не найдено")
    timezone_name = data.get("timezone_name", "не найдено")
    currency = data.get("currency", "не найдено")
    currency_code = data.get("currency_code", "не найдено")
    currency_symbol = data.get("currency_symbol", "не найдено")

    for _ in tqdm(range(10), desc=desc_text, ncols=100):
        time.sleep(0.1)
    time.sleep(0.1)
    clear_cmd_func()

    print(f"{Fore.BLUE}Запрос {Fore.LIGHTGREEN_EX}{ip}")
    print(f"{Fore.BLUE}Тип: {Fore.LIGHTCYAN_EX}{type}")
    print(f"{Fore.BLUE}Долгота:{Fore.LIGHTCYAN_EX}{latitudee}")
    print(f"{Fore.BLUE}Широта: {Fore.LIGHTCYAN_EX}{longitudee}")

    print(f"{Fore.BLUE}Континент: {Fore.LIGHTCYAN_EX}{continent}")
    print(f"{Fore.BLUE}Страна: {Fore.LIGHTCYAN_EX}{countryy}")
    print(f"{Fore.BLUE}Столица: {Fore.LIGHTCYAN_EX}{country_capital}")
    print(f"{Fore.BLUE}Регион: {Fore.LIGHTCYAN_EX}{regionn}")
    print(f"{Fore.BLUE}Город: {Fore.LIGHTCYAN_EX}{cityy}")

    print(f"{Fore.BLUE}Код континента: {Fore.LIGHTCYAN_EX}{continent_code}")
    print(f"{Fore.BLUE}Код страны: {Fore.LIGHTCYAN_EX}{country_code}")
    print(f"{Fore.BLUE}Код телефона: {Fore.LIGHTCYAN_EX}{country_phone}")
    print(f"{Fore.BLUE}Флаг страны: {Fore.LIGHTCYAN_EX}{country_flag}")
    print(f"{Fore.BLUE}Соседние страны: {Fore.LIGHTCYAN_EX}{country_neighbours}")
    print(f"{Fore.BLUE}Аsn: {Fore.LIGHTCYAN_EX}{asn}")
    print(f"{Fore.BLUE}Провайдер: {Fore.LIGHTCYAN_EX}{isp}")
    print(f"{Fore.BLUE}Организация: {Fore.LIGHTCYAN_EX}{orgg}")
    print(f"{Fore.BLUE}Часовой пояс: {Fore.LIGHTCYAN_EX}{timezone}")
    print(f"{Fore.BLUE}Название: {Fore.LIGHTCYAN_EX}{timezone_name}")
    print(f"{Fore.BLUE}Валюта: {Fore.LIGHTCYAN_EX}{currency}")
    print(f"{Fore.BLUE}Код валюты: {Fore.LIGHTCYAN_EX}{currency_code}")
    print(f"{Fore.BLUE}Символ валюты: {Fore.LIGHTCYAN_EX}{currency_symbol}")

    print(Style.RESET_ALL)
    input(Fore.BLUE + "Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    logo_main_text()


#api latlon
def coordinates_api():
    clear_cmd_func()
    logo()
    lat = input(f"{Fore.BLUE}Широта/lat:{Fore.RESET} ").strip()
    lon = input(f"{Fore.BLUE}Долготa/lon:{Fore.RESET} ").strip()

    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    latt = data.get("lat", "не найдено")
    lonn = data.get("lon", "не найдено")

    address = data.get("address", {})
    tourism = address.get("tourism", "не найдено")
    house_number = address.get("house_number", "не найдено")
    road = address.get("road", "не найдено")
    quarter = address.get("quarter", "не найдено")
    neighbourhood = address.get("neighbourhood", "не найдено")
    suburb = address.get("suburb", "не найдено")
    city = address.get("city", "не найдено")
    state = address.get("state", "не найдено")
    region = address.get("region", "не найдено")
    postcode = address.get("postcode", "не найдено")
    country = address.get("country", "не найдено")
    country_code = address.get("country_code", "не найдено")
    name = data.get("name", "не найдено")

    osm_type = data.get("osm_type", "не найдено")
    classs = data.get("class", "не найдено")
    type = data.get("type", "не найдено")
    place_rank = data.get("place_rank", "не найдено")
    place_id = data.get("place_id", "не найдено")

    for _ in tqdm(range(15), desc=desc_text, ncols=100):
        time.sleep(0.2)
    clear_cmd_func()
    print(
    f"{Fore.LIGHTCYAN_EX}широта: {Fore.LIGHTGREEN_EX}{latt}{Fore.RESET} | {Fore.LIGHTCYAN_EX}долгота: {Fore.LIGHTGREEN_EX}{lonn}")
    print(f"{Fore.LIGHTCYAN_EX}Страна: {Fore.CYAN}{country}")
    print(f"{Fore.LIGHTCYAN_EX}Регион: {Fore.CYAN}{region}")
    print(f"{Fore.LIGHTCYAN_EX}Область: {Fore.CYAN}{state}")
    print(f"{Fore.LIGHTCYAN_EX}Город: {Fore.CYAN}{city}")
    print(f"{Fore.LIGHTCYAN_EX}Пригород: {Fore.CYAN}{suburb}")
    print(f"{Fore.LIGHTCYAN_EX}Квартал: {Fore.CYAN}{quarter}")
    print(f"{Fore.LIGHTCYAN_EX}Улица: {Fore.CYAN}{road}")
    print(f"{Fore.LIGHTCYAN_EX}Микрорайон: {Fore.CYAN}{neighbourhood}")
    print(f"{Fore.LIGHTCYAN_EX}Достопримечательность: {Fore.CYAN}{name}{Fore.RESET} | {Fore.CYAN}{tourism}")
    print(f"{Fore.LIGHTCYAN_EX}Номер дома: {Fore.CYAN}{house_number}")

    print(f"{Fore.LIGHTCYAN_EX}Код страны: {Fore.CYAN}{country_code}")
    print(f"{Fore.LIGHTCYAN_EX}Индентификатор места: {Fore.CYAN}{place_id}")
    print(f"{Fore.LIGHTCYAN_EX}Тип объекта: {Fore.CYAN}{osm_type}")
    print(f"{Fore.LIGHTCYAN_EX}Класс объекта: {Fore.CYAN}{classs}")
    print(f"{Fore.LIGHTCYAN_EX}Тип: {Fore.CYAN}{type}")
    print(f"{Fore.LIGHTCYAN_EX}Числовой ранг: {Fore.CYAN}{place_rank}")
    print(f"{Fore.LIGHTCYAN_EX}Почтовый индекс: {Fore.CYAN}{postcode}")
    print(Style.RESET_ALL)
    input("Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    logo_main_text()


#ton api
def ton_api():
    url = "https://api.coinpaprika.com/v1/tickers/toncoin-the-open-network?quotes=USD,RUB"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        tonusd = usd.get("price", "not found")
        tonrub = rub.get("price", "not found")

        print(f"{Fore.BLUE}Usd: {Fore.LIGHTCYAN_EX}{tonusd:.2f}{Fore.LIGHTGREEN_EX}${Style.RESET_ALL}")
        print(f"{Fore.BLUE}Rub: {Fore.LIGHTCYAN_EX}{tonrub:.1f}{Fore.LIGHTGREEN_EX}₽{Style.RESET_ALL}")
        input(Fore.BLUE + "Enter: ")
        clear_cmd_func()
        logo()
        currency_logo_text()

    except Exception as error_ton:
        print(Fore.RED + f"API временно не работает\n\n{error_ton}{Style.RESET_ALL}")

#btc api
def btc_api():
    url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD,RUB"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        btcusd = usd.get("price", "not found")
        btcrub = rub.get("price", "not found")

        print(f"{Fore.BLUE}Usd: {Fore.LIGHTCYAN_EX}{btcusd:,.1f}{Fore.LIGHTGREEN_EX}${Style.RESET_ALL}")
        print(f"{Fore.BLUE}Rub: {Fore.LIGHTCYAN_EX}{btcrub:,.0f}{Fore.LIGHTGREEN_EX}₽{Style.RESET_ALL}")

        input(Fore.BLUE + "Enter: ")
        clear_cmd_func()
        logo()
        currency_logo_text()


    except Exception as error_btc:
        print(Fore.RED + f"API временно не работает\n\n{error_btc}{Style.RESET_ALL}")


#qrcode
def qrcode_mk():
    data = input(f"{Fore.BLUE}url:{Fore.RESET} ")
    try:
        img = qrcode.make(data)
        img.save("qrcode.png")
        print(f"{Fore.LIGHTGREEN_EX}QR код сгенерирован и сохранён как 'qrcode.png'{Style.RESET_ALL}")
        input("Enter: ")
    except Exception as error_qr:
        print(f"{Fore.RED}Ошибка при создании qrcode.\n\n{error_qr}{Style.RESET_ALL}")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    logo_main_text()

# flask server
def flask_server_open():
    try:
        script_dir = Path(__file__).parent / "modules" / "apiserver"
        script_file = script_dir / "hidlowAPI.py"

        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_file)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as error_flask:
        print(f"{Fore.RED}HidlowAPI.py failed to start.\n\n{error_flask}")

#troll
def troll_open():
    try:
        script_dir = Path(__file__).parent / "modules" / "troll"
        script_file = script_dir / "trollhidlowCLI.py"

        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_file)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as error_troll:
        print(f"{Fore.RED}trollhidlowCLI.py failed to start.\n\n{error_troll}")

#gpt
def gpt_converter():

    enternamefile = input(f"{Fore.BLUE}chat name: {Style.RESET_ALL}")

    INPUT_FILE = "conversations.json"

    CHAT_TITLE = enternamefile

    OUTPUT_FILE = "chat_export.txt"

    def extract_chat(input_file, chat_title, output_file):
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        chat = None
        for conv in data:
            if conv.get("title") == chat_title:
                chat = conv
                break

        if not chat:
            print(f"{Fore.RED}Чат с названием '{chat_title}' не найден.")
            return

        messages = []
        mapping = chat.get("mapping", {})
        for msg in mapping.values():
            message = msg.get("message")
            if not message:
                continue
            author = message.get("author", {}).get("role", "unknown")
            content_parts = message.get("content", {}).get("parts", [])
            text_parts = []
            for part in content_parts:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict):

                    if "text" in part:
                        text_parts.append(part["text"])
                    else:
                        text_parts.append(str(part))
            text = "\n".join(text_parts).strip()
            if text:
                if author == "user":
                    messages.append(f"Вы: {text}")
                elif author == "assistant":
                    messages.append(f"ChatGPT: {text}")
                elif author == "system":
                    messages.append(f"[СИСТЕМА]: {text}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(messages))

        print(f"{Fore.LIGHTGREEN_EX}Чат '{chat_title}' сохранён в {output_file}")

    extract_chat(INPUT_FILE, CHAT_TITLE, OUTPUT_FILE)

    input("Enter: ")
    clear_cmd_func()
    time.sleep(0.1)
    logo()
    logo_main_text()


def check_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=7)
        return True
    except urllib.error.URLError:
        return False

#number2
def send_request(url, phone):
    try:
        response = requests.get(url, headers=headers, timeout=10)

        time.sleep(random.uniform(2, 5))

        if response.status_code == 200:
            _ = phone
            time.sleep(0.1)

            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None

#number
def scanphone(phone):

    url = f"https://htmlweb.ru/geo/api.php?json&telcod={phone}"
    data = send_request(url, phone)

    if not isinstance(data, dict):
        return "[!] Произошла ошибка: данные ответа не являются словарем."

    country = data.get('country', {})
    region = data.get('region', {})
    capital = data.get('capital', {})

    if not isinstance(country, dict):
        country = {}
    if not isinstance(region, dict):
        region = {}
    if not isinstance(capital, dict):
        capital = {}

    if data.get("status_error"):
        return f"Ошибка: {data.get('error_message', 'Не удалось получить данные обратитесь к владельцу.')}"

    if data.get("limit") <= 0:
        return f"Ошибка: {data.get('error_message', f'У ВАС ИСЧЕРПАН ЛИМИТ {data.get("limit")}')}"

    region_data = data.get('region', {})

    country_name = country.get('name', 'Не найдено')
    country_fullname = country.get('fullname', 'Не найдено')
    city_name = capital.get('name', 'Не найдено')
    postal_code = capital.get('post', 'Не найдено')
    currency_code = country.get('iso', 'Не найдено')
    phone_codes = capital.get('telcod', 'Не найдено')
    wiki_url = capital.get('wiki', 'Не найдено')
    car_plate_code = region.get('autocod', 'Не найдено')
    country_id = country.get('id', 'Не найднено')
    operator_brand = capital.get('oper_brand', 'Не найдено')
    operator_default = capital.get('def', 'Не найдено')
    location = country.get('location', 'Не найдено')
    language = country.get('lang', 'Не найдено').title()
    language_code = capital.get('langcod', 'Не найдено')
    capitall = capital.get('name', 'Не найдено')
    latitude = capital.get('latitude', 'Не найдено')
    longitude = capital.get('longitude', 'Не найдено')

    parsed_phone = phonenumbers.parse(phone, country_id)

    carrier_info = phonenumbers.carrier.name_for_number(parsed_phone, "en")
    country_prefixx = phonenumbers.region_code_for_number(parsed_phone)
    countryy = phonenumbers.geocoder.description_for_number(parsed_phone, "en")
    regionn = phonenumbers.geocoder.description_for_number(parsed_phone, "ru")
    formatted_numberr = phonenumbers.format_number(parsed_phone,
                                                   phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    is_validd = "Valid" if phonenumbers.is_valid_number(parsed_phone) else "Invalid"
    is_possiblee = phonenumbers.is_possible_number(parsed_phone)
    timezonaa = phonenumbers.timezone.time_zones_for_number(parsed_phone)
    national_numberr = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL)
    country_codee = phonenumbers.region_code_for_number(parsed_phone)

    for _ in tqdm(range(10), desc=desc_text, ncols=100):
        time.sleep(0.1)
    time.sleep(0.5)
    clear_cmd_func()
    return f"""
{Fore.RESET}API #1
{Fore.BLUE}[+] ├Номер телефона -> {Fore.LIGHTCYAN_EX}{phone}
{Fore.BLUE}[+] ├Страна: {Fore.LIGHTCYAN_EX}{country_name}, {country_fullname}
{Fore.BLUE}[+] ├Город: {Fore.LIGHTCYAN_EX}{city_name}
{Fore.BLUE}[+] ├Почтовый индекс: {Fore.LIGHTCYAN_EX}{postal_code}
{Fore.BLUE}[+] ├Код валюты: {Fore.LIGHTCYAN_EX}{currency_code}
{Fore.BLUE}[+] ├Телефонные коды: {Fore.LIGHTCYAN_EX}{phone_codes}
{Fore.BLUE}[+] ├Посмотреть в wiki: {Fore.LIGHTCYAN_EX}{wiki_url}
{Fore.BLUE}[+] ├Гос. номер региона авто: {Fore.LIGHTCYAN_EX}{car_plate_code}
{Fore.BLUE}[+] ├Оператор: {Fore.LIGHTCYAN_EX}{carrier_info}, {operator_brand}, {operator_default}
{Fore.BLUE}[+] ├Местоположение: {Fore.LIGHTCYAN_EX}{country_name}, {capital.get('name', 'Не найдено')}, {city_name} ({region_data.get('okrug', 'Не найдено')})
{Fore.BLUE}[+] ├Открыть на карте (Google): {Fore.LIGHTCYAN_EX}https://www.google.com/maps/place/{latitude}+{longitude}
{Fore.BLUE}[+] ├Локация: {Fore.LIGHTCYAN_EX}{location}
{Fore.BLUE}[+] ├Язык общения: {Fore.LIGHTCYAN_EX}{language}, {language_code}
{Fore.BLUE}[+] ├Край/Округ/Область: {Fore.LIGHTCYAN_EX}{region.get('name', 'Не найдено')}, {region.get('okrug', 'Не найдено')}
{Fore.BLUE}[+] ├Столица: {Fore.LIGHTCYAN_EX}{capitall}
{Fore.BLUE}[+] ├Широта/Долгота: {Fore.LIGHTCYAN_EX}{latitude}, {longitude}
{Fore.BLUE}[+] └Оценка номера в сети: {Fore.LIGHTCYAN_EX}https://phoneradar.ru/phone/{phone}

{Fore.RESET}API #2
{Fore.BLUE}[*] ├Номер телефона - {Fore.LIGHTCYAN_EX}{phone}
{Fore.BLUE}[*] ├Страна -> {Fore.LIGHTCYAN_EX}{countryy}
{Fore.BLUE}[*] ├Регион -> {Fore.LIGHTCYAN_EX}{regionn}
{Fore.BLUE}[*] ├Формат -> {Fore.LIGHTCYAN_EX}{formatted_numberr}
{Fore.BLUE}[*] ├Оператор -> {Fore.LIGHTCYAN_EX}{carrier_info}
{Fore.BLUE}[*] ├Активен -> {Fore.LIGHTCYAN_EX}{is_possiblee}
{Fore.BLUE}[*] ├Валид -> {Fore.LIGHTCYAN_EX}{is_validd}
{Fore.BLUE}[*] ├Префикс страны -> {Fore.LIGHTCYAN_EX}+{country_prefixx}
{Fore.BLUE}[*] ├Таймзона -> {Fore.LIGHTCYAN_EX}{timezonaa}
{Fore.BLUE}[*] ├Национальный формат -> {Fore.LIGHTCYAN_EX}{national_numberr}
{Fore.BLUE}[*] └Код страны -> {Fore.LIGHTCYAN_EX}{country_codee}{Fore.RESET}
"""



def main():
    while True:
        choiceuser = input("> ").lower().strip()

        if choiceuser == "fakerru":
            faker_ru()
        elif choiceuser == "fakereng":
            faker_eng()
        elif choiceuser == "fakeres":
            faker_es()
        elif choiceuser == "fakerjp":
            faker_jp()
        elif choiceuser == "ip":
            ip_api()
        elif choiceuser == "lat":
            coordinates_api()
        elif choiceuser == "btc":
            btc_api()
        elif choiceuser == "ton":
            ton_api()
        elif choiceuser == "qr":
            qrcode_mk()

        elif choiceuser == "phone":
            user_iput = input(f"number: ")
            phone = re.sub(r"\D", "", user_iput)

            if check_internet():
                print(f"ethernet enable\n")
                a = scanphone(phone)
                print(a)
                input("Нажмите Enter, чтобы продолжить...")
                os.system("cls")
            else:
                print(f"Отсутствует интернет-соединение!")
                input("Нажмите Enter, чтобы продолжить...")
                os.system("cls")


if __name__ == '__main__':
    main()