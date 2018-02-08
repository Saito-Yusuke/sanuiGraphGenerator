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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, QDropEvent):
        return super().dropEvent(QDropEvent)

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
        self.regLine3RadioButton = QRadioButton("y = ax (a: 相関)")
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

        fig = plt.figure()



if __name__== "__main__":
    app = QApplication(sys.argv)
    win = InputWindow()
    sys.exit(app.exec_())