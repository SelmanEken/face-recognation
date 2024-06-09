import sys
from PyQt5.QtWidgets import *
from yonetici_python import Ui_Form2
from ogrenci_ekle import OgrenciEklePage
from PyQt5.QtCore import QStringListModel
from ogrenci_cikar import OgrenciCikarPage
from yoklama import YoklamaPage
from sorgula import SorgulaPage
import mysql.connector

class yoneticiPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.yoneticiform = Ui_Form2()
        self.yoneticiform.setupUi(self)
        self.ogrenciekleform = OgrenciEklePage()  # OgrenciEklePage sınıfının bir örneği oluşturuldu
        self.ogrencicikarform = OgrenciCikarPage()  # OgrenciCikarPage sınıfının bir örneği oluşturuldu
        self.yoklamaform = YoklamaPage() # Yoklama sınıfının bir örneği oluşturuldu
        self.sorgulaform = SorgulaPage() # sorgula sınıfının bir örneği
        self.yoneticiform.pushButton.clicked.connect(self.OgrenciEklemeFormu)
        self.yoneticiform.pushButton_2.clicked.connect(self.OgrenciCikarFormu)
        self.yoneticiform.pushButton_3.clicked.connect(self.SorgulaFormu)
        self.yoneticiform.pushButton_4.clicked.connect(self.YoklamaFormu)

    def OgrenciEklemeFormu(self):
        self.ogrenciekleform.kamerayi_baslat()
        self.ogrenciekleform.show()
        self.ogrenciekleform.secilen_dersler.clear()
        self.ogrenciekleform.ogrenciekleform.listView.setModel(QStringListModel([]))  # ListView içeriğini sıfırla

    def OgrenciCikarFormu(self):
        self.ogrencicikarform.show()    
    
    def YoklamaFormu(self):
        self.yoklamaform.show()   

    def SorgulaFormu(self):
        # Tabloyu temizle
        self.sorgulaform.ui.tableWidget.clearContents()
        self.sorgulaform.ui.tableWidget.setRowCount(0)
        self.sorgulaform.show()

    def KullaniciDersleriniYukle(self, kullanici_adi):
        try:
            veritabani = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Se563214',
                database='sface'
            )
            cursor = veritabani.cursor()
        
            # Kullanıcının derslerini sorgula
            cursor.execute("""
                SELECT d.DersID, d.DersAdi 
                FROM KullaniciDers kd 
                JOIN Ders d ON kd.DersID = d.DersID 
                WHERE kd.KullaniciAdi = %s
            """, (kullanici_adi,))
            dersler = cursor.fetchall()

            # OgrenciEklePage sınıfındaki QComboBox ve ListView'ı temizle
            self.ogrenciekleform.ogrenciekleform.comboBox.clear()
            self.ogrenciekleform.secilen_dersler.clear()

            # QComboBox'a sadece giriş yapan kullanıcının derslerini ekle
            for ders_id, ders_adi in dersler:
                self.ogrenciekleform.ogrenciekleform.comboBox.addItem(ders_adi, ders_id)

            # OgrenciCikarPage sınıfındaki QComboBox'u temizle ve sadece giriş yapan kullanıcının derslerini ekle
            self.ogrencicikarform.ui.comboBox.clear()
            for ders_id, ders_adi in dersler:
                self.ogrencicikarform.ui.comboBox.addItem(ders_adi, ders_id)

            # YoklamaPage sınıfındaki QComboBox'u temizle ve sadece giriş yapan kullanıcının derslerini ekle
            self.yoklamaform.ui.comboBox.clear()
            for ders_id, ders_adi in dersler:
                self.yoklamaform.ui.comboBox.addItem(ders_adi, ders_id)

            # SorguPage sınıfındaki QComboBox'u temizle ve sadece giriş yapan kullanıcının derslerini ekle
            self.sorgulaform.ui.comboBox.clear()
            for ders_id, ders_adi in dersler:
                self.sorgulaform.ui.comboBox.addItem(ders_adi, ders_id)

        except mysql.connector.Error as err:
            print("Hata:", err)
            QMessageBox.warning(self, 'Hata', 'Veritabanı hatası')
        finally:
            try:
                if veritabani.is_connected():
                    cursor.close()
                    veritabani.close()
            except UnboundLocalError:
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yoneticiPage = yoneticiPage()
    yoneticiPage.show()
    sys.exit(app.exec_())
