import sys
from notebook import Notebook
# from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from guinote import Ui_MainWindow
# from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.notebook = Notebook()
        self.setWindowTitle("My GUI App")
        self.tableWidget.itemClicked.connect(self.task_clicked)
        self.btnTaskAdd.clicked.connect(self.task_add)
        self.btnTaskDel.clicked.connect(self.task_del)
        self.btnCancel.clicked.connect(self.cancel_clicked)
        self.bntOk.clicked.connect(self.save_clicked)
        self.btnTagEdit.clicked.connect(self.tag_edit)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ltag.setSpacing(3)
        self.lid.hide()
        self.load_note()
        self.show_rec(0)

    def load_note(self):
        data = self.notebook.get_notes()
        rows = len(data)
        cols = len(data[0])
        # print(f"{rows=}\n{cols=}")
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setHorizontalHeaderLabels(["id", "parent", "Notes", "content", "ts", "tag"])
        self.tableWidget.hideColumn(0)
        self.tableWidget.hideColumn(1)
        self.tableWidget.hideColumn(3)
        self.tableWidget.hideColumn(4)
        self.tableWidget.hideColumn(5)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        for row in range(rows):
            # print(data[row])
            # print(data[row]["id"])
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(data[row]["id"])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(data[row]["parentid"])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(data[row]["subject"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(data[row]["content"]))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(data[row]["ts"].strftime("%d.%m.%y %H:%M"))))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(data[row]["tag"])))

    def show_rec(self, row):
        lid = self.tableWidget.item(row, 0).text()
        subj = self.tableWidget.item(row, 2).text()
        content = self.tableWidget.item(row, 3).text()
        fromdate = self.tableWidget.item(row, 4).text()
        tag = self.tableWidget.item(row, 5).text()
        # print(tag)
        tags = self.notebook.get_tags(int(tag))
        self.ltag.clear()
        self.ltag.addItems(tags)
        # print(tags)

        self.lid.setText(lid)
        self.esubject.setText(subj)
        self.lfromdate.setText(fromdate)
        self.econtent.setText(content)

    def task_clicked(self, item):
        row = item.row()
        self.show_rec(row)

    def task_add(self):
        pass

    def task_del(self):
        pass

    def cancel_clicked(self):
        # print(self.lid.text())
        self.show_rec(self.tableWidget.currentRow())

    def save_clicked(self):
        self.notebook.update_note(self.lid.text(), self.esubject.text(), self.econtent.toPlainText())
        self.load_note()

    def tag_edit(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
