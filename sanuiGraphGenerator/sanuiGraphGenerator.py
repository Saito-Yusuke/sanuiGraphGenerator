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
        self.initUI()

    def initUI(self):

        # gridオブジェクト
        grid = QVBoxLayout()

        # Labelオブジェクト
        howToUse1Label = QLabel('1. ')

        # CheckBoxオブジェクト
        headerCheckBox = QCheckBox('ヘッダーあり', self)
        headerCheckBox.toggle()

        # RadioButtonオブジェクト
        self.regLine1RadioButton = QRadioButton("なし")
        self.regLine2RadioButton = QRadioButton("y = x")
        self.regLine3RadioButton = QRadioButton("y = ax (a: 相関)")
        self.regLine1RadioButton.setChecked(True)

        # Buttonオブジェクト
        outPutButton = QPushButton("Output", self)
        outPutButton.resize(outPutButton.sizeHint())
        outPutButton.clicked.connect(self.outPutButtonClicked)

        # TextEditオブジェクト
        self.howToUseTextEdit = QTextEdit(self)

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
        self.howToUseGroupBox.setLayout(howToUseBox)
        
        grid.addWidget(headerCheckBox)
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