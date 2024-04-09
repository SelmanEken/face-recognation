# yonetici.py dosyası

import sys
from PyQt5.QtWidgets import *
from yonetici_python import Ui_Form2
from ogrenci_ekle import OgrenciEklePage
from PyQt5.QtCore import QStringListModel
from ogrenci_cikar import OgrenciCikarPage
from yoklama import YoklamaPage
import mysql.connector

class yoneticiPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.yoneticiform = Ui_Form2()
        self.yoneticiform.setupUi(self)
        self.ogrenciekleform = OgrenciEklePage()  # OgrenciEklePage sınıfının bir örneği oluşturuldu
        self.ogrencicikarform = OgrenciCikarPage()  # OgrenciCikarPage sınıfının bir örneği oluşturuldu
        self.yoklamaform = YoklamaPage() # Yoklama sınıfının bir örneği oluşturuldu
        self.yoneticiform.pushButton.clicked.connect(self.OgrenciEklemeFormu)
        self.yoneticiform.pushButton_2.clicked.connect(self.OgrenciCikarFormu)
        self.yoneticiform.pushButton_4.clicked.connect(self.YoklamaFormu)

    def OgrenciEklemeFormu(self):
        self.ogrenciekleform.start_camera()
        self.ogrenciekleform.show()
        self.ogrenciekleform.secilen_dersler.clear()
        self.ogrenciekleform.ogrenciekleform.listView.setModel(QStringListModel([]))  # ListView içeriğini sıfırla

    def OgrenciCikarFormu(self):
        self.ogrencicikarform.show()    
    
    def YoklamaFormu(self):
        self.yoklamaform.show()   

    def KullaniciDersleriniYukle(self, kullanici_adi):
        try:
            veritabani = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Se563214',
                database='face'
            )
            cursor = veritabani.cursor()
        
            # Kullanıcının derslerini sorgula
            cursor.execute("""
                SELECT d.DersAdi 
                FROM KullaniciDers kd 
                JOIN Ders d ON kd.DersID = d.DersID 
                WHERE kd.KullaniciAdi = %s
            """, (kullanici_adi,))
            dersler = cursor.fetchall()

            # OgrenciEklePage sınıfındaki QComboBox ve ListView'ı temizle
            self.ogrenciekleform.ogrenciekleform.comboBox.clear()
            self.ogrenciekleform.secilen_dersler.clear()

            # QComboBox'a sadece giriş yapan kullanıcının derslerini ekle
            for ders in dersler:
                self.ogrenciekleform.ogrenciekleform.comboBox.addItem(ders[0])

            # OgrenciCikarPage sınıfındaki QComboBox'u temizle ve sadece giriş yapan kullanıcının derslerini ekle
            self.ogrencicikarform.ui.comboBox.clear()
            for ders in dersler:
                self.ogrencicikarform.ui.comboBox.addItem(ders[0])

            # YoklamaPage sınıfındaki QComboBox'u temizle ve sadece giriş yapan kullanıcının derslerini ekle
            self.yoklamaform.ui.comboBox.clear()
            for ders in dersler:
                self.yoklamaform.ui.comboBox.addItem(ders[0])
        
            # OgrenciEklePage sınıfındaki ListView'ı temizle
            self.ogrenciekleform.secilen_dersler.clear()
            self.ogrenciekleform.ogrenciekleform.listView.setModel(QStringListModel([]))  # ListView içeriğini sıfırla

        except mysql.connector.Error as err:
            print("Hata:", err)
            QMessageBox.warning(self, 'Hata', 'Veritabanı hatası')
        finally:
            cursor.close()
            veritabani.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yoneticiPage = yoneticiPage()
    yoneticiPage.show()
    sys.exit(app.exec_())
