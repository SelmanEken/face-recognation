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
            database="face"
        )
        self.cursor = self.db.cursor()

        # Dersleri comboBox'a ekle
        self.populate_courses()

        # PushButton'a tıklandığında çalışacak fonksiyonu bağla
        self.ui.pushButton.clicked.connect(self.populate_listview)
        self.ui.pushButton_2.clicked.connect(self.remove_student_from_course)

    def populate_courses(self):
        query = "SELECT DersID, DersAdi FROM Ders"
        self.cursor.execute(query)
        courses = self.cursor.fetchall()
        for course_id, course_name in courses:
            self.ui.comboBox.addItem(course_name, course_id)

    def populate_listview(self):
        # Seçilen dersin adını al
        course_name = self.ui.comboBox.currentText()
    
        # Seçilen dersin ID'sini bul
        query = "SELECT DersID FROM Ders WHERE DersAdi = %s"
        self.cursor.execute(query, (course_name,))
        result = self.cursor.fetchone()
        if result:
            course_id = result[0]
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
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(ogrenci_no)))
            self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(ogrenci_ad))
            self.ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(ogrenci_soyad))

    def remove_student_from_course(self):
        # Seçilen öğrenciyi belirlemek için seçilen satırı al
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir öğrenci seçin.')
            return

        # Seçilen öğrencinin bilgilerini al
        ogrenci_no = self.ui.tableWidget.item(selected_row, 0).text()

        # Seçilen dersin adını al
        course_name = self.ui.comboBox.currentText()

        # Seçilen dersin ID'sini bul
        query = "SELECT DersID FROM Ders WHERE DersAdi = %s"
        self.cursor.execute(query, (course_name,))
        result = self.cursor.fetchone()
        if result:
            course_id = result[0]
        else:
            print("Ders bulunamadı.")
            return

        # Kullanıcıyı uyar
        msg = f"{ogrenci_no} numaralı öğrenciyi {course_name} dersinden çıkarmak istediğinizden emin misiniz?"
        reply = QMessageBox.question(self, 'Öğrenci Dersinden Çıkar', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Öğrenciyi belirli dersten çıkar
                query = "DELETE FROM OgrenciDers WHERE OgrenciNo = %s AND DersID = %s"
                self.cursor.execute(query, (ogrenci_no, course_id))

                self.db.commit()

                # Başarılı bir şekilde çıkarıldığına dair mesaj göster
                QMessageBox.information(self, 'Başarılı', 'Öğrenci başarıyla dersden çıkarıldı.')

                # Tabloyu yeniden doldur
                self.populate_listview()
            except mysql.connector.Error as err:
                print("Hata:", err)
                QMessageBox.warning(self, 'Hata', 'Öğrenci dersden çıkarılırken bir hata oluştu.')

