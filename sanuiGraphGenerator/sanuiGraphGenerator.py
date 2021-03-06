#libraries
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lin
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.initUI()

    #dragの境界侵入時
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    #dropしたとき
    def dropEvent(self, event):
        event.accept()
        mimeData = event.mimeData()

    def initUI(self):

        # gridオブジェクト
        grid = QVBoxLayout()

        # Labelオブジェクト
        howToUse1Label = QLabel('1. csvファイルのみ扱い可能. ')
        howToUse2Label = QLabel('2. ヘッダーで次のようにカラム名をつける. ')
        howToUse3Label = QLabel('       横軸（CANデータから算出した総消費電力量）: x  ')
        howToUse4Label = QLabel('       縦軸1（走行による推定消費電力量）: y1  ')
        howToUse5Label = QLabel('       縦軸2（電装品による推定消費電力量）: y2  ')
        howToUse6Label = QLabel('       縦軸3（エアコンによる推定消費電力量）: y3  ')
        howToUse7Label = QLabel('3. csvファイルをウィンドウ内にドラッグ&ドロップ. ')
        howToUse8Label = QLabel('4. 回帰直線を選ぶ. ')
        howToUse9Label = QLabel('5. Outputボタンをクリックするとグラフが出力される. ')

        # RadioButtonオブジェクト
        self.regLine1RadioButton = QRadioButton("なし")
        self.regLine2RadioButton = QRadioButton("y = x")
        self.regLine3RadioButton = QRadioButton("y = ax")
        self.regLine4RadioButton = QRadioButton("y = ax + b")
        self.regLine1RadioButton.setChecked(True)

        # Buttonオブジェクト
        outPutButton = QPushButton("Output", self)
        outPutButton.resize(outPutButton.sizeHint())
        outPutButton.clicked.connect(self.outPutButtonClicked)

        # 回帰直線を指定するWidgetグループ
        self.regLineGroupBox = QGroupBox("回帰直線")
        regLineBox = QVBoxLayout()
        regLineBox.addWidget(self.regLine1RadioButton)
        regLineBox.addWidget(self.regLine2RadioButton)
        regLineBox.addWidget(self.regLine3RadioButton)
        regLineBox.addWidget(self.regLine4RadioButton)
        self.regLineGroupBox.setLayout(regLineBox)

        # How to Use関連のwidgetグループ
        self.howToUseGroupBox = QGroupBox("How to Use")
        howToUseBox = QVBoxLayout()
        howToUseBox.addWidget(howToUse1Label)
        howToUseBox.addWidget(howToUse2Label)
        howToUseBox.addWidget(howToUse3Label)
        howToUseBox.addWidget(howToUse4Label)
        howToUseBox.addWidget(howToUse5Label)
        howToUseBox.addWidget(howToUse6Label)
        howToUseBox.addWidget(howToUse7Label)
        howToUseBox.addWidget(howToUse8Label)
        howToUseBox.addWidget(howToUse9Label)
        self.howToUseGroupBox.setLayout(howToUseBox)
        
        grid.addWidget(self.regLineGroupBox)
        grid.addWidget(outPutButton)
        grid.addWidget(self.howToUseGroupBox)

        self.setLayout(grid)
        self.setWindowTitle('Sanui Gragh Generator')
        self.show()

    # 出力ボタンが押された時の処理
    def outPutButtonClicked(self):
        sender = self.sender()

        df = pd.read_csv('sample.csv').dropna()
        header = df.columns.values.tolist()
        data = df.values

        xi = df['x'].T
        yi = df['y1'].T + df['y2'] + df['y3'].T

        n = len(data)
        print("n = " + str(n))
        sum_x = sum(xi)
        sum_y = sum(yi)
        sum_xx = sum(xi ** 2)
        sum_xy = sum(xi * yi)

        if self.regLine2RadioButton.isChecked():
            slope = 1
            intercept = 0
        elif self.regLine3RadioButton.isChecked():
            slope = sum_xy / sum_xx
            intercept = 0
        elif self.regLine4RadioButton.isChecked():
            #最小二乗法による係数決定
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
            intercept = (sum_xx * sum_y - sum_xy * sum_x) / (n * sum_xx - sum_x ** 2)

        #回帰直線との標準偏差
        sigma = np.std(yi - slope * xi - intercept)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        left = np.array(df['x'].T)
        height_y1 = np.array(df['y1'].T)
        height_y2 = np.array(df['y2'].T)
        height_y3 = np.array(df['y3'].T)
        regLine = lin.Line2D([0, 12], [intercept, slope * 12 + intercept], linewidth = 3, color = "black")
        regLine_sigma = lin.Line2D([0, 12], [intercept + sigma, slope * 12 + intercept + sigma], color = "black")
        regLine_2sigma = lin.Line2D([0, 12], [intercept + 2 * sigma, slope * 12 + intercept + 2 * sigma], color = "black")
        regLine_minus_sigma = lin.Line2D([0, 12], [intercept - sigma, slope * 12 + intercept - sigma], color = "black")
        regLine_minus_2sigma = lin.Line2D([0, 12], [intercept - 2 * sigma, slope * 12 + intercept - 2 * sigma], color = "black")
        bar_y1 = plt.bar(left, height_y1, color = '#006400', width = 0.05)
        bar_y2 = plt.bar(left, height_y2, bottom = height_y1, color = '#ffd700', width = 0.05)
        bar_y3 = plt.bar(left, height_y3, bottom = height_y1 + height_y2, color = '#4169e1', width = 0.05)

        if self.regLine1RadioButton.isChecked():
            pass
        else:
            ax.add_line(regLine)
            ax.add_line(regLine_sigma)
            ax.add_line(regLine_2sigma)
            ax.add_line(regLine_minus_sigma)
            ax.add_line(regLine_minus_2sigma)
            print("回帰直線の傾き = " + str(round(slope, 3)))
            print("回帰直線のy切片 = " + str(round(intercept, 3)))
            print("回帰直線との標準偏差 = " + str(round(sigma, 3)))

        plt.xlim([0, 10])
        plt.ylim([0, 10])
        plt.title("ECOLOG Estimation", fontsize = 20)
        plt.xlabel("Energy Consumption from CAN [kWh]", fontsize = 16)
        plt.ylabel("Estimated Energy Consumption [kWh]", fontsize = 16)
        ax.set_aspect('equal')
        plt.legend((bar_y1[0], bar_y2[0], bar_y3[0]), ("ECOLOG Estimation", "AUX Consumption", "Air Conditioner Estimation"), fontsize = 16)
        plt.show()

if __name__== "__main__":
    app = QApplication(sys.argv)
    win = InputWindow()
    sys.exit(app.exec_())