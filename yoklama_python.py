

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form5(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(944, 525)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 30, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(160, 30, 151, 31))
        self.comboBox.setStyleSheet("background-color:rgb(13,17,47);border:none;\n"
"color:white;padding-left:10px;padding-right:10px")
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(220, 460, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(13,17,47);border:none;border-radius:15px;\n"
"color:white;padding-left:10px;padding-right:10px")
        self.pushButton.setObjectName("pushButton")
        self.img_label = QtWidgets.QLabel(Form)
        self.img_label.setGeometry(QtCore.QRect(30, 80, 581, 371))
        self.img_label.setFrameShape(QtWidgets.QFrame.Box)
        self.img_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.img_label.setLineWidth(6)
        self.img_label.setText("")
        self.img_label.setObjectName("img_label")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(640, 80, 281, 371))
        self.listWidget.setObjectName("listWidget")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(620, 40, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(730, 470, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        self.comboBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Yoklama Sistemi"))
        self.label.setText(_translate("Form", "Ders Seçiniz:"))
        self.pushButton.setText(_translate("Form", "Yoklamayı Başlat"))
        self.label_2.setText(_translate("Form", "Yoklamaya Dahil Olan Öğrenciler :"))
        self.pushButton_2.setText(_translate("Form", "İndir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form5()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
