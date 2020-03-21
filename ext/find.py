# 3-01
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

import re

class Find(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
        
        self.initUI()

        # 3-02
        self.lastStart = 0
    
    # 3-02
    def find(self):
        text = self.parent.text.toPlainText()
        query = self.findField.toPlainText()
        cursor = self.parent.text.textCursor()
        if cursor.atEnd():
            self.parent.text.moveCursor(QtGui.QTextCursor.Start)    
        elif self.lastStart != cursor.position():
            self.lastStart = cursor.position()

        if self.normalRadio.isChecked():
            self.lastStart = text.find(query, self.lastStart)
            if self.lastStart >= 0:
                end = self.lastStart + len(query)
                self.moveCursor(self.lastStart,end)
            else:
                self.lastStart = 0
                self.parent.text.moveCursor(QtGui.QTextCursor.End)

        else:
            pattern = re.compile(query)
            match = pattern.search(text,self.lastStart)
            if match:
                self.lastStart = match.start()
                self.moveCursor(self.lastStart, match.end())
            else:
                self.lastStart = 0
                self.parent.text.moveCursor(QtGui.QTextCursor.End)
        
        self.hide()
    
    # 3-02
    def moveCursor(self,start,end):
        cursor = self.parent.text.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,end - start)
        self.parent.text.setTextCursor(cursor)

    def initUI(self):

        findButton = QtWidgets.QPushButton("Поиск",self)
        replaceButton = QtWidgets.QPushButton("Замена",self)
        allButton = QtWidgets.QPushButton("Заменить все",self)

        self.normalRadio = QtWidgets.QRadioButton("Обычный",self)
        regexRadio = QtWidgets.QRadioButton("RegEx",self)

        self.findField = QtWidgets.QTextEdit(self)
        self.findField.resize(250,50)

        self.replaceField = QtWidgets.QTextEdit(self)
        self.replaceField.resize(250,50)
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.findField,1,0,1,4)
        layout.addWidget(self.normalRadio,2,2)
        layout.addWidget(regexRadio,2,3)
        layout.addWidget(findButton,2,0,1,2)
        layout.addWidget(self.replaceField,3,0,1,4)
        layout.addWidget(replaceButton,4,0,1,2)
        layout.addWidget(allButton,4,2,1,2)

        self.setGeometry(300,300,360,250)
        self.setWindowTitle("Поиск и замена")
        self.setLayout(layout)

        self.normalRadio.setChecked(True)
        self.findField.setFocus()

        # 3-02
        findButton.clicked.connect(self.find)

        #3-03
        replaceButton.clicked.connect(self.replace)
        allButton.clicked.connect(self.replaceAll)

    # 3-03
    def replace(self):
        result = False
        self.find()
        cursor = self.parent.text.textCursor()
        if self.lastStart >= 0 and cursor.hasSelection():
            cursor.insertText(self.replaceField.toPlainText())
            self.parent.text.setTextCursor(cursor)
            result = True
        self.hide()
        return result

    def replaceAll(self):
        self.lastStart = 0
        self.parent.text.moveCursor(QtGui.QTextCursor.Start)
        while self.replace():
            pass
        self.hide()
        