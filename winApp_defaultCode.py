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

form_class = uic.loadUiType("ui/weather.ui")[0]


# QT Designer에서 만든 외부 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자 호출
        self.setupUi(self)  # 불러온 ui 파일을 연결. 윈도우 app 생성시 거의 여기까지 유사하게 함.

        self.setWindowTitle("구글 한줄 번역기")  # 윈도우 제목
        self.setWindowIcon(QIcon("img/weather.png"))  # 윈도우 아이콘
        self.statusBar().showMessage("네이버 날씨 앱 v0.5")

        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 항상 위 옵션


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