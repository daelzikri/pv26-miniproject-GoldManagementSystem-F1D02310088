import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QFrame,
    QStatusBar, QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

import controllers as ctrl
from views.dialogs import InventarisDialog, TransaksiDialog, OperasionalDialog

#MENJALANKAN TAMPILAN UTAMA KE USER


class MainWindow(QMainWindow):#Membuat tampilan utama windownya
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gold-MS — Gold Management System")
        self.setMinimumSize(1050, 680)
        self._build_ui()
        self._build_menu()
        self._build_statusbar()
        self._refresh_semua()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh_dashboard)
        self.timer.start(30_000)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        root.addWidget(self._buat_header())

        root.addWidget(self._buat_dashboard())

        garis = QFrame()
        garis.setFrameShape(QFrame.HLine)
        root.addWidget(garis)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        self._buat_tab_transaksi()
        self._buat_tab_inventaris()
        self._buat_tab_operasional()

    def _buat_header(self) -> QWidget:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 4, 8, 4)

        kiri = QVBoxLayout()
        lbl_judul = QLabel("Gold-MS")
        lbl_judul.setObjectName("title_label")
        lbl_sub = QLabel("Gold Management System — Toko Perhiasan")
        lbl_sub.setObjectName("subtitle_label")
        kiri.addWidget(lbl_judul)
        kiri.addWidget(lbl_sub)

        kanan = QVBoxLayout()
        kanan.setAlignment(Qt.AlignRight)
        lbl_petugas = QLabel(f"{ctrl.NAMA}")
        lbl_petugas.setObjectName("petugas_label")
        lbl_nim = QLabel(f"NIM: {ctrl.NIM}")
        lbl_nim.setObjectName("petugas_label")
        lbl_nim.setAlignment(Qt.AlignRight)
        kanan.addWidget(lbl_petugas)
        kanan.addWidget(lbl_nim)

        layout.addLayout(kiri, 1)
        layout.addLayout(kanan)
        return frame

    def _buat_dashboard(self) -> QWidget:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        self.card_omzet     = self._buat_kartu("Omzet Penjualan", "Rp 0", "card_value_green")
        self.card_buyback   = self._buat_kartu("Total Buyback", "Rp 0", "card_value_red")
        self.card_keluar    = self._buat_kartu("Pengeluaran", "Rp 0", "card_value_red")
        self.card_saldo     = self._buat_kartu("Saldo Kas Hari Ini", "Rp 0", "card_value")
        self.card_stok      = self._buat_kartu("Stok Tersedia", "0 item", "card_value_blue")

        layout.addWidget(self.card_omzet)
        layout.addWidget(self.card_buyback)
        layout.addWidget(self.card_keluar)
        layout.addWidget(self.card_saldo)
        layout.addWidget(self.card_stok)
        return frame

    def _buat_kartu(self, judul, nilai, style_value) -> QFrame:
        card = QFrame()
        card.setObjectName("dashboard_card")
        vl = QVBoxLayout(card)
        vl.setSpacing(4)
        vl.setAlignment(Qt.AlignCenter)

        lbl_judul = QLabel(judul)
        lbl_judul.setObjectName("card_title")
        lbl_judul.setAlignment(Qt.AlignCenter)

        lbl_nilai = QLabel(nilai)
        lbl_nilai.setObjectName(style_value)
        lbl_nilai.setAlignment(Qt.AlignCenter)

        vl.addWidget(lbl_judul)
        vl.addWidget(lbl_nilai)

        card._lbl_nilai = lbl_nilai
        return card

    def _buat_tab_transaksi(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        lbl = QLabel("Riwayat Transaksi (Penjualan & Buyback)")
        lbl.setObjectName("subtitle_label")

        btn_tambah = QPushButton("Catat Transaksi Baru")
        btn_tambah.clicked.connect(self._on_tambah_transaksi)

        btn_hapus = QPushButton("Hapus")
        btn_hapus.setObjectName("btn_danger")
        btn_hapus.clicked.connect(self._on_hapus_transaksi)

        toolbar.addWidget(lbl, 1)
        toolbar.addWidget(btn_tambah)
        toolbar.addWidget(btn_hapus)
        layout.addLayout(toolbar)

        self.tabel_transaksi = self._buat_tabel([
            "ID", "Tanggal", "Jenis", "Nama Barang", "Kategori",
            "Berat (g)", "Harga/g (Rp)", "Total (Rp)", "Keterangan"
        ])
        layout.addWidget(self.tabel_transaksi)

        self.tabs.addTab(widget, "Transaksi")

    def _buat_tab_inventaris(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        lbl = QLabel("Daftar Inventaris Barang")
        lbl.setObjectName("subtitle_label")

        btn_tambah = QPushButton("Tambah Barang")
        btn_tambah.clicked.connect(self._on_tambah_inventaris)

        btn_edit = QPushButton("Edit")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.clicked.connect(self._on_edit_inventaris)

        btn_hapus = QPushButton("Hapus")
        btn_hapus.setObjectName("btn_danger")
        btn_hapus.clicked.connect(self._on_hapus_inventaris)

        toolbar.addWidget(lbl, 1)
        toolbar.addWidget(btn_tambah)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_hapus)
        layout.addLayout(toolbar)

        self.tabel_inventaris = self._buat_tabel([
            "ID", "Kode", "Nama Barang", "Kategori",
            "Kadar", "Berat (g)", "Lokasi", "Status", "Tgl Input"
        ])
        layout.addWidget(self.tabel_inventaris)

        self.tabs.addTab(widget, "Inventaris")

    def _buat_tab_operasional(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        # Toolbar
        toolbar = QHBoxLayout()
        lbl = QLabel("Data Operasional Toko")
        lbl.setObjectName("subtitle_label")

        btn_tambah = QPushButton("Catat Operasional")
        btn_tambah.clicked.connect(self._on_tambah_operasional)

        btn_hapus = QPushButton("Hapus")
        btn_hapus.setObjectName("btn_danger")
        btn_hapus.clicked.connect(self._on_hapus_operasional)

        toolbar.addWidget(lbl, 1)
        toolbar.addWidget(btn_tambah)
        toolbar.addWidget(btn_hapus)
        layout.addLayout(toolbar)

        self.tabel_operasional = self._buat_tabel([
            "ID", "Tanggal", "Tipe", "Deskripsi", "Nominal (Rp)", "Keterangan"
        ])
        layout.addWidget(self.tabel_operasional)

        self.tabs.addTab(widget, "Operasional")

    def _buat_tabel(self, kolom: list) -> QTableWidget:
        tabel = QTableWidget()
        tabel.setColumnCount(len(kolom))
        tabel.setHorizontalHeaderLabels(kolom)
        tabel.setAlternatingRowColors(True)
        tabel.setEditTriggers(QTableWidget.NoEditTriggers)
        tabel.setSelectionBehavior(QTableWidget.SelectRows)
        tabel.verticalHeader().setVisible(False)
        tabel.horizontalHeader().setStretchLastSection(True)
        tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        return tabel

    def _build_menu(self):
        menubar = self.menuBar()

        menu_app = menubar.addMenu("Aplikasi")
        act_keluar = QAction("Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_app.addAction(act_keluar)

        act_tentang = QAction("Tentang", self)
        act_tentang.triggered.connect(self._tampil_tentang)
        menubar.addAction(act_tentang)

    def _tampil_tentang(self):
        QMessageBox.information(
            self, "Tentang Aplikasi",
            "<h2>Gold-MS</h2>"
            "<p><b>Gold Management System</b></p>"
            "<p>Aplikasi manajemen data penjualan, buyback, inventaris, dan operasional "
            "toko perhiasan emas berbasis PySide6.</p>"
            "<hr>"
            f"<p>Nama: {ctrl.NAMA}</p>"
            f"<p>NIM: {ctrl.NIM}</p>"
            "<p>Tugas Mini Project — Pemrograman Visual (PySide6)</p>"
        )

    def _build_statusbar(self):
        self.statusBar().showMessage(
            f"Gold-MS  |  Petugas: {ctrl.NAMA}  |  NIM: {ctrl.NIM}"
        )

    def _refresh_semua(self):
        self._refresh_dashboard()
        self._refresh_transaksi()
        self._refresh_inventaris()
        self._refresh_operasional()

    def _refresh_dashboard(self):
        data = ctrl.ambil_data_dashboard()
        self.card_omzet._lbl_nilai.setText(f"Rp {data['omzet_penjualan']:,.0f}")
        self.card_buyback._lbl_nilai.setText(f"Rp {data['total_buyback']:,.0f}")
        self.card_keluar._lbl_nilai.setText(f"Rp {data['total_pengeluaran']:,.0f}")
        saldo = data["saldo_kas"]
        self.card_saldo._lbl_nilai.setText(f"Rp {saldo:,.0f}")
        self.card_saldo._lbl_nilai.setObjectName(
            "card_value_red" if saldo < 0 else "card_value"
        )
        self.card_stok._lbl_nilai.setText(f"{data['stok_tersedia']} item")
        self.statusBar().showMessage(
            f"Gold-MS  |  Petugas: {ctrl.NAMA}  |  NIM: {ctrl.NIM}"
            f"  |  Terakhir diperbarui: {ctrl.get_tanggal_sekarang()}"
        )

    def _refresh_transaksi(self):
        rows = ctrl.ambil_transaksi()
        self.tabel_transaksi.setRowCount(0)
        for row in rows:
            r = self.tabel_transaksi.rowCount()
            self.tabel_transaksi.insertRow(r)
            nilai = [
                str(row["id"]), row["tanggal"], row["jenis"],
                row["nama_barang"], row["kategori"],
                f"{row['berat']:.2f}", f"{row['harga_gram']:,.0f}",
                f"{row['total_harga']:,.0f}",
                row["keterangan"] or "-"
            ]
            for c, v in enumerate(nilai):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                if row["jenis"] == "Penjualan":
                    item.setForeground(Qt.GlobalColor.darkGreen)
                elif row["jenis"] == "Buyback":
                    item.setForeground(Qt.GlobalColor.darkRed)
                self.tabel_transaksi.setItem(r, c, item)

    def _refresh_inventaris(self):
        rows = ctrl.ambil_inventaris()
        self.tabel_inventaris.setRowCount(0)
        for row in rows:
            r = self.tabel_inventaris.rowCount()
            self.tabel_inventaris.insertRow(r)
            nilai = [
                str(row["id"]), row["kode_barang"], row["nama_barang"],
                row["kategori"], row["kadar"], f"{row['berat']:.2f}",
                row["lokasi"], row["status"], row["tgl_input"]
            ]
            for c, v in enumerate(nilai):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                if row["status"] == "Tersedia":
                    item.setForeground(Qt.green) if c == 7 else None
                elif row["status"] in ("Terjual", "Dilebur"):
                    item.setForeground(Qt.red) if c == 7 else None
                self.tabel_inventaris.setItem(r, c, item)

    def _refresh_operasional(self):
        rows = ctrl.ambil_operasional()
        self.tabel_operasional.setRowCount(0)
        for row in rows:
            r = self.tabel_operasional.rowCount()
            self.tabel_operasional.insertRow(r)
            nilai = [
                str(row["id"]), row["tanggal"], row["tipe"],
                row["deskripsi"], f"{row['jumlah']:,.0f}",
                row["keterangan"] or "-"
            ]
            for c, v in enumerate(nilai):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabel_operasional.setItem(r, c, item)

    def _on_tambah_transaksi(self):
        dialog = TransaksiDialog(self)
        if dialog.exec():
            self._refresh_semua()

    def _on_hapus_transaksi(self):
        row = self.tabel_transaksi.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih baris transaksi yang ingin dihapus.")
            return
        id_t = int(self.tabel_transaksi.item(row, 0).text())
        konfirm = QMessageBox.question(
            self, "Hapus Transaksi",
            f"Yakin hapus transaksi ID <b>{id_t}</b>? Aksi ini tidak bisa dibatalkan.",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm == QMessageBox.Yes:
            ctrl.hapus_transaksi(id_t)
            self._refresh_semua()
            self.statusBar().showMessage("Transaksi berhasil dihapus.", 3000)

    def _on_tambah_inventaris(self):
        dialog = InventarisDialog(self)
        if dialog.exec():
            self._refresh_semua()

    def _on_edit_inventaris(self):
        row = self.tabel_inventaris.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih barang yang ingin diedit.")
            return
        data_edit = {
            "id":          int(self.tabel_inventaris.item(row, 0).text()),
            "kode_barang": self.tabel_inventaris.item(row, 1).text(),
            "nama_barang": self.tabel_inventaris.item(row, 2).text(),
            "kategori":    self.tabel_inventaris.item(row, 3).text(),
            "kadar":       self.tabel_inventaris.item(row, 4).text(),
            "berat":       float(self.tabel_inventaris.item(row, 5).text()),
            "lokasi":      self.tabel_inventaris.item(row, 6).text(),
            "status":      self.tabel_inventaris.item(row, 7).text(),
        }
        dialog = InventarisDialog(self, data_edit=data_edit)
        if dialog.exec():
            self._refresh_semua()

    def _on_hapus_inventaris(self):
        row = self.tabel_inventaris.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih barang yang ingin dihapus.")
            return
        id_b  = int(self.tabel_inventaris.item(row, 0).text())
        nama  = self.tabel_inventaris.item(row, 2).text()
        konfirm = QMessageBox.question(
            self, "Hapus Barang",
            f"Yakin hapus barang <b>{nama}</b> dari inventaris?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm == QMessageBox.Yes:
            ctrl.hapus_inventaris(id_b)
            self._refresh_semua()
            self.statusBar().showMessage(f"Barang '{nama}' dihapus dari inventaris.", 3000)

    def _on_tambah_operasional(self):
        dialog = OperasionalDialog(self)
        if dialog.exec():
            self._refresh_semua()

    def _on_hapus_operasional(self):
        row = self.tabel_operasional.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data operasional yang ingin dihapus.")
            return
        id_o = int(self.tabel_operasional.item(row, 0).text())
        desk = self.tabel_operasional.item(row, 3).text()
        konfirm = QMessageBox.question(
            self, "Hapus Data Operasional",
            f"Yakin hapus data operasional: <b>{desk}</b>?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm == QMessageBox.Yes:
            ctrl.hapus_operasional(id_o)
            self._refresh_semua()
            self.statusBar().showMessage("Data operasional berhasil dihapus.", 3000)
