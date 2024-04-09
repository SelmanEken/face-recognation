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

class YoklamaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form5()
        self.ui.setupUi(self)
        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_camera)
        self.ui.pushButton.clicked.connect(self.start_camera)
        self.ui.pushButton_2.clicked.connect(self.export_to_excel)
        self.student_face_encodings = {}
        self.student_face_names = {}
        self.recognized_students = set()
        self.selected_course = None

        self.ui.comboBox.activated.connect(self.handle_course_selection)

    def handle_course_selection(self):
        self.selected_course = self.ui.comboBox.currentText()

    def load_students_for_selected_course(self):
        if not self.selected_course:
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", passwd="Se563214", database="face")
            cursor = connection.cursor()
            cursor.execute("""
                SELECT o.OgrenciNo, o.OgrenciAd, o.OgrenciSoyad, o.Ozellikler
                FROM Ogrenci o
                JOIN OgrenciDers od ON o.OgrenciNo = od.OgrenciNo
                JOIN Ders d ON od.DersID = d.DersID
                WHERE d.DersAdi = %s
            """, (self.selected_course,))
            students = cursor.fetchall()

            self.student_face_encodings.clear()
            self.student_face_names.clear()
            self.recognized_students.clear()
            self.ui.listWidget.clear()

            for student in students:
                ogrenci_no, ogrenci_ad, ogrenci_soyad, yuz_verisi_blob = student
                nparr = np.frombuffer(yuz_verisi_blob, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                face_encodings = face_recognition.face_encodings(img)
                if face_encodings:
                    face_encoding = face_encodings[0]
                    self.student_face_encodings[ogrenci_no] = face_encoding
                    self.student_face_names[ogrenci_no] = f"{ogrenci_ad} {ogrenci_soyad}"
                else:
                    print(f"Öğrenci {ogrenci_no} için yüz verisi bulunamadı.")

        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Veritabanı Hatası', f"Veritabanı hatası: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def start_camera(self):
        if not self.selected_course:
            QMessageBox.warning(self, 'Ders Seçilmemiş', 'Lütfen bir ders seçin.')
            return

        self.load_students_for_selected_course()
        self.camera = cv2.VideoCapture(0)
        self.timer.start(100)

    def stop_camera(self):
        if self.camera is not None and self.camera.isOpened():
            self.timer.stop()
            self.camera.release()
            self.camera = None
            self.ui.img_label.clear()  # Kamera görüntüsünü temizle

    def show_camera(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(list(self.student_face_encodings.values()), face_encoding)
                name = "Tanimlanamayan Yuz"

                if matches:
                    face_distances = face_recognition.face_distance(list(self.student_face_encodings.values()), face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        student_no = list(self.student_face_encodings.keys())[best_match_index]
                        if student_no in self.student_face_names:
                            name = self.student_face_names[student_no]
                            if student_no not in self.recognized_students:
                                self.ui.listWidget.addItem(QListWidgetItem(name))
                                self.recognized_students.add(student_no)
                        else:
                            continue

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), 2)

            self.display_image(frame)

    def display_image(self, image):
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        img = img.rgbSwapped()
        self.ui.img_label.setPixmap(QPixmap.fromImage(img))
        self.ui.img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def closeEvent(self, event):
        if self.camera is not None:
            self.camera.release()
        event.accept()

    def export_to_excel(self):

        self.stop_camera()
        #ders seçilmemişse
        if not self.selected_course:
            QMessageBox.warning(self, 'Ders Seçilmemiş', 'Lütfen bir ders seçin.')
            return
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Excel Dosyası Kaydet", "", "Excel Dosyaları (*.xls)", options=options)
        if not filename:
            return

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        worksheet.write('A1', 'Öğrenci No', header_format)
        worksheet.write('B1', 'Öğrenci Adı', header_format)

        row = 1
        col = 0

        for student_no in self.recognized_students:
            student_name = self.student_face_names[student_no]
            worksheet.write(row, col, student_no)
            worksheet.write(row, col + 1, student_name)
            row += 1

        workbook.close()
        QMessageBox.information(self, 'Dışa Aktarma Başarılı', f'{filename} dosyasına başarıyla dışa aktarıldı.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yoklamaPage = YoklamaPage()
    yoklamaPage.show()
    sys.exit(app.exec_())
