from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt, QStringListModel
from PyQt5.QtGui import QImage, QPixmap
import mysql.connector
import face_recognition
import cv2
from ogrenci_ekle_python import Ui_Form
from ders_ekle import DersEklePage

class OgrenciEklePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ogrenciekleform = Ui_Form()
        self.ogrenciekleform.setupUi(self)
        self.ogrenciekleform.pushButton.clicked.connect(self.Kaydet)

        # Seçilen dersleri tutmak için bir küme oluştur
        self.secilen_dersler = set()
        
        # currentIndexChanged yerine activated sinyalini kullan
        self.ogrenciekleform.comboBox.activated.connect(self.ders_secildi)

        # Kamera değişkenleri
        self.camera = None
        self.timer = QTimer(self)
        
    def ders_ekle_arayuz_ac(self, ogrenci_No):
        self.ders_ekle_arayuz = DersEklePage(ogrenci_No, self.combobox_ogeleri_al())
        # Sinyali yuvaya bağlayın
        self.ders_ekle_arayuz.kameraDurumuDegisti.connect(self.kamera_durumunu_degistir)
        self.ders_ekle_arayuz.show()
        # Kamerayı durdurun
        self.kamera_durumunu_degistir(False)

    def kamera_durumunu_degistir(self, durum):
        if durum:
            self.kamerayi_baslat()
        else:
            self.kamerayi_durdur()

    def kamerayi_durdur(self):
        if self.camera is not None:
            self.timer.stop()
            self.camera.release()
            self.camera = None

    def ders_secildi(self):
        # Combobox'tan seçilen dersi al
        secilen_ders = self.ogrenciekleform.comboBox.currentText()

        # Eğer seçilen ders boşsa veya zaten eklenmişse bir şey yapma
        if not secilen_ders or secilen_ders in self.secilen_dersler:
            return

        # Eğer seçilen ders eklenmemişse, set'e ekle ve listView'e ekle
        self.secilen_dersler.add(secilen_ders)
        model = QStringListModel(list(self.secilen_dersler))
        self.ogrenciekleform.listView.setModel(model)

    def combobox_ogeleri_al(self):
        items = []
        for i in range(self.ogrenciekleform.comboBox.count()):
            items.append(self.ogrenciekleform.comboBox.itemText(i))
        return items
    
    def kamerayi_baslat(self):
        # Kamera değişkenlerini başlat
        self.camera = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.kamerayi_goster)
        self.timer.start(100)
    
    def kamerayi_goster(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                # Yüz tespiti için frame'i RGB'ye çevir
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                yuz_konumlari = face_recognition.face_locations(rgb_frame)

                # Tanınan her yüz için bir çerçeve çiz
                for ust, sag, alt, sol in yuz_konumlari:
                    cv2.rectangle(frame, (sol, ust), (sag, alt), (0, 255, 0), 2)

                # OpenCV'nin görüntüyü QPixmap'a dönüştürme işlemi
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = img.shape
                satir_basi = ch * w
                qt_formatina_cevir = QImage(img.data, w, h, satir_basi, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_formatina_cevir)

                # img_label boyutunu kamera görüntüsü boyutuna ayarla
                # Qt.KeepAspectRatio yerine Qt.IgnoreAspectRatio kullanarak görüntüyü img_label boyutlarına sığdır
                pixmap = pixmap.scaled(self.ogrenciekleform.img_label.width(), self.ogrenciekleform.img_label.height(), Qt.IgnoreAspectRatio)
                self.ogrenciekleform.img_label.setPixmap(pixmap)

    def Kaydet(self):
        # Öğrenci bilgilerini al
        ogrenci_ad = self.ogrenciekleform.lineEdit.text()
        ogrenci_soyad = self.ogrenciekleform.lineEdit_2.text()
        ogrenci_No = self.ogrenciekleform.lineEdit_3.text()
        success = False

        # Doğrulama kontrolleri
        if not ogrenci_ad.strip() or not ogrenci_soyad.strip():
            QMessageBox.warning(self, 'Hata', 'Boş kısımları doldurunuz.')
            return

        if len(ogrenci_No) != 10:
            QMessageBox.warning(self, 'Hata', 'Öğrenci No 10 haneli olmalıdır.')
            return

        # Veritabanı bağlantısı oluştur
        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()

            # Öğrenci numarası ile mevcut öğrenci kontrolü
            cursor.execute("SELECT * FROM Ogrenci WHERE OgrenciNo = %s", (ogrenci_No,))
            ogrenci = cursor.fetchone()

            if ogrenci:
                # Öğrenci mevcutsa, ders ekleme mesajı göster
                reply = QMessageBox.question(self, 'Öğrenci Mevcut', 'Bu numaraya ait bir öğrenci mevcut. Ders eklemek ister misiniz?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Ders ekleme işlemi için yeni bir arayüz oluştur ve öğrenci numarasını geçir
                    self.ders_ekle_arayuz = DersEklePage(ogrenci_No, self.combobox_ogeleri_al())
                    self.ders_ekle_arayuz.show()
                    self.ders_ekle_arayuz_ac(ogrenci_No)
                    return
            # Öğrenci mevcut değilse, kaydetme işlemini sürdür
            # Kameradan bir kare al ve yüz tespiti yap (kodun bu kısmı değişmeden kalıyor)
            ret, frame = self.camera.read()

            if not ret:
                QMessageBox.warning(self, 'Hata', 'Kamera bağlantısı yok.')
                return

            # Yüz tespiti
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yuz_konumlari = face_recognition.face_locations(rgb_frame)

            if len(yuz_konumlari) == 0:
                QMessageBox.warning(self, 'Hata', 'Yüz tespit edilemedi.')
                return

            # İlk yüzü seç
            ust, sag, alt, sol = yuz_konumlari[0]

            # Yüz bölgesini kırp
            kirpilmis_yuz = frame[ust:alt, sol:sag]

            # Yüz verisini al
            yuz_verisi = cv2.imencode('.jpg', kirpilmis_yuz)[1].tobytes()

            # Öğrenci bilgilerini ve yüz verisini veritabanına ekle
            cursor.execute("INSERT INTO Ogrenci (OgrenciAd, OgrenciSoyad, OgrenciNo, Ozellikler) VALUES (%s, %s, %s, %s)",
                        (ogrenci_ad, ogrenci_soyad, ogrenci_No, yuz_verisi))
            cursor.execute("SELECT LAST_INSERT_ID()")  # Son eklenen öğrenci ID'sini al
            ogrenci_id = cursor.fetchone()[0]

            # Seçilen dersleri veritabanına ekle
            for ders in self.secilen_dersler:
                cursor.execute("SELECT DersID FROM Ders WHERE DersAdi = %s", (ders,))
                ders_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO OgrenciDers (OgrenciNo, DersID) VALUES (%s, %s)", (ogrenci_No, ders_id))

            connection.commit()
            QMessageBox.information(self, 'Başarılı', 'Öğrenci ve dersleri başarıyla eklendi.')

            success = True

             # Öğrenci başarıyla eklendikten sonra formu temizle
            if success: # success, öğrenci ekleme işleminin başarılı olup olmadığını kontrol eden bir değişken
                self.temizle_form()


        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")

        finally:
            # Bağlantıyı kapat
            if connection.is_connected():
                cursor.close()
                connection.close()
    def temizle_form(self):
        # QLineEdit içeriklerini temizle
        self.ogrenciekleform.lineEdit.clear()
        self.ogrenciekleform.lineEdit_2.clear()
        self.ogrenciekleform.lineEdit_3.clear()

        # ListView içeriğini temizle
        self.secilen_dersler.clear()
        self.ogrenciekleform.listView.setModel(QStringListModel([]))

    def closeEvent(self, event):
        # Formu temizle
        self.temizle_form()

        # Kamerayı ve timer'ı kapat
        if self.camera is not None:
            self.timer.stop()
            self.camera.release()
            self.camera = None

        event.accept()


# Ana uygulama kısmı
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ogrenciEklePage = OgrenciEklePage()
    ogrenciEklePage.show()
    sys.exit(app.exec_())
