# 0.6 날씨 이미지 추가
# 0.6 엔터 입력시 작동 추가
# 0.6 프로그램 시작 시 현재 지역 날씨 추가
# v0.6 공란으로 검색 시 경고창 출력 후 현재 지역 날씨 출력
# v0.7 해외 도시 날씨 검색 기능 추가
# v0.8 도시명 입력 오류시 처리 추가

#  app 만드는 기본모듈
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic  # QT Designer에서 만든 ui를 불러오는 모듈
from PyQt5.QtCore import Qt  # 화면 앞으로 보내기

#  고해상도 모니터용---------------------------------------
from os import environ
import multiprocessing as mp
# ---------------------------------------------------------

import requests
from bs4 import BeautifulSoup


form_class = uic.loadUiType("ui/weather.ui")[0]
# QT Designer에서 만든 외부 ui 불러오기


class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자 호출
        self.setupUi(self)  # 불러온 ui 파일을 연결. 윈도우 app 생성시 거의 여기까지 유사하게 함.

        self.setWindowTitle("네이버 날씨 프로그램")  # 윈도우 제목
        self.setWindowIcon(QIcon("img/weather.png"))  # 윈도우 아이콘
        self.statusBar().showMessage("네이버 날씨 앱 v0.8")

        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 항상 위 옵션

        self.weather_search(1)  # 프로그램 실행시 자동으로 한번 실행. 공란으로 검색하니까 현재 지역으로 조회

        self.weather_btn.clicked.connect(self.weather_search_call)  # 날씨 조회 버튼 클릭시 weather_search 메소드 호출
        self.area_input_edit.returnPressed.connect(self.weather_search_call)  # enter 입력시 작동
        
    def weather_search_call(self):
        self.weather_search(0)

    def weather_search(self, startFlag):
        inputArea = self.area_input_edit.text()  # 사용자가 입력한 지역명 텍스트 가져오기

        if inputArea == "" and startFlag != 1:
            QMessageBox.information(self, "날씨정보", "지역을 입력하지 않으시면\n현재 지역의 날씨가 출력됩니다")
        # 처음 자동실행하면 경고창이 떠서 함수를 추가해서 해결

        html = requests.get(f"https://search.naver.com/search.naver?query={inputArea}+날씨")
        soup = BeautifulSoup(html.text, "html.parser")
        # print(soup.prettify())

        try:
            ### 국내도시 날씨 처리. 오류시 밑에 해외도시 처리로

            # 한글날씨 - 조회수가 너무 많아서 f12로 웹브라우저에서 찾음
            weatherText = soup.find("span",{"class":"weather before_slash"}).text.strip()
            print(weatherText)

            # 현재온도
            nowTemperText = soup.find("div",{"class":"temperature_text"}).text.strip()  # 현재온도
            nowTemperText = nowTemperText[5:]  # 현재 온도16.6° 를 슬라이싱
            print(nowTemperText)

            # 지역
            areaText = soup.find("h2", {"class": "title"}).text.strip()  # 날씨조회 지역이름
            print(areaText)

            # 어제날씨 - 한글날씨 옆에 있어서 브라우저에서 같이 찾음
            yesterdayTempText = soup.find("p",{"class":"summary"}).text.strip()
            yesterdayTempText = yesterdayTempText[:15].strip()
            print(yesterdayTempText) #  어제보다 0.3° 높아요  구름많음

            # 체감온도 - 브라우저에서 찾음. 파이참보다 더 편함
            senseTemperText = soup.find("dd", {"class": "desc"}).text.strip()
            print(senseTemperText)

            # 미세먼지
            todayWeatherInfo = soup.select("ul.today_chart_list>li")  # 리스트 형태로 반환 -> 미세먼지, 초미세먼지, 자외선, 일몰
            # print(todayWeatherInfo)
            dustInfo1 = todayWeatherInfo[0].find("span",{"class":"txt"}).text.strip()  # 미세먼지 정보
            dustInfo2 = todayWeatherInfo[1].find("span", {"class": "txt"}).text.strip()  # 초미세먼지 정보
            print(dustInfo1)
            print(dustInfo2)

            # ui 해당 label에 크롤링한 텍스트 출력
            self.weather_area_label.setText(areaText)
            self.now_temper_label.setText(nowTemperText)
            # self.weather_image_label.setText(weatherText)
            self.weather_image(weatherText)
            self.yester_temp_label.setText(yesterdayTempText)
            self.sense_temper_label.setText(senseTemperText)
            self.dust1_info_label.setText(dustInfo1)
            self.dust2_info_label.setText(dustInfo1)

        except:
            try:
                ### 해외도시 날씨 처리

                # 지역
                areaText = soup.find("h2", {"class": "title"}).text.strip()  # 날씨조회 지역이름
                print(areaText)
                # 현재온도
                # 10˚ 맑음(낮) 체감온도 9˚ -> 슬라이싱 하긴 힘듬. 글자수가 항상 일치하지 않을 수 있음.
                # nowTemperText = soup.find("div", {"class": "temperature_text"}).text.strip()
                todayWeatherInfoText = soup.find("div", {"class": "temperature_text"})  # 해외도시 날씨 정보(태그)
                print(todayWeatherInfoText)

                nowTemperText = soup.select("div.temperature_text>strong")  # 현재온도(list 타입으로 반환)
                # print(nowTemperText)  # [<strong><span class="blind">현재 온도</span>10<span class="celsius">°</span></strong>]
                # print(nowTemperText[0].text.strip())  # 현재 온도10°
                nowTemperText = nowTemperText[0].text.strip()[5:]  # 해외도시 현재 온도
                # print(nowTemperText)

                senseTemperText = soup.select("p.summary>span.text")  # [<span class="text">체감온도 <em>9°</em></span>]
                # print(senseTemperText[0].text.strip())  # 체감온도 9°
                senseTemperText = senseTemperText[0].text.strip()[5:]  # 해외도시 체감 온도
                # print(senseTemperText)

                weatherText = soup.select("div.temperature_text>p.summary")
                # print(weatherText)  # [<p class="summary">맑음(낮) <span class="text">체감온도 <em>9°</em></span></p>]
                weatherText = weatherText[0].text.strip()

                weatherText2 = ""
                for char in weatherText:
                    if char == "(":
                        break
                    weatherText2 = weatherText2 + char

                print(weatherText2)  # 해외도시 현재 날씨
                weatherText = weatherText2.strip()

                ## 없는 정보 - 로 표시
                dustInfo1 = "-"
                dustInfo2 = "-"
                yesterdayTempText = "-"

                # ui 해당 label에 크롤링한 텍스트 출력
                self.weather_area_label.setText(areaText)
                self.now_temper_label.setText(nowTemperText)
                # self.weather_image_label.setText(weatherText)
                self.weather_image(weatherText)
                self.yester_temp_label.setText(yesterdayTempText)
                self.sense_temper_label.setText(senseTemperText)
                self.dust1_info_label.setText(dustInfo1)
                self.dust2_info_label.setText(dustInfo1)
            except:
                QMessageBox.warning(self, "입력오류", "입력하신 지역명은 존재하지 않는 지역명입니다.\n지역명 확인 후 입력하세요.")
                self.area_input_edit.clear()
    def weather_image(self, weather_text):
        if "맑음" in weather_text:
            weatherImage = QPixmap("img/sun.png")  # 준비한 이미지 불러와서 저장
        elif "흐림" in weather_text:
            weatherImage = QPixmap("img/cloud.png")
        elif "구름" in weather_text:
            weatherImage = QPixmap("img/cloud.png")
        elif "비" in weather_text:
            weatherImage = QPixmap("img/rain.png")
        elif "소나기" in weather_text:
            weatherImage = QPixmap("img/rain.png")
        elif "눈" in weather_text:
            weatherImage = QPixmap("img/snow.png")
        else:
            self.weather_image_label.setText(weather_text)  # 일치된 이미지가 없을 경우.
            weatherImage = 1

        if weatherImage != 1:  # 일치된 이미지가 있을 때만
            self.weather_image_label.setPixmap(QPixmap(weatherImage))  # label에 이미지 출력


#  고해상도 모니터용 코드. -------------------------------------------------
def suppress_qt_warnings():  # 해상도별 글자크기 강제 고정하는 함수
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"
# 해상도 고정 함수 호출
suppress_qt_warnings()
mp.freeze_support()
#-------------------------------------------------------------------------


app = QApplication(sys.argv)
win = WeatherApp()  # 이렇게 하면 화면에 나타났다가 사라짐. 아래를 해주면 나타났다가 엑스를 누를 때 까지 실행 됨
win.show()  # 이 문장의 위치가 손으로 만든 것 하고 차이.
sys.exit(app.exec_())