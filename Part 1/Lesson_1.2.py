# _2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests
import time
import json

def get_data(service, appid,city):
    while True:
        time.sleep(1)
        url = f'{service}?q={city}&appid={appid}'
        response = requests.get(url)
        if response.status_code == 200:
            print(url)
            break
    return response.json()

appid = 'e8df6ef1f00a4e5b8f6175322221905'
service = 'http://api.weatherapi.com/v1/forecast.json?key=e8df6ef1f00a4e5b8f6175322221905&q=saint-petersburg&days=5&aqi=no&alerts=no'
city = 'Saint-petersburg'
# city ='Manchester,uk'
response = get_data(service, appid, city)

print('Получен результат')
print(response)

with open('1.2_weather.json', 'w') as f:
    json_repo = json.dump(response, f)