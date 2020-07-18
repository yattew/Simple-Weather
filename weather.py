from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import requests
import sys
import datetime
import geocoder
from geopy.geocoders import Nominatim
def getloc():
    g = geocoder.ip('me')
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(" ".join(map(lambda x: str(x),g.latlng)), exactly_one=True)
    address = location.raw['address']
    city = address.get('city', '')
    return city
class weather:
    def __init__(self):
        api_address = "http://api.openweathermap.org/data/2.5/weather?appid=a579fbb4b1588d97589c22b21b55abe3&q="
        city = getloc()
        url = api_address + city
        self.json_data = requests.get(url).json()
    def get_temp(self):return str(round(self.json_data["main"]["temp"]-273.15))+u"\N{DEGREE SIGN}"+"C"
    def get_humidity(self):return str(self.json_data["main"]["humidity"]) + "%"
    def get_desc(self):return str(self.json_data["weather"][0]["description"])
    def get_sun_rise_set(self,r_s):
        time = datetime.datetime.fromtimestamp(int(self.json_data["sys"][r_s])).strftime('%Y-%m-%d %H:%M:%S')
        hour,min = map(lambda x : int(x),time.split()[1].split(":")[:2])
        if hour>12:hour-=12
        return str(hour) + ":" + str(min)
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200,200,300,400)
        self.setWindowTitle("New Window")
        self.weather = weather()
        self.initUI()
    def initUI(self):
        self.label_weather = QtWidgets.QLabel(self)
        self.label_weather.setFont(QFont("Arial",50))
        self.label_weather.move(75, 50)
        self.label_description = QtWidgets.QLabel(self)
        self.label_description.setFont(QFont("Arial",20))
        self.label_description.move(120,130)
        self.label_humidity = QtWidgets.QLabel(self)
        self.label_humidity.setFont(QFont("Arial", 20))
        self.label_humidity.move(20, 270)
        self.label_sun_rise_set = QtWidgets.QLabel(self)
        self.label_sun_rise_set.setFont(QFont("Arial", 20))
        self.label_sun_rise_set.move(175, 260)
        self.set_data()
    def set_data(self):
        self.label_weather.setText(self.weather.get_temp())
        self.label_weather.adjustSize()
        self.label_description.setText(self.weather.get_desc())
        self.label_description.adjustSize()
        self.label_humidity.setText(f"Humidity:\n   {self.weather.get_humidity()}")
        self.label_humidity.adjustSize()
        self.label_sun_rise_set.setText(f"""Sunrise:\n {self.weather.get_sun_rise_set("sunrise")} A.M\nSunset:\n  {self.weather.get_sun_rise_set("sunset")} P.M""")
        self.label_sun_rise_set.adjustSize()
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QtCore.Qt.white)
        painter.drawLine(0, 250, 300, 250)
        painter.drawLine(150,250,150,400)
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
window()