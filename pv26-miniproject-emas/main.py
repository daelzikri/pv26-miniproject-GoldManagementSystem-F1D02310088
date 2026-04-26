import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import database as db #import agar bisa dipanggil di main
from views.main_window import MainWindow #import agar bisa dipanggil di main

def load_stylesheet(app: QApplication):#agar bisa dipisah untuk style nya ke style.qss semua
    qss_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss") #agar style.qss dapat diterapkan pada keseluruhan program
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"[WARNING] File style.qss tidak ditemukan di: {qss_path}")


def main():
    db.init_db() #panggil fungsi tersebut agar memulai terhubung ke database dan jalankan query di fungsi jika belum

    app = QApplication(sys.argv) #menginisialisasi sistem (paling penting)
    app.setApplicationName("Gold-MS")
    app.setOrganizationName("Toko Emas")

    load_stylesheet(app) #jalankan fungsinya

    window = MainWindow()
    window.show()#mulai menampilkan tampilannya

    sys.exit(app.exec())


if __name__ == "__main__":
    main()#jalankan fungsi main yang didalamnya berisi program untuk menjalankan bagian lainnya
