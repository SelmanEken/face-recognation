# kaydol.py dosyası

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel
from kaydol_ekran import Ui_Form2
import mysql.connector

class KaydolPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.kaydolform = Ui_Form2()
        self.kaydolform.setupUi(self)

        # Seçilen dersleri tutmak için bir küme oluştur
        self.secilen_dersler = set()

        # Combobox'ın değeri değiştiğinde tetiklenecek fonksiyonu bağla
        self.kaydolform.comboBox.currentIndexChanged.connect(self.ders_secildi)

        # Kayıt Ol butonuna tıklandığında tetiklenecek fonksiyonu bağla
        self.kaydolform.pushButton_2.clicked.connect(self.kayit_ol)

    def ders_secildi(self):
        # Combobox'tan seçilen dersi al
        secilen_ders = self.kaydolform.comboBox.currentText()

        # Eğer seçilen ders zaten eklenmişse hata mesajı ver
        if secilen_ders in self.secilen_dersler:
            QMessageBox.warning(self, "Hata", "Bu ders zaten eklenmiş.")
        else:
            # Eğer seçilen ders eklenmemişse, set'e ekle ve listView'e ekle
            self.secilen_dersler.add(secilen_ders)
            model = QStringListModel(self.secilen_dersler)
            self.kaydolform.secilen_ders.setModel(model)

    def temizle(self):
        # Tüm girdi alanlarını temizle
        self.kaydolform.yoneticiAd.clear()
        self.kaydolform.yoneticiSoyad.clear()
        self.kaydolform.yoneticikadi.clear()
        self.kaydolform.yoneticisifre.clear()
        self.kaydolform.yoneticieposta.clear()
        self.secilen_dersler.clear()
        model = QStringListModel(self.secilen_dersler)
        self.kaydolform.secilen_ders.setModel(model)

    def kayit_ol(self):
        yonetici_ad = self.kaydolform.yoneticiAd.text()
        yonetici_soyad = self.kaydolform.yoneticiSoyad.text()
        yonetici_kadi = self.kaydolform.yoneticikadi.text()
        yonetici_sifre = self.kaydolform.yoneticisifre.text()
        yonetici_eposta = self.kaydolform.yoneticieposta.text()
        yonetici_ders = list(self.secilen_dersler)

        veritabani = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Se563214',
            database='sface'
        )

        # Veritabanı üzerinde işlem yapacak bir cursor oluştur
        cursor = veritabani.cursor()

        try:
            # Öğrenci bilgilerini veritabanına ekle
            cursor.execute("INSERT INTO kullanici (KullaniciAd, KullaniciSoyad, KullaniciAdi, Parola, Eposta) VALUES (%s, %s, %s, %s, %s)",
                           (yonetici_ad, yonetici_soyad, yonetici_kadi, yonetici_sifre, yonetici_eposta))

            # Eklenen kullanıcının ID'sini al
            cursor.execute("SELECT KullaniciID FROM kullanici WHERE KullaniciAdi = %s", (yonetici_kadi,))
            kullanici_id = cursor.fetchone()[0]

            for ders in yonetici_ders:
                # Dersin veritabanında olup olmadığını kontrol et
                cursor.execute("SELECT DersID FROM ders WHERE DersAdi = %s", (ders,))
                result = cursor.fetchone()

                if result:
                    # Ders zaten varsa ders_id'yi al
                    ders_id = result[0]
                else:
                    # Ders yoksa dersi ekleyip ders_id'yi al
                    cursor.execute("INSERT INTO ders (DersAdi) VALUES (%s)", (ders,))
                    cursor.execute("SELECT DersID FROM ders WHERE DersAdi = %s", (ders,))
                    ders_id = cursor.fetchone()[0]

                # Kullanıcı-Ders ilişkisini kullaniciders tablosuna ekle
                cursor.execute("INSERT INTO kullaniciders (KullaniciID, DersID, KullaniciAdi) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE KullaniciID=KullaniciID", (kullanici_id, ders_id, yonetici_kadi))


            veritabani.commit()
            QMessageBox.information(self, 'Başarılı', 'Kullanıcı başarıyla eklendi.')

        except mysql.connector.Error as err:
            print("Hata:", err)
            veritabani.rollback()
            QMessageBox.warning(self, 'Hata', 'Kullanıcı eklenirken bir hata oluştu.')

        # Veritabanı bağlantısını kapat
        cursor.close()
        veritabani.close()

# Ana uygulama kısmı
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form2()
    ui.setupUi(Form)
    kaydol_page = KaydolPage()
    Form.show()

    sys.exit(app.exec_())
