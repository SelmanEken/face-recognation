#login dosyası
from PyQt5.QtWidgets import *
from login_python import Ui_Form
from yonetici import yoneticiPage
from PyQt5.QtCore import Qt
from kaydol import KaydolPage
import mysql.connector

class LoginPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.loginform = Ui_Form()
        self.loginform.setupUi(self)
        self.yoneticiac = yoneticiPage()
        self.loginform.pushButton.clicked.connect(self.GirisYap)
        self.kaydolac = KaydolPage()
        self.loginform.pushButton_2.clicked.connect(self.KaydolButon)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:  # Enter tuşu için kontrol
            self.GirisYap()  # Giriş yapma fonksiyonunu çağır
        else:
            super().keyPressEvent(event)  # Diğer tuş basımları için varsayılan işlemi yap
    
    def KaydolButon(self):
        self.kaydolac.temizle()  # Arayüz yeniden açıldığında girilen bilgileri temizle
        self.kaydolac.show()

    def GirisYap(self):
        kadi = self.loginform.lineEdit_kullaniciadi.text().strip()  # strip() ile baştaki ve sondaki boşlukları temizle
        sifre = self.loginform.lineEdit_sifre.text().strip()

        # Kullanıcı adı veya şifre boşsa hata mesajı göster
        if not kadi or not sifre:
            QMessageBox.warning(self, 'Hatalı Giriş', 'Kullanıcı adı ve şifre boş bırakılamaz!')
            return  # Fonksiyondan çık

        try:
            veritabani = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Se563214',
                database='sface'
            )
            cursor = veritabani.cursor()
            # Kullanıcı bilgilerini veritabanından kontrol et
            cursor.execute("SELECT * FROM Kullanici WHERE KullaniciAdi = %s AND Parola = %s", (kadi, sifre))
            kullanici = cursor.fetchone()

            if kullanici:
                # Giriş başarılı ise giriş yap
                self.hide()
                self.yoneticiac.KullaniciDersleriniYukle(kadi)  # Kullanıcı adını kullanarak dersleri yükle
                self.yoneticiac.show()
            else:
                # Giriş başarısız ise hata mesajı göster
                QMessageBox.warning(self, 'Hatalı Giriş', 'Kullanıcı adı veya şifre yanlış!')

        except mysql.connector.Error as err:
            print("Hata:", err)
            QMessageBox.warning(self, 'Hata', 'Veritabanı hatası')

        finally:
            # Veritabanı bağlantısını kapat
            if 'cursor' in locals():
                cursor.close()
            if 'veritabani' in locals() and veritabani.is_connected():
                veritabani.close()