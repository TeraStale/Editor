import sys

# 1-04 add QtPrintSupport
from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport
from PyQt5.QtCore import Qt

# 3-01
from ext import *

# 4-01
import locale

DEFAULT_FILE_EXT = ".edt"

class Main(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # 1-03
        self.filename = ""

        # 4-04
        self.changesSaved = True

        self.initUI()
    

    # 1-03
    def new(self):
        spawn = Main(self)
        spawn.show()
    

    # 1-03
    def open(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл',".",f"(*{DEFAULT_FILE_EXT})")[0]
        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())
 
 
    # 1-03
    def save(self):
        if not self.filename:
            self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл')[0]
        if self.filename:
            if not self.filename.endswith(DEFAULT_FILE_EXT):
                self.filename += DEFAULT_FILE_EXT
            with open(self.filename,"wt") as file:
                file.write(self.text.toHtml())
            
            # 4-04
            self.changesSaved = True

    
    # 1-04
    def print(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    
    # 1-04
    def preview(self):
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()
 

    # 1-06
    def bulletList(self):
        cursor = self.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)
 

    # 1-06
    def numberList(self):
        cursor = self.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)


    # 1-07
    def cursorPosition(self):
        cursor = self.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.showMessage("Строка: {} | Столбец: {}".format(line,col))
    
    # 2-01
    def fontColorChanged(self):
        color = QtWidgets.QColorDialog.getColor()
        self.text.setTextColor(color)

    # 2-01
    def highlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self.text.setTextBackgroundColor(color)

    # 2-02
    def bold(self):
        if self.text.fontWeight() == QtGui.QFont.Bold:
            self.text.setFontWeight(QtGui.QFont.Normal)
        else:
            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):
        state = self.text.fontItalic()
        self.text.setFontItalic(not state)

    def underline(self):
        state = self.text.fontUnderline()
        self.text.setFontUnderline(not state)

    def strike(self):
        fmt = self.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):
        fmt = self.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):
        fmt = self.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.text.setCurrentCharFormat(fmt)
    
    # 2-03
    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)
    
    # 2-04
    def indent(self):
        cursor = self.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for n in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                cursor.insertText("\t")
                cursor.movePosition(direction)
        else:
            cursor.insertText("\t")

    def handleDedent(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        line = cursor.block().text()
        if line.startswith("\t"):
            cursor.deleteChar()
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()

    def dedent(self):
        cursor = self.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)
                cursor.movePosition(direction)
        else:
            self.handleDedent(cursor)

    # 2-05
    def toggleToolbar(self):
        state = self.toolbar.isVisible()
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):
        state = self.formatbar.isVisible()
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):
        state = self.statusbar.isVisible()
        self.statusbar.setVisible(not state)

    # 3-04
    def insertImage(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Вставить изображение',".","Изображения (*.png *.jpg *.bmp *.gif)")[0]
        if filename:
            image = QtGui.QImage(filename)
            if image.isNull():
                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                    "Ошибка открытия файла",
                    "Невозможно открыть файл изображения!",
                    QtWidgets.QMessageBox.Ok,
                    self)
                popup.show()
            else:
                cursor = self.text.textCursor()
                cursor.insertImage(image,filename)
    
    # 3-05
    def wordCount(self):
        wc = wordcount.WordCount(self)
        wc.getText()
        wc.show()

    # 4-03
    def removeRow(self):
        cursor = self.text.textCursor()
        table = cursor.currentTable()
        cell = table.cellAt(cursor)
        table.removeRows(cell.row(),1)

    # 4-03
    def removeCol(self):
        cursor = self.text.textCursor()
        table = cursor.currentTable()
        cell = table.cellAt(cursor)
        table.removeColumns(cell.column(),1)

    # 4-03
    def insertRow(self):
        cursor = self.text.textCursor()
        table = cursor.currentTable()
        cell = table.cellAt(cursor)
        table.insertRows(cell.row(),1)

    # 4-03
    def insertCol(self):
        cursor = self.text.textCursor()
        table = cursor.currentTable()
        cell = table.cellAt(cursor)
        table.insertColumns(cell.column(),1)

    # 4-03
    def context(self,pos):
        cursor = self.text.textCursor()
        table = cursor.currentTable()

        if table:
            menu = QtWidgets.QMenu(self)
            appendRowAction = QtWidgets.QAction("Добавить строку",self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))
            appendColAction = QtWidgets.QAction("Добавить столбец",self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))
            removeRowAction = QtWidgets.QAction("Удалить строку",self)
            removeRowAction.triggered.connect(self.removeRow)
            removeColAction = QtWidgets.QAction("Удалить столбец",self)
            removeColAction.triggered.connect(self.removeCol)
            insertRowAction = QtWidgets.QAction("Вставить строку",self)
            insertRowAction.triggered.connect(self.insertRow)
            insertColAction = QtWidgets.QAction("Вставить столбец",self)
            insertColAction.triggered.connect(self.insertCol)

            mergeAction = QtWidgets.QAction("Объединить ячейки",self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)

            splitAction = QtWidgets.QAction("Разделить ячейки",self)
            cell = table.cellAt(cursor)
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:
                splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))
            else:
                splitAction.setEnabled(False)

            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)
            menu.addSeparator()
            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)
            menu.addSeparator()
            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)
            menu.addSeparator()
            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            pos = self.mapToGlobal(pos)
            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)
            if self.formatbar.isVisible():
                pos.setY(pos.y() + 45)
            menu.move(pos)
            menu.show()

        else:
            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())
            self.text.contextMenuEvent(event)

    # 4-04
    def changed(self):
        self.changesSaved = False

    # 4-04
    def closeEvent(self,event):
        if self.changesSaved:
            event.accept()
        else:
            popup = QtWidgets.QMessageBox(self)
            popup.setWindowTitle('Редактор')
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("Документ был изменен!")
            popup.setInformativeText("Вы хотите сохранить изменения?")
            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)
            popup.setDefaultButton(QtWidgets.QMessageBox.Save)
            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()
                if not self.changesSaved:
                    event.ignore()
            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

    # 1-02
    def initToolbar(self):
        
        # 1-03
        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.png"),"Новый",self)
        self.newAction.setStatusTip("Создать новый документ")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)
        
        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open.png"),"Открыть...",self)
        self.openAction.setStatusTip("Открыть существующий документ")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)
        
        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"),"Сохранить",self)
        self.saveAction.setStatusTip("Сохранить документ")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        # 1-04
        self.printAction = QtWidgets.QAction(QtGui.QIcon("icons/print.png"),"Печать",self)
        self.printAction.setStatusTip("Печать документа")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.print)
 
        self.previewAction = QtWidgets.QAction(QtGui.QIcon("icons/preview.png"),"Предварительный просмотр...",self)
        self.previewAction.setStatusTip("Предварительный просмотр перед печатью")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)
        
        self.toolbar = self.addToolBar("Options")

        # 3-01
        self.findAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"),"Поиск и замена",self)
        self.findAction.setStatusTip("Поиск и замена текста в документе")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        # 1-05
        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"),"Вырезать",self)
        self.cutAction.setStatusTip("Удалить и скопировать текст в буфер обмена")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)
        
        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"),"Копировать",self)
        self.copyAction.setStatusTip("Копировать текст в буфер обмена")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)
        
        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"),"Вставить",self)
        self.pasteAction.setStatusTip("Вставить текст из буфера обмена")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)
        
        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"),"Отменить",self)
        self.undoAction.setStatusTip("Отменить последнее действие")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)
        
        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"),"Повторить",self)
        self.redoAction.setStatusTip("Повторить последнее отмененное действие")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)
        
        # 1-06
        self.bulletAction = QtWidgets.QAction(QtGui.QIcon("icons/bullet.png"),"Маркированный список",self)
        self.bulletAction.setStatusTip("Вставить маркированный список")
        self.bulletAction.setShortcut("Ctrl+Shift+B")
        self.bulletAction.triggered.connect(self.bulletList)
        
        self.numberedAction = QtWidgets.QAction(QtGui.QIcon("icons/number.png"),"Нумерованный список",self)
        self.numberedAction.setStatusTip("Вставить нумерованный список")
        self.numberedAction.setShortcut("Ctrl+Shift+L")
        self.numberedAction.triggered.connect(self.numberList)

        # 3-04
        imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.png"),"Вставить изображение",self)
        imageAction.setStatusTip("Вставить изображение")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        # 3-05
        wordCountAction = QtWidgets.QAction(QtGui.QIcon("icons/count.png"),"Статистика",self)
        wordCountAction.setStatusTip("Статистика документа")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        # 4-01
        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/calender.png"),"Вставить дату/время",self)
        dateTimeAction.setStatusTip("Вставить текущие дату/время")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        # 4-02
        tableAction = QtWidgets.QAction(QtGui.QIcon("icons/table.png"),"Вставить таблицу",self)
        tableAction.setStatusTip("Вставить таблицу")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(table.Table(self).show)

        # 1-03
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        # 1-04
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        # 1-05
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()
        
        # 3-01
        self.toolbar.addAction(self.findAction)

        # 3-04
        self.toolbar.addAction(imageAction)

        # 4-01
        self.toolbar.addAction(dateTimeAction)

        # 4-02
        self.toolbar.addAction(tableAction)

        # 3-05
        self.toolbar.addAction(wordCountAction)

        self.toolbar.addSeparator()
        
        # 1-06
        self.toolbar.addAction(self.bulletAction)
        self.toolbar.addAction(self.numberedAction)

        self.addToolBarBreak()

    
    # 1-02
    def initFormatbar(self):
        self.formatbar = self.addToolBar("Format")

        # 2-01
        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))

        fontSize = QtWidgets.QSpinBox(self)
        fontSize.setSuffix(" pt")
        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))
        fontSize.setValue(14)

        fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"),"Цвет текста",self)
        fontColor.triggered.connect(self.fontColorChanged)

        backColor = QtWidgets.QAction(QtGui.QIcon("icons/highlight.png"),"Цвет фона",self)
        backColor.triggered.connect(self.highlight)

        # 2-02
        boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"),"Полужирный",self)
        boldAction.setShortcut("Ctrl+B")
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"),"Курсив",self)
        italicAction.setShortcut("Ctrl+I")
        italicAction.triggered.connect(self.italic)

        underlAction = QtWidgets.QAction(QtGui.QIcon("icons/underline.png"),"Подчеркивание",self)
        underlAction.setShortcut("Ctrl+U")
        underlAction.triggered.connect(self.underline)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.png"),"Перечеркивание",self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("icons/superscript.png"),"Верхний индекс",self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("icons/subscript.png"),"Нижний индекс",self)
        subAction.triggered.connect(self.subScript)
        
        # 2-03
        alignLeft = QtWidgets.QAction(QtGui.QIcon("icons/align-left.png"),"По левому краю",self)
        alignLeft.setShortcut("Ctrl+L")
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("icons/align-center.png"),"По середине",self)
        alignCenter.setShortcut("Ctrl+E")
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("icons/align-right.png"),"По правому краю",self)
        alignRight.setShortcut("Ctrl+R")
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("icons/align-justify.png"),"По ширине",self)
        alignJustify.setShortcut("Ctrl+J")
        alignJustify.triggered.connect(self.alignJustify)

        # 2-04
        indentAction = QtWidgets.QAction(QtGui.QIcon("icons/indent.png"),"Увеличить отступ",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtWidgets.QAction(QtGui.QIcon("icons/dedent.png"),"Уменшить отступ",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        # 2-01
        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()

        # 2-02
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)
        self.formatbar.addSeparator()

        # 2-03
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)
        self.formatbar.addSeparator()

        # 2-04
        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)
        
    # 1-02
    def initMenubar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("Файл")
        edit = menubar.addMenu("Правка")
        view = menubar.addMenu("Вид")

        # 1-03
        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
    
        # 1-04
        file.addAction(self.printAction)
        file.addAction(self.previewAction)
    
        # 1-05
        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)

        # 2-05
        toolbarAction = QtWidgets.QAction("Панель инструментов",self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Панель форматирования",self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Строка состояния",self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)


    def initUI(self):
        # 1-02
        self.text = QtWidgets.QTextEdit(self)

        # 1-07
        self.text.setTabStopWidth(33)
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        
        self.setCentralWidget(self.text)
        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()
        self.statusbar = self.statusBar()
        
        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("Редактор")

        # 1-07
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        # 4-03
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        # 4-04
        self.text.textChanged.connect(self.changed)

def main():
    # 4-01
    locale.setlocale(locale.LC_ALL, "ru")
    
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
