# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kaydol.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(404, 354)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(0, 0, 401, 351))
        self.label_7.setStyleSheet("\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1 y2:0.477, stop:0 rgba(11,131,120,219), stop:1 rgba(85,98,112,226));\n"
"    color:rgba(255,255,255,210);\n"
"    \n"
"\n"
"    \n"
"\n"
"border-bottom-right-radius:50px;\n"
"border-bottom-left-radius:50px;\n"
"border-top-left-radius:50px;\n"
"border-top-right-radius:50px;")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.yoneticiAd = QtWidgets.QLineEdit(Form)
        self.yoneticiAd.setGeometry(QtCore.QRect(30, 80, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.yoneticiAd.setFont(font)
        self.yoneticiAd.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.yoneticiAd.setText("")
        self.yoneticiAd.setObjectName("yoneticiAd")
        self.yoneticiSoyad = QtWidgets.QLineEdit(Form)
        self.yoneticiSoyad.setGeometry(QtCore.QRect(30, 120, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.yoneticiSoyad.setFont(font)
        self.yoneticiSoyad.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.yoneticiSoyad.setObjectName("yoneticiSoyad")
        self.yoneticikadi = QtWidgets.QLineEdit(Form)
        self.yoneticikadi.setGeometry(QtCore.QRect(30, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.yoneticikadi.setFont(font)
        self.yoneticikadi.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.yoneticikadi.setObjectName("yoneticikadi")
        self.yoneticisifre = QtWidgets.QLineEdit(Form)
        self.yoneticisifre.setGeometry(QtCore.QRect(30, 200, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.yoneticisifre.setFont(font)
        self.yoneticisifre.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.yoneticisifre.setObjectName("yoneticisifre")
        self.yoneticieposta = QtWidgets.QLineEdit(Form)
        self.yoneticieposta.setGeometry(QtCore.QRect(30, 240, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.yoneticieposta.setFont(font)
        self.yoneticieposta.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;")
        self.yoneticieposta.setObjectName("yoneticieposta")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(200, 100, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.secilen_ders = QtWidgets.QListView(Form)
        self.secilen_ders.setGeometry(QtCore.QRect(200, 140, 131, 131))
        self.secilen_ders.setObjectName("secilen_ders")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(100, 20, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(0, 255, 255);\n"
"color: rgb(179, 144, 255);\n"
"color: rgb(255, 217, 140);")
        self.label_8.setObjectName("label_8")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 290, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{color:white;background-color:rgb(82,84,99);\n"
"border:none;border-radius:20px}\n"
"QPushButton::hover{background-color:black;}\n"
"QPushButton::focus{background-color:green;}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(200, 80, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.retranslateUi(Form)
        self.comboBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.yoneticiAd.setPlaceholderText(_translate("Form", "Adınız.."))
        self.yoneticiSoyad.setPlaceholderText(_translate("Form", "Soyadınız.."))
        self.yoneticikadi.setPlaceholderText(_translate("Form", "Kullanıcı Adınız.."))
        self.yoneticisifre.setPlaceholderText(_translate("Form", "Şifreniz.."))
        self.yoneticieposta.setPlaceholderText(_translate("Form", "E-Postanız.."))
        self.comboBox.setItemText(0, _translate("Form", "Veri Yapıları"))
        self.comboBox.setItemText(1, _translate("Form", "Bitirme Ödevi"))
        self.comboBox.setItemText(2, _translate("Form", "Optimizasyon"))
        self.comboBox.setItemText(3, _translate("Form", "Sayısal Elektronik"))
        self.label_8.setText(_translate("Form", "Kayıt Ekranı"))
        self.pushButton_2.setText(_translate("Form", "Kayıt Ol"))
        self.label_9.setText(_translate("Form", "Ders Seçiniz:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form2()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
