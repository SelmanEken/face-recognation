import mysql.connector
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QStringListModel 
from ders_ekle_python import Ui_Form6
from PyQt5.QtCore import pyqtSignal

class DersEklePage(QWidget):
    # Sinyali tanımlayın
    kameraDurumuDegisti = pyqtSignal(bool)

    def __init__(self, ogrenci_No=None, combobox_items=None):
        super().__init__()
        self.ogrenci_No = ogrenci_No
        self.combobox_items = combobox_items or []
        self.ders_ekle_form = Ui_Form6()
        self.ders_ekle_form.setupUi(self)
        self.ders_ekle_form.pushButton.clicked.connect(self.Kaydet)
        self.ders_ekle_form.comboBox.activated.connect(self.ders_secildi)
        self.dersleri_yukle()
        
        self.secilen_dersler = set()
        self.model = None

        self.ogrenci_bilgilerini_yukle()
        
    def closeEvent(self, event):
        # Pencere kapatıldığında sinyali tetikleyin
        self.kameraDurumuDegisti.emit(True)
        event.accept()
        
    def ogrenci_bilgilerini_yukle(self):
        ogrenci_no = self.ogrenci_No
        if ogrenci_no:
            try:
                connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT OgrenciAd, OgrenciSoyad, OgrenciNo FROM Ogrenci
                    WHERE OgrenciNo = %s
                """, (ogrenci_no,))
                ogrenci_bilgileri = cursor.fetchone()
                if ogrenci_bilgileri:
                    adi, soyadi, ogrenci_no = ogrenci_bilgileri
                    self.ders_ekle_form.lineEdit.setText(adi)
                    self.ders_ekle_form.lineEdit_2.setText(soyadi)
                    self.ders_ekle_form.lineEdit_3.setText(str(ogrenci_no))
                else:
                    QMessageBox.warning(self, 'Uyarı', 'Öğrenci bulunamadı.')
            except mysql.connector.Error as error:
                QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            QMessageBox.warning(self, 'Uyarı', 'Öğrenci numarası girilmemiş.')
    
    def ders_secildi(self):
        secilen_ders = self.ders_ekle_form.comboBox.currentText()
        if not secilen_ders or secilen_ders in self.secilen_dersler:
            return
        self.secilen_dersler.add(secilen_ders)
        self.model = QStringListModel(list(self.secilen_dersler))
        self.ders_ekle_form.listView.setModel(self.model) 

    def dersleri_yukle(self):
        self.ders_ekle_form.comboBox.clear()
        kayitli_dersler = self.ogrencinin_derslerini_getir()
        for item in self.combobox_items:
            if item not in kayitli_dersler:
                self.ders_ekle_form.comboBox.addItem(item)

    def ogrencinin_derslerini_getir(self):
        kayitli_dersler = []
        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Ders.DersAdi FROM OgrenciDers
                INNER JOIN Ders ON OgrenciDers.DersID = Ders.DersID
                WHERE OgrenciDers.OgrenciNo = %s
            """, (self.ogrenci_No,))
            kayitli_dersler = [ders[0] for ders in cursor.fetchall()]
        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return kayitli_dersler

    def DersEkle(self, ders_adi):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO OgrenciDers (OgrenciNo, DersID)
                VALUES (%s, (SELECT DersID FROM Ders WHERE DersAdi = %s))
            """, (self.ogrenci_No, ders_adi))
            connection.commit()
            self.secilen_dersler.add(ders_adi)
            return True
        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def Kaydet(self):
        # Önce öğrenci bilgilerini kontrol et
        yeni_adi = self.ders_ekle_form.lineEdit.text()
        yeni_soyadi = self.ders_ekle_form.lineEdit_2.text()
        yeni_numara = self.ders_ekle_form.lineEdit_3.text()

        if not yeni_adi or not yeni_soyadi or not yeni_numara:
            QMessageBox.warning(self, 'Uyarı', 'Öğrenci bilgileri eksik.')
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()

            # Öğrenci numarasının zaten kullanılıp kullanılmadığını kontrol et
            cursor.execute("SELECT * FROM Ogrenci WHERE OgrenciNo = %s", (yeni_numara,))
            if cursor.fetchone() and yeni_numara != self.ogrenci_No:
                QMessageBox.warning(self, 'Hata', 'Bu öğrenci numarası zaten kullanılıyor.')
                return

            # Dış anahtar kısıtlamalarını devre dışı bırak
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")

            # Eğer öğrenci bilgileri değiştirilmişse, güncelle
            cursor.execute("""
                UPDATE Ogrenci
                SET OgrenciAd = %s, OgrenciSoyad = %s, OgrenciNo = %s
                WHERE OgrenciNo = %s
            """, (yeni_adi, yeni_soyadi, yeni_numara, self.ogrenci_No))
            connection.commit()

            # Numara güncellendiyse, ders kayıtlarındaki numarayı güncelle
            if yeni_numara != self.ogrenci_No:
                cursor.execute("""
                    UPDATE OgrenciDers
                    SET OgrenciNo = %s
                    WHERE OgrenciNo = %s
                """, (yeni_numara, self.ogrenci_No))
                connection.commit()
                self.ogrenci_No = yeni_numara  # Öğrenci numarasını güncelle

            # Dış anahtar kısıtlamalarını tekrar etkinleştir
            cursor.execute("SET FOREIGN_KEY_CHECKS=1")

            # Dersleri ekleme işlemine devam et
            if self.secilen_dersler:
                for ders_adi in self.secilen_dersler:
                    if not self.DersEkle(ders_adi):
                        QMessageBox.warning(self, 'Hata', f"'{ders_adi}' dersi eklenemedi.")
                QMessageBox.information(self, 'Başarılı', 'Tüm dersler başarıyla eklendi.')
                self.secilen_dersler.clear()
                self.ders_ekle_form.listView.setModel(QStringListModel([]))
                self.dersleri_yukle()
            else:
                QMessageBox.warning(self, 'Uyarı', 'Listede ders bulunmamaktadır.')

        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DersEklePage()
    window.show()
    sys.exit(app.exec_())
