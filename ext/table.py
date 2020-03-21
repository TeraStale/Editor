# 4-02
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

class Table(QtWidgets.QDialog):
    def __init__(self,parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.initUI()
 
    def initUI(self):
        rowsLabel = QtWidgets.QLabel("Строки: ",self)
        self.rows = QtWidgets.QSpinBox(self)
        colsLabel = QtWidgets.QLabel("Столбцы",self)
        self.cols = QtWidgets.QSpinBox(self)
        spaceLabel = QtWidgets.QLabel("Между ячейками",self)
        self.space = QtWidgets.QSpinBox(self)
        padLabel = QtWidgets.QLabel("Поля ячеек",self)
        self.pad = QtWidgets.QSpinBox(self)
        self.pad.setValue(10)
        insertButton = QtWidgets.QPushButton("Вставка",self)
        insertButton.clicked.connect(self.insert)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(rowsLabel,0,0)
        layout.addWidget(self.rows,0,1)
        layout.addWidget(colsLabel,1,0)
        layout.addWidget(self.cols,1,1)
        layout.addWidget(padLabel,2,0)
        layout.addWidget(self.pad,2,1)
        layout.addWidget(spaceLabel,3,0)
        layout.addWidget(self.space,3,1)
        layout.addWidget(insertButton,4,0,1,2)
        self.setWindowTitle("Вставка таблицы")
        self.setGeometry(300,300,200,100)
        self.setLayout(layout)

    def insert(self):
        cursor = self.parent.text.textCursor()
        rows = self.rows.value()
        cols = self.cols.value()

        if not rows or not cols:
            popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                "Ошибка параметра",
                "Количество строк или столбцов не может быть нулевым!",
                QtWidgets.QMessageBox.Ok,
                self)
            popup.show()
        else:
            padding = self.pad.value()
            space = self.space.value()
            fmt = QtGui.QTextTableFormat()
            fmt.setCellPadding(padding)
            fmt.setCellSpacing(space)
            cursor.insertTable(rows,cols,fmt)
            self.close()
