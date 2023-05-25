import requests
city = 'Moscow,RU'
res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'q': 'Moscow,RU', 'units': 'metric', 'lang': 'ru', 'APPID': '1041a545d05a6aef5e469fba7b7b3340'})
data = res.json()
print("Город:", city)
print("Скорость ветра: ", data['wind']['speed'])
print("Видимость: ", data['visibility'])

"""""
import requests
res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'q': 'Moscow,RU', 'units': 'metric', 'lang': 'ru', 'APPID': '1041a545d05a6aef5e469fba7b7b3340'})
data = res.json()
print("Прогноз погоды на неделю:")
for i in data['list']:
    print("Дата: ", i['dt_txt'])
    print("Скорость ветра: ", i['wind']['speed'])
    print("Видимость: ", i['visibility'])
    print("____________________________")
"""""
