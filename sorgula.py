from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from sorgula_python import Ui_Form7
import sys
import mysql.connector

class SorgulaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form7()
        self.ui.setupUi(self)

        # Listele butonuna tıklandığında self.listele fonksiyonunu çağır
        self.ui.pushButton.clicked.connect(self.listele)

        # Veritabanı bağlantısını başlat
        self.db_baglanti_baslat()

    def db_baglanti_baslat(self):
        try:
            self.conn = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Veritabanı Bağlantı Hatası', f'Veritabanı bağlantısı başarısız: {err}')
            sys.exit(-1)

    def listele(self):
        # ComboBox ve DateEdit'ten değerleri al
        ders_adi = self.ui.comboBox.currentText()
        tarih = self.ui.dateEdit.date().toString("yyyy-MM-dd")

        # İlk olarak DersID'yi almak için Ders tablosunda sorgulama yap
        ders_id_query = "SELECT DersID FROM Ders WHERE DersAdi = %s"
        self.cursor.execute(ders_id_query, (ders_adi,))
        ders_id_result = self.cursor.fetchone()

        if ders_id_result:
            ders_id = ders_id_result[0]

            # Veritabanında sorgulama yap
            query = ("SELECT Ogrenci.OgrenciAd, Ogrenci.OgrenciSoyad, Ogrenci.OgrenciNo FROM OgrenciYoklama "
                    "INNER JOIN Ogrenci ON OgrenciYoklama.OgrenciNo = Ogrenci.OgrenciNo "
                    "WHERE OgrenciYoklama.DersID = %s AND OgrenciYoklama.Tarih = %s")
            self.cursor.execute(query, (ders_id, tarih))
            result = self.cursor.fetchall()

            # Tabloyu temizle
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            if not result:
                # Eğer sonuç boşsa, yoklama bilgisi olmadığını belirten bir mesaj göster
                QMessageBox.information(self, 'Yoklama Bilgisi', 'Seçilen tarih ve derse ait yoklama bilgisi bulunmamaktadır.')
            else:
                # Sütun sayısını ve başlıkları ayarla
                self.ui.tableWidget.setColumnCount(3)
                self.ui.tableWidget.setHorizontalHeaderLabels(["Öğrenci Adı", "Öğrenci Soyadı", "Öğrenci No"])

                # Veritabanından alınan verileri tabloya ekle
                for row, (ogrenci_ad, ogrenci_soyad, ogrenci_no) in enumerate(result):
                    self.ui.tableWidget.insertRow(row)
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(ogrenci_ad))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(ogrenci_soyad))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(ogrenci_no)))

    def closeEvent(self, event):
        # Uygulama kapatılırken veritabanı bağlantısını kapatma
        # self.cursor.close()
        # self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    # PyQt5 uygulamasını başlat
    app = QApplication(sys.argv)
    window = SorgulaPage()
    window.show()
    sys.exit(app.exec_())
