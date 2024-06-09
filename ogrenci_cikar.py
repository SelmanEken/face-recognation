# ogrenci_cikar.py dosyası

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from ogrenci_cikar_python import Ui_Form4
import mysql.connector

class OgrenciCikarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form4()
        self.ui.setupUi(self)

        # MySQL bağlantısı
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Se563214",
            database="sface"
        )
        self.cursor = self.db.cursor()

        # Dersleri comboBox'a ekle
        self.dersleri_doldur()

        # PushButton'a tıklandığında çalışacak fonksiyonu bağla
        self.ui.pushButton.clicked.connect(self.listview_doldur)
        self.ui.pushButton_2.clicked.connect(self.ogrenciyi_dersten_cikar)

    def dersleri_doldur(self):
        query = "SELECT DersID, DersAdi FROM Ders"
        self.cursor.execute(query)
        dersler = self.cursor.fetchall()
        for ders_id, ders_adi in dersler:
            self.ui.comboBox.addItem(ders_adi, ders_id)

    def listview_doldur(self):
        # Seçilen dersin adını al
        ders_adi = self.ui.comboBox.currentText()
    
    
        # Seçilen dersin ID'sini bul
        query = "SELECT DersID FROM Ders WHERE DersAdi = %s"
        self.cursor.execute(query, (ders_adi,))
        sonuc = self.cursor.fetchone()
        if sonuc:
            course_id = sonuc[0]
        else:
            print("Ders bulunamadı.")
            return
    
        # Seçilen dersi alan öğrencileri çek
        query = """
        SELECT O.OgrenciNo, O.OgrenciAd, O.OgrenciSoyad
        FROM OgrenciDers OD
        JOIN Ogrenci O ON OD.OgrenciNo = O.OgrenciNo
        WHERE OD.DersID = %s
        """
        self.cursor.execute(query, (course_id,))
        ogrenciler = self.cursor.fetchall()

        # Tabloyu temizle
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)

        # Sütun sayısını ayarla
        self.ui.tableWidget.setColumnCount(3)

        # Başlıkları ayarla
        self.ui.tableWidget.setHorizontalHeaderLabels(["Öğrenci No", "Öğrenci Adı", "Öğrenci Soyadı"])

        # Öğrencileri tabloya ekle
        for ogrenci_no, ogrenci_ad, ogrenci_soyad in ogrenciler:
            satir_pozisyonu = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(satir_pozisyonu)
            self.ui.tableWidget.setItem(satir_pozisyonu, 0, QTableWidgetItem(str(ogrenci_no)))
            self.ui.tableWidget.setItem(satir_pozisyonu, 1, QTableWidgetItem(ogrenci_ad))
            self.ui.tableWidget.setItem(satir_pozisyonu, 2, QTableWidgetItem(ogrenci_soyad))

    def ogrenciyi_dersten_cikar(self):
        # Seçilen öğrenciyi belirlemek için seçilen satırı al
        secilen_satir = self.ui.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir öğrenci seçin.')
            return

        # Seçilen öğrencinin bilgilerini al
        ogrenci_no = self.ui.tableWidget.item(secilen_satir, 0).text()

        # Seçilen dersin adını al
        ders_adi = self.ui.comboBox.currentText()

        # Seçilen dersin ID'sini bul
        query = "SELECT DersID FROM Ders WHERE DersAdi = %s"
        self.cursor.execute(query, (ders_adi ,))
        sonuc = self.cursor.fetchone()
        if sonuc:
            ders_id = sonuc[0]
        else:
            print("Ders bulunamadı.")
            return

        # Kullanıcıyı uyar
        msg = f"{ogrenci_no} numaralı öğrenciyi {ders_adi} dersinden çıkarmak istediğinizden emin misiniz?"
        reply = QMessageBox.question(self, 'Öğrenci Dersinden Çıkar', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Öğrenciyi belirli dersten çıkar
                query = "DELETE FROM OgrenciDers WHERE OgrenciNo = %s AND DersID = %s"
                self.cursor.execute(query, (ogrenci_no, ders_id))

                self.db.commit()

                # Başarılı bir şekilde çıkarıldığına dair mesaj göster
                QMessageBox.information(self, 'Başarılı', 'Öğrenci başarıyla dersden çıkarıldı.')

                # Tabloyu yeniden doldur
                self.listview_doldur()
            except mysql.connector.Error as err:
                print("Hata:", err)
                QMessageBox.warning(self, 'Hata', 'Öğrenci dersden çıkarılırken bir hata oluştu.')

