from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import json
from urllib.request import urlopen
from datetime import datetime,timedelta,date
from translate import Translator
from langdetect import detect
from kivy.core.window import Window
class MyApp(App):
    Window.size = (1080, 2400)
    def translateStatus_ru(self,instance):
        lang = detect(self.status)
        translator = Translator(from_lang=lang,to_lang="ru")
        return translator.translate(self.status)
    def translateCity_ru(self,instance):
        lang = detect(self.city)
        translator = Translator(from_lang=lang,to_lang="ru")
        self.r = translator.translate(self.city)
        self.lbl_city.text = self.r
        print(self.r)
    def translateCity_en(self, instance):
        lang = detect(self.lbl_city.text)
        translator = Translator(from_lang=lang, to_lang="en")
        return translator.translate(self.lbl_city.text)
    def changeCity(self, instance):
        self.place = self.city_input.text
        self.lbl_city.text = self.city_input.text
        self.lbl_date.text = ''
        self.lbl_time.text = ''
        self.lbl_temperature.text = ''
        self.lbl_weather.text = ''
        self.lbl_recomend.text = ''
        # self.setWeather(self)
    def defineCity(self, instance):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        IP = data['ip']
        org = data['org']
        self.city = data['city']
        self.place = data['city']
        self.country = data['country']
        self.translateCity_ru(instance)
        self.lbl_date.text = ''
        self.lbl_time.text = ''
        self.lbl_temperature.text = ''
        self.lbl_weather.text = ''
        self.lbl_recomend.text = ''
        # self.setWeather(self)
    def setWeather(self, instance):
        try:
            config_dict = get_default_config()  # Инициализация get_default_config()
            config_dict['language'] = 'en'  # Установка языка
            # place = self.city  # Переменная для записи города
            # country = self.country  # Переменная для записи страны/кода страны
            country_and_place = self.translateCity_en(instance)  # Запись города и страны в одну переменную через запятую

            owm = OWM('904d2c1b517d94f646ca42dccaf5a55d')  # Ваш ключ с сайта open weather map
            mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
            observation = mgr.weather_at_place(country_and_place)
            # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город

            w = observation.weather
            status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
            print(status)
            print(self.translateStatus_ru())
            # w.wind()  # Узнаем скорость ветра
            # humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
            temp = w.temperature('celsius')[
                'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
            city_url = f'http://api.openweathermap.org/geo/1.0/direct?q={self.translateCity_en(instance)}&limit=1&appid=904d2c1b517d94f646ca42dccaf5a55d'
            city_response = urlopen(city_url)
            data_city_name = json.load(city_response)
            lat = data_city_name[0]['lat']
            lon = data_city_name[0]['lon']
            time_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=904d2c1b517d94f646ca42dccaf5a55d'
            time_responce = urlopen(time_url)
            time_city_data = json.load(time_responce)
            timezone = time_city_data['timezone']
            self.lbl_temperature.text = "Температура: " + str(round(temp)) + "°С" + ' / ' + str(round(temp*1.8 + 32)) + 'F'
            self.lbl_weather.text = "Состояние: " + self.translateStatus_ru()

            now = datetime.utcnow() + timedelta(hours=timezone//3600)
            now_date = date.today()
            self.lbl_date.text = "Дата: " + str(now_date)
            current_time = now.strftime("%H:%M:%S")
            self.lbl_time.text = "Время: " + str(current_time)
            if int(temp) > 0:
                Window.clearcolor = (1, 1, 0, 1)
            else:
                Window.clearcolor = (0, 0, 1, 1)

        except:
            self.lbl_city.text = 'Город не найден'

    def build(self):
        Window.clearcolor = (.45,.45,.45,1)
        bl = BoxLayout(orientation = 'vertical', padding=25)
        bl_text = BoxLayout(orientation='vertical')
        bl_buttons = BoxLayout(orientation='vertical',spacing=15, padding=(125,0,125,0))
        self.lbl_city = Label(text="Введите город", font_size="64", size_hint = (1, .6))
        self.lbl_date = Label(text="", font_size="64", size_hint=(1, .6))
        self.lbl_time = Label(text="", font_size="64", size_hint=(1, .6))
        self.lbl_temperature = Label(text="", font_size="64", size_hint=(1, .6))
        self.lbl_weather = Label(text="", font_size="64", size_hint=(1, .6))
        self.lbl_recomend = Label(text="Возьмите зонтик", font_size="64", size_hint=(1, .6))
        self.city_input = TextInput(text = '', hint_text = "Введите город:")
        bl_text.add_widget(self.lbl_city)
        bl_text.add_widget(self.lbl_date)
        bl_text.add_widget(self.lbl_time)
        bl_text.add_widget(self.lbl_temperature)
        bl_text.add_widget(self.lbl_weather)
        bl_text.add_widget(self.lbl_recomend)
        bl.add_widget(bl_text)
        bl_buttons.add_widget(self.city_input)
        bl_buttons.add_widget(Button(text="Изменить город",background_color=[.88,.88,.88,1], on_press=self.changeCity))
        bl_buttons.add_widget(Button(text="Определить город",background_color=[.88,.88,.88,1], on_press=self.defineCity))
        bl_buttons.add_widget(Button(text="Узнать погоду",background_color=[.88,.88,.88,1], on_press=self.setWeather))
        bl.add_widget(bl_buttons)
        return bl

if __name__ == "__main__":
    MyApp().run()
