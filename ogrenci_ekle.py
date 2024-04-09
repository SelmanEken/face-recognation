# ogrenci_ekle.py dosyası

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt, QStringListModel
from PyQt5.QtGui import QImage, QPixmap
import mysql.connector
import face_recognition
import cv2
from ogrenci_ekle_python import Ui_Form

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

    def start_camera(self):
        # Kamera değişkenlerini başlat
        self.camera = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.show_camera)
        self.timer.start(100)
    
    def show_camera(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                # Yüz tespiti için frame'i RGB'ye çevir
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)

                # Tanınan her yüz için bir çerçeve çiz
                for top, right, bottom, left in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # OpenCV'nin görüntüyü QPixmap'a dönüştürme işlemi
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = img.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(convert_to_qt_format)

                # img_label boyutunu kamera görüntüsü boyutuna ayarla
                # Qt.KeepAspectRatio yerine Qt.IgnoreAspectRatio kullanarak görüntüyü img_label boyutlarına sığdır
                pixmap = pixmap.scaled(self.ogrenciekleform.img_label.width(), self.ogrenciekleform.img_label.height(), Qt.IgnoreAspectRatio)
                self.ogrenciekleform.img_label.setPixmap(pixmap)

    def Kaydet(self):
        # Öğrenci bilgilerini al
        ogrenci_ad = self.ogrenciekleform.lineEdit.text()
        ogrenci_soyad = self.ogrenciekleform.lineEdit_2.text()
        ogrenci_No = self.ogrenciekleform.lineEdit_3.text()

        # Doğrulama kontrolleri
        if not ogrenci_ad.strip() or not ogrenci_soyad.strip():
            QMessageBox.warning(self, 'Hata', 'Boş kısımları doldurunuz.')
            return

        if len(ogrenci_No) != 10:
            QMessageBox.warning(self, 'Hata', 'Öğrenci No 10 haneli olmalıdır.')
            return

        # Kameradan bir kare al
        ret, frame = self.camera.read()

        if not ret:
            QMessageBox.warning(self, 'Hata', 'Kamera bağlantısı yok.')
            return

        # Yüz tespiti
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            QMessageBox.warning(self, 'Hata', 'Yüz tespit edilemedi.')
            return

        # İlk yüzü seç
        top, right, bottom, left = face_locations[0]

        # Yüz bölgesini kırp
        cropped_face = frame[top:bottom, left:right]

        # Yüz verisini al
        yuz_verisi = cv2.imencode('.jpg', cropped_face)[1].tobytes()

        # Veritabanı bağlantısı oluştur
        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="face")
            cursor = connection.cursor()

            # Öğrenci bilgilerini veritabanına ekle
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

        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Hata', f"Veritabanı hatası: {error}")

        finally:
            # Bağlantıyı kapat
            if connection.is_connected():
                cursor.close()
                connection.close()

    def closeEvent(self, event):
        # Kamerayı kapat
        if self.camera is not None:
            self.camera.release()
        event.accept()

 # Ana uygulama kısmı
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ogrenciEklePage = OgrenciEklePage()
    ogrenciEklePage.show()
    sys.exit(app.exec_())
