# v0.6 날씨 이미지 추가
# v0.6 날씨 지역 입력 후 엔터키 이벤트 처리
# v0.6 프로그램 실행 시 현재 지역 날씨 출력 추가
# v0.6 공란으로 검색 시 경고창 출력 후 현재 지역 날씨 출력


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic  # QT Designer에서 만든 ui를 불러오는 모듈
from PyQt5.QtCore import Qt

from os import environ
import multiprocessing as mp

import requests
from bs4 import BeautifulSoup

form_class = uic.loadUiType("ui/weather.ui")[0]


# QT Designer에서 만든 외부 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자 호출
        self.setupUi(self)  # 불러온 ui 파일을 연결

        self.setWindowTitle("네이버 날씨 프로그램")  # 윈도우 제목 설정
        self.setWindowIcon(QIcon("img/weather_icon.png"))  # 윈도우 아이콘 설정
        self.statusBar().showMessage("네이버 날씨 앱 v0.6")  # 윈도우 상태 표시줄 설정
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 항상 위에 옵션

        self.weather_search(1)  # 프로그램 실행시 자동으로 날씨 조회 결과 출력->공란으로 검색->현재지역의 날씨가 출력
        self.weather_btn.clicked.connect(self.weather_search_call)  # 날씨 조회 버튼 클릭시 weather_search 메소드 호출
        self.area_input_edit.returnPressed.connect(self.weather_search_call)  # 엔터 이벤트 처리

    def weather_search_call(self):
        self.weather_search(0)

    def weather_search(self, startFlag):  # 날씨 조회 메소드
        inputArea = self.area_input_edit.text()  # 사용자가 입력한 지역명 텍스트 가져오기
        if inputArea == "" and startFlag != 1:
            QMessageBox.information(self, "날씨정보", "지역을 입력하지 않으시면\n현재 지역의 날씨가 출력됩니다.")

        html = requests.get(f"https://search.naver.com/search.naver?query={inputArea}+날씨")
        soup = BeautifulSoup(html.text, "html.parser")
        # print(soup.prettify())
        nowTemperText = soup.find("div", {"class": "temperature_text"}).text.strip()  # 현재 온도
        nowTemperText = nowTemperText[5:]
        print(nowTemperText)
        areaText = soup.find("h2", {"class": "title"}).text.strip()  # 날씨 조회 지역이름
        print(areaText)
        weatherText = soup.find("span", {"class": "weather before_slash"}).text.strip()  # 오늘 날씨 텍스트
        print(weatherText)
        yesterdayTempText = soup.find("p", {"class": "summary"}).text.strip()  # 어제와의 날씨 비교
        # print(yesterdayTempText[:15].strip())
        yesterdayTempText = yesterdayTempText[:15].strip()
        print(yesterdayTempText)
        senseTemperText = soup.find("dd", {"class": "desc"}).text.strip()  # 체감온도
        print(senseTemperText)
        todayWeatherInfo = soup.select("ul.today_chart_list>li")  # 리스트 형태로 반환->미세먼지,초미세먼지,자외선,일몰
        # print(todayWeatherInfo)
        dustInfo1 = todayWeatherInfo[0].find("span", {"class": "txt"}).text.strip()  # 미세먼지 정보
        dustInfo2 = todayWeatherInfo[1].find("span", {"class": "txt"}).text.strip()  # 초미세먼지 정보
        print(dustInfo1)
        print(dustInfo2)

        # ui 해당 label에 크롤링한 텍스트 출력
        self.weather_area_label.setText(areaText)
        self.now_temper_label.setText(nowTemperText)
        # self.weather_image_label.setText(weatherText)
        self.weather_image(weatherText)  # 이미지 출력해주는 메소드 호출
        self.yester_temper_label.setText(yesterdayTempText)
        self.sense_temper_label.setText(senseTemperText)
        self.dust1_info_label.setText(dustInfo1)
        self.dust2_info_label.setText(dustInfo2)

    def weather_image(self, weather_text):
        if "맑음" in weather_text:
            weatherImage = QPixmap("img/sun.png")  # 준비한 이미지 불러와서 저장
        elif "흐림" in weather_text:
            weatherImage = QPixmap("img/cloud.png")
        elif "구름" in weather_text:
            weatherImage = QPixmap("img/cloud.png")  # 준비한 이미지 불러와서 저장
        elif "비" in weather_text:
            weatherImage = QPixmap("img/rain.png")  # 준비한 이미지 불러와서 저장
        elif "소나기" in weather_text:
            weatherImage = QPixmap("img/rain.png")  # 준비한 이미지 불러와서 저장
        elif "눈" in weather_text:
            weatherImage = QPixmap("img/snow.png")  # 준비한 이미지 불러와서 저장
        else:
            self.weather_image_label.setText(weather_text)
            weatherImage = 1
            # 준비한 날씨 텍스트가 아닌 경우 해당 날씨를 텍스트로 출력
        if weatherImage != 1:
            self.weather_image_label.setPixmap(QPixmap(weatherImage))  # label에 이미지 출력


def suppress_qt_warnings():  # 해상도별 글자크기 강제 고정하는 함수
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


# 해상도 고정 함수 호출
suppress_qt_warnings()
mp.freeze_support()

app = QApplication(sys.argv)
Win = WeatherApp()
Win.show()
sys.exit(app.exec_())