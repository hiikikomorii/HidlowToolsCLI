from flask import Flask, jsonify
import requests
import json, urllib.request
import sys
import random
import requests
import time
import re
from colorama import init, Fore, Style, Back
import phonenumbers
from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number

app = Flask(__name__)

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

@app.route('/home')
def home():
    return jsonify({
    "status": "ok"})

@app.route('/home/ip=<ip>')
def ip_api(ip):
    url = f"https://ipwhois.app/json/{ip}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "status": "ok",
            "ip": ip,
            "continent": data.get('continent', 'unknown'),
            "country": data.get('country', 'unknown'),
            "type": data.get('type', 'unknown'),
            "continent_code": data.get('continent_code', 'unknown'),
            "country_code": data.get('country_code', 'unknown'),
            "country_capital": data.get('country_capital', 'unknown'),
            "country_phone": data.get('country_phone', 'unknown'),
            "country_neighbours": data.get('country_neighbours', 'unknown'),
            "region": data.get('region', 'unknown'),
            "city": data.get('city', 'unknown'),
            "latitude": data.get('latitude', 'unknown'),
            "longitude": data.get('longitude', 'unknown'),
            "asn": data.get('asn', 'unknown'),
            "org": data.get('org', 'unknown'),
            "isp": data.get('isp', 'unknown'),
            "timezone": data.get('timezone', 'unknown'),
            "timezone_name": data.get('timezone_name', 'unknown'),
            "timezone_dstOffset": data.get('timezone_dstOffset', 'unknown'),
            "timezone_gmtOffset": data.get('timezone_gmtOffset', 'unknown'),
            "timezone_gmt": data.get('timezone_gmt', 'unknown'),
            "currency": data.get('currency', 'unknown'),
            "currency_code": data.get('currency_code', 'unknown'),
            "currency_symbol": data.get('currency_symbol', 'unknown'),
            "currency_rates": data.get('currency_rates', 'unknown'),
            "currency_plural": data.get('currency_plural', 'unknown')
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Не удалось получить данные"
        })

@app.route('/home/lat=<latt>&lon=<lonn>')
def latlon(latt, lonn):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latt}2&lon={lonn}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "lat": f'{latt}',
            "lon": f'{lonn}',
            "place_id": data.get('place_id', "unknown"),
            "osm_type": data.get('osm_type', "unknown"),
            "osm_id": data.get('osm_id', "unknown"),
            "class": data.get('class', "unknown"),
            "type": data.get('type', "unknown"),
            "place_rank": data.get('place_rank', "unknown"),
            "importance": data.get('importance', "unknown"),
            "addresstype": data.get('addresstype', "unknown"),
            "display_name": data.get('display_name', "unknown"),
            "house_number": data.get('address', {}).get('house_number', 'unknown'),
            "road": data.get('address', {}).get('road', 'unknown'),
            "suburb": data.get('address', {}).get('suburb', 'unknown'),
            "city": data.get('address', {}).get('city', 'unknown'),
            "state": data.get('address', {}).get('state', 'unknown'),
            "ISO3166-2-lvl4": data.get('address', {}).get('ISO3166-2-lvl4', 'unknown'),
            "region": data.get('address', {}).get('region', 'unknown'),
            "postcode": data.get('address', {}).get('postcode', 'unknown'),
            "country": data.get('address', {}).get('country', 'unknown'),
            "country_code": data.get('address', {}).get('country_code', 'unknown')

            })
    else:
        return jsonify({
            "status": "error",
            "message": "Не удалось получить данные"
        })

@app.route('/home/phone=<phone>')

def scanphone(phone):
    url = f"https://htmlweb.ru/geo/api.php?json&telcod={phone}"
    data = send_request(url, phone)

    if not data or not isinstance(data, dict):
        copyable.insert("1.0", "[!] Ошибка: не удалось получить данные.")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}[!] Ошибка: не удалось получить данные.")
        return

    if data.get("status_error"):
        copyable.insert("1.0", f"Ошибка API: {data.get('error_message', 'Не удалось получить данные.')}")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API: {data.get('error_message', 'Не удалось получить данные.')}")
        return

    if data.get("limit") is not None and data.get("limit") <= 0:
        copyable.insert("1.0", "Ошибка: лимит запросов исчерпан.")
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Лимит исчерпан!")
        return

    country = data.get('country', {}) or {}
    region = data.get('region', {}) or {}
    capital = data.get('capital', {}) or {}

    return jsonify ({
        "country": country.get('name', 'Не найдено'),
        "country fullname": country.get('fullname', '—'),
        "region": region.get('name', 'Не найдено'),
        "city": capital.get('name', 'Не найдено'),
        "post": capital.get('post', 'Не найдено'),
        "iso": country.get('iso', 'Не найдено'),
        "phone code": capital.get('telcod', 'Не найдено'),
        "operator_1": capital.get('oper_brand', 'Не найдено'),
        "operator_2": capital.get('def', 'Не найдено'),
        "capital": capital.get('name', 'Не найдено'),
        "lat": capital.get('latitude', '—'),
        "lon": capital.get('longitude', '—'),
        "Wiki": capital.get('wiki', '—'),
        "autocode": region.get('autocod', '—'),
        "location": country.get('location', '—'),
        "language": country.get('lang', '—')
        })

def send_request(url, phone):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(random.uniform(2, 5))
        if response.status_code == 200:
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен успешно: {phone}")
            return response.json()
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка: {response.status_code}")
            return None
    except Exception as er:
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка при отправке запроса: {er}")
        return None


app.run(host="0.0.0.0", port=5000, debug=True)