from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QListWidgetItem, QFileDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys
import face_recognition
import numpy as np
import mysql.connector
import xlsxwriter
from yoklama_python import Ui_Form5
from datetime import datetime

class YoklamaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form5()
        self.ui.setupUi(self)
        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.kamera_goster)
        self.ui.pushButton.clicked.connect(self.kamerayi_baslat)
        self.ui.pushButton_2.clicked.connect(self.excele_aktar)
        self.ogrenci_yuz_ozellikleri = {}
        self.ogrenci_isimleri = {}
        self.tanimlanan_ogrenciler = set()
        self.secilen_ders = None

        self.ui.comboBox.activated.connect(self.ders_secimi_yap)

    def ders_secimi_yap(self):
        self.secilen_ders = self.ui.comboBox.currentText()
        index = self.ui.comboBox.currentIndex()
        self.secilen_ders_id = self.ui.comboBox.itemData(index)  # seçilen ders id'sini sınıfın bir özelliği olarak sakla


    def secilen_ders_icin_ogrencileri_yukle(self):
        if not self.secilen_ders:
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()
            cursor.execute("""
                SELECT o.OgrenciNo, o.OgrenciAd, o.OgrenciSoyad, o.Ozellikler
                FROM Ogrenci o
                JOIN OgrenciDers od ON o.OgrenciNo = od.OgrenciNo
                JOIN Ders d ON od.DersID = d.DersID
                WHERE d.DersAdi = %s
            """, (self.secilen_ders,))
            ogrenciler = cursor.fetchall()

            self.ogrenci_yuz_ozellikleri.clear()
            self.ogrenci_isimleri.clear()
            self.tanimlanan_ogrenciler.clear()
            self.ui.listWidget.clear()

            for ogrenci in ogrenciler:
                ogrenci_no, ogrenci_ad, ogrenci_soyad, yuz_verisi_blob = ogrenci
                nparr = np.frombuffer(yuz_verisi_blob, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                yuz_ozellikleri = face_recognition.face_encodings(img)
                if yuz_ozellikleri:
                    yuz_ozelligi = yuz_ozellikleri[0]
                    self.ogrenci_yuz_ozellikleri[ogrenci_no] = yuz_ozelligi
                    self.ogrenci_isimleri[ogrenci_no] = f"{ogrenci_ad} {ogrenci_soyad}"
                else:
                    print(f"Öğrenci {ogrenci_no} için yüz verisi bulunamadı.")
        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Veritabanı Hatası', f"Veritabanı hatası: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def kamerayi_baslat(self):
        if not self.secilen_ders:
            QMessageBox.warning(self, 'Ders Seçilmemiş', 'Lütfen bir ders seçin.')
            return

        self.secilen_ders_icin_ogrencileri_yukle()
        self.camera = cv2.VideoCapture(0)
        self.timer.start(100)

    def kamerayi_durdur(self):
        if self.camera is not None and self.camera.isOpened():
            self.timer.stop()
            self.camera.release()
            self.camera = None
            self.ui.img_label.clear()  # Kamera görüntüsünü temizle

    def kamera_goster(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yuz_konumlari = face_recognition.face_locations(rgb_frame)
            yuz_ozellikleri = face_recognition.face_encodings(rgb_frame, yuz_konumlari)

            for (ust, sag, alt, sol), yuz_ozelligi in zip(yuz_konumlari, yuz_ozellikleri):
                eslesmeler = face_recognition.compare_faces(list(self.ogrenci_yuz_ozellikleri.values()), yuz_ozelligi)
                isim = "Tanımlanamayan Yüz"

                if eslesmeler:
                    yuz_mesafeleri = face_recognition.face_distance(list(self.ogrenci_yuz_ozellikleri.values()), yuz_ozelligi)
                    en_iyi_eslesme_index = np.argmin(yuz_mesafeleri)
                    if eslesmeler[en_iyi_eslesme_index]:
                        ogrenci_no = list(self.ogrenci_yuz_ozellikleri.keys())[en_iyi_eslesme_index]
                        if ogrenci_no in self.ogrenci_isimleri:
                            isim = self.ogrenci_isimleri[ogrenci_no]
                            if ogrenci_no not in self.tanimlanan_ogrenciler:
                                self.ui.listWidget.addItem(QListWidgetItem(isim))
                                self.tanimlanan_ogrenciler.add(ogrenci_no)
                        else:
                            continue

                cv2.rectangle(frame, (sol, ust), (sag, alt), (0, 255, 0), 2)
                cv2.putText(frame, isim, (sol, alt + 20), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), 2)

            self.goruntuyu_goster(frame)

    def goruntuyu_goster(self, goruntu):
        qformat = QImage.Format_Indexed8
        if len(goruntu.shape) == 3:
            if goruntu.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(goruntu, goruntu.shape[1], goruntu.shape[0], goruntu.strides[0], qformat)
        img = img.rgbSwapped()
        self.ui.img_label.setPixmap(QPixmap.fromImage(img))
        self.ui.img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def closeEvent(self, event):
        if self.camera is not None:
            self.camera.release()
        event.accept()

    def excele_aktar(self):

        tarih = datetime.now().date()
        self.kamerayi_durdur()
        #ders seçilmemişse
        if not self.secilen_ders_id:
            QMessageBox.warning(self, 'Ders Seçilmemiş', 'Lütfen bir ders seçin.')
            return
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Excel Dosyası Kaydet", "", "Excel Dosyaları (*.xls)", options=options)
        # Kullanıcı dosya adı seçmediyse veya iptal ettiyse, işlemi durdur
        if not filename:
            QMessageBox.warning(self, 'Dosya Seçilmedi', 'Excel dosyası kaydetmek için bir dosya adı seçilmedi.')
            return  # Fonksiyondan çık ve işlemi durdur

        # Eğer dosya adı '.xls' ile bitmiyorsa, sonuna ekle
        if not filename.endswith('.xls'):
            filename += '.xls'
            
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        baslik_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        worksheet.write('A1', 'Öğrenci No', baslik_format)
        worksheet.write('B1', 'Öğrenci Adı', baslik_format)
        worksheet.write('C1', 'Tarih', baslik_format)

        satir = 1
        sutun = 0

        # Öğrenci bilgilerini ve tarih bilgisini yazdırma
        for ogrenci_no in self.tanimlanan_ogrenciler:
            ogrenci_adi = self.ogrenci_isimleri[ogrenci_no]
            worksheet.write(satir, sutun, ogrenci_no)
            worksheet.write(satir, sutun + 1, ogrenci_adi)
            worksheet.write(satir, sutun + 2, str(tarih))  # Tarih bilgisini yazdır
            satir += 1

        workbook.close()
        QMessageBox.information(self, 'Dışa Aktarma Başarılı', f'{filename} dosyasına başarıyla kaydedildi.')
        # Excel'e dışa aktarma işlemi tamamlandıktan sonra veritabanına kayıt ekleme
        self.yoklama_kayitlarini_ekle()

    def yoklama_kayitlarini_ekle(self):
        tarih = datetime.now().date()
        if not self.secilen_ders_id:
            print("Ders ID'si seçilmedi.")
            return


        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="sface")
            cursor = connection.cursor()
            for ogrenci_no in self.tanimlanan_ogrenciler:
                # Yoklama kaydını veritabanına ekle
                cursor.execute("""
                    INSERT INTO OgrenciYoklama (DersID, OgrenciNo, Tarih)
                    VALUES (%s, %s, %s)
                """, (self.secilen_ders_id, ogrenci_no, tarih))
            connection.commit()
            print("Yoklama kayıtları başarıyla eklendi.")
            self.ui.listWidget.clear()
        except mysql.connector.Error as error:
            print(f"Veritabanı hatası: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    yoklamaPage = YoklamaPage()
    yoklamaPage.show()
    sys.exit(app.exec_())
