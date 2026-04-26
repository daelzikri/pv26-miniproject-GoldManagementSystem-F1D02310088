from PySide6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit,
    QPushButton, QLabel, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
import controllers as ctrl

class InventarisDialog(QDialog):
    def __init__(self, parent=None, data_edit=None):
        super().__init__(parent)
        self.data_edit = data_edit  
        self.setWindowTitle("Tambah Barang" if not data_edit else "Edit Barang")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui()
        if data_edit:
            self._isi_data_edit()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        judul = QLabel(" Form Data Inventaris Barang")
        judul.setObjectName("title_label")
        judul.setAlignment(Qt.AlignCenter)
        layout.addWidget(judul)

        garis = QFrame()
        garis.setFrameShape(QFrame.HLine)
        layout.addWidget(garis)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(10)

        self.input_kode = QLineEdit()
        self.input_kode.setPlaceholderText("Contoh: GLD-001")
        self.input_kode.setToolTip("Kode unik untuk setiap barang (tidak boleh sama)")
        form.addRow("Kode Barang / SKU:", self.input_kode)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Contoh: Kalung Model Bunga")
        form.addRow("Nama Perhiasan:", self.input_nama)

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems([
            "Kalung", "Cincin", "Gelang", "Anting",
            "Logam Mulia / Batangan", "Liontin", "Lainnya"
        ])
        form.addRow("Kategori:", self.combo_kategori)

        self.combo_kadar = QComboBox()
        self.combo_kadar.addItems(["16K", "17K", "18K", "22K", "24K", "Perak 925"])
        form.addRow("Kadar (Karat):", self.combo_kadar)

        self.spin_berat = QDoubleSpinBox()
        self.spin_berat.setRange(0.01, 9999.99)
        self.spin_berat.setDecimals(2)
        self.spin_berat.setSuffix(" gram")
        self.spin_berat.setSingleStep(0.05)
        form.addRow("Berat (Gram):", self.spin_berat)

        self.combo_lokasi = QComboBox()
        self.combo_lokasi.addItems([
            "Etalase A", "Etalase B", "Etalase C",
            "Brankas Utama", "Gudang", "Lainnya"
        ])
        form.addRow("Lokasi Penyimpanan:", self.combo_lokasi)

        self.combo_status = QComboBox()
        self.combo_status.addItems([
            "Tersedia", "Dalam Perbaikan", "Dilebur", "Buyback - Masuk Kembali"
        ])
        form.addRow("Status Barang:", self.combo_status)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btn_secondary")
        self.btn_simpan = QPushButton("💾  Simpan ke Inventaris")

        self.btn_batal.clicked.connect(self.reject)
        self.btn_simpan.clicked.connect(self._on_simpan)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        layout.addLayout(btn_layout)

    def _isi_data_edit(self):
        d = self.data_edit
        self.input_kode.setText(d["kode_barang"])
        self.input_nama.setText(d["nama_barang"])
        self._set_combo(self.combo_kategori, d["kategori"])
        self._set_combo(self.combo_kadar, d["kadar"])
        self.spin_berat.setValue(d["berat"])
        self._set_combo(self.combo_lokasi, d["lokasi"])
        self._set_combo(self.combo_status, d["status"])

    def _set_combo(self, combo, teks):
        idx = combo.findText(teks)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _on_simpan(self):
        kode     = self.input_kode.text()
        nama     = self.input_nama.text()
        kategori = self.combo_kategori.currentText()
        kadar    = self.combo_kadar.currentText()
        berat    = self.spin_berat.value()
        lokasi   = self.combo_lokasi.currentText()
        status   = self.combo_status.currentText()

        konfirm = QMessageBox.question(
            self, "Konfirmasi Simpan",
            f"Simpan barang <b>{nama}</b> (Kode: {kode}) ke inventaris?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm != QMessageBox.Yes:
            return

        if self.data_edit:
            ok, pesan = ctrl.edit_inventaris(
                self.data_edit["id"], kode, nama, kategori, kadar, berat, lokasi, status
            )
        else:
            ok, pesan = ctrl.simpan_inventaris(kode, nama, kategori, kadar, berat, lokasi, status)

        if ok:
            QMessageBox.information(self, "Berhasil", pesan)
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", pesan)

class TransaksiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Catat Transaksi")
        self.setMinimumWidth(500)
        self.setModal(True)
        self._stok_map = {}  # {tampilan_text: id_barang}
        self._build_ui()
        self._muat_stok()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        judul = QLabel(" Form Transaksi Penjualan / Buyback")
        judul.setObjectName("title_label")
        judul.setAlignment(Qt.AlignCenter)
        layout.addWidget(judul)

        garis = QFrame()
        garis.setFrameShape(QFrame.HLine)
        layout.addWidget(garis)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(10)

        self.combo_jenis = QComboBox()
        self.combo_jenis.addItems(["Penjualan", "Buyback"])
        self.combo_jenis.currentTextChanged.connect(self._on_jenis_berubah)
        form.addRow("Jenis Transaksi:", self.combo_jenis)

        self.combo_stok = QComboBox()
        self.combo_stok.addItem("-- Input Manual (Buyback/Baru) --")
        self.combo_stok.currentIndexChanged.connect(self._on_stok_dipilih)
        form.addRow("Pilih dari Stok:", self.combo_stok)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama perhiasan / deskripsi singkat")
        form.addRow("Nama Barang:", self.input_nama)

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems([
            "Kalung", "Cincin", "Gelang", "Anting",
            "Logam Mulia / Batangan", "Liontin", "Lainnya"
        ])
        form.addRow("Kategori:", self.combo_kategori)

        self.spin_berat = QDoubleSpinBox()
        self.spin_berat.setRange(0.01, 9999.99)
        self.spin_berat.setDecimals(2)
        self.spin_berat.setSuffix(" gram")
        self.spin_berat.setSingleStep(0.05)
        self.spin_berat.valueChanged.connect(self._hitung_total)
        form.addRow("Berat (Gram):", self.spin_berat)

        self.input_harga = QLineEdit()
        self.input_harga.setPlaceholderText("Contoh: 1050000")
        self.input_harga.textChanged.connect(self._hitung_total)
        form.addRow("Harga / Gram (Rp):", self.input_harga)

        self.input_total = QLineEdit()
        self.input_total.setReadOnly(True)
        self.input_total.setPlaceholderText("Terhitung otomatis")
        self.input_total.setToolTip("Berat × Harga Per Gram")
        form.addRow("Total Harga (Rp):", self.input_total)

        self.input_ket = QTextEdit()
        self.input_ket.setPlaceholderText("Keterangan tambahan (opsional)...")
        self.input_ket.setMaximumHeight(70)
        form.addRow("Keterangan:", self.input_ket)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btn_secondary")
        self.btn_simpan = QPushButton("💾  Simpan Transaksi")

        self.btn_batal.clicked.connect(self.reject)
        self.btn_simpan.clicked.connect(self._on_simpan)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        layout.addLayout(btn_layout)

    def _muat_stok(self):
        stok_list = ctrl.ambil_stok_untuk_penjualan()
        self._stok_map = {}
        for row in stok_list:
            teks = f"{row['kode_barang']} | {row['nama_barang']} ({row['berat']:.2f}g)"
            self._stok_map[teks] = {
                "id": row["id"],
                "nama": row["nama_barang"],
                "kategori": row["kategori"],
                "berat": row["berat"],
            }
            self.combo_stok.addItem(teks)

    def _on_stok_dipilih(self, index):
        if index <= 0:
            self.input_nama.setReadOnly(False)
            self.spin_berat.setReadOnly(False)
            return
        teks = self.combo_stok.currentText()
        data = self._stok_map.get(teks)
        if data:
            self.input_nama.setText(data["nama"])
            self.input_nama.setReadOnly(True)
            idx_kat = self.combo_kategori.findText(data["kategori"])
            if idx_kat >= 0:
                self.combo_kategori.setCurrentIndex(idx_kat)
            self.spin_berat.setValue(data["berat"])
            self.spin_berat.setReadOnly(True)

    def _on_jenis_berubah(self, jenis):
        if jenis == "Buyback":
            self.combo_stok.setCurrentIndex(0)
            self.input_nama.setReadOnly(False)
            self.spin_berat.setReadOnly(False)

    def _hitung_total(self):
        total = ctrl.hitung_total_transaksi(
            self.spin_berat.value(), self.input_harga.text()
        )
        if total > 0:
            self.input_total.setText(f"Rp {total:,.0f}")
        else:
            self.input_total.clear()

    def _on_simpan(self):
        jenis    = self.combo_jenis.currentText()
        nama     = self.input_nama.text()
        kategori = self.combo_kategori.currentText()
        berat    = self.spin_berat.value()
        harga    = self.input_harga.text()
        ket      = self.input_ket.toPlainText()

        id_barang = None
        idx = self.combo_stok.currentIndex()
        if idx > 0:
            teks  = self.combo_stok.currentText()
            data  = self._stok_map.get(teks)
            if data:
                id_barang = data["id"]

        total = ctrl.hitung_total_transaksi(berat, harga)

        konfirm = QMessageBox.question(
            self, "Konfirmasi Transaksi",
            f"Simpan transaksi <b>{jenis}</b>?<br>"
            f"Barang: {nama}<br>"
            f"Total: <b>Rp {total:,.0f}</b>",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm != QMessageBox.Yes:
            return

        ok, pesan = ctrl.simpan_transaksi(
            jenis, id_barang, nama, kategori, berat, harga, ket
        )
        if ok:
            QMessageBox.information(self, "Berhasil", pesan)
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", pesan)

class OperasionalDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Catat Data Operasional")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        judul = QLabel(" Form Operasional Toko")
        judul.setObjectName("title_label")
        judul.setAlignment(Qt.AlignCenter)
        layout.addWidget(judul)

        garis = QFrame()
        garis.setFrameShape(QFrame.HLine)
        layout.addWidget(garis)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(10)

        self.combo_tipe = QComboBox()
        self.combo_tipe.addItems([
            "Pengeluaran Toko",
            "Pembelian Emas / Stok Baru",
            "Biaya Operasional Lain",
            "Pemasukan Non-Penjualan",
            "Pengeluaran Modal",
        ])
        form.addRow("Tipe:", self.combo_tipe)

        self.input_deskripsi = QLineEdit()
        self.input_deskripsi.setPlaceholderText("Contoh: Bayar listrik bulan ini")
        form.addRow("Deskripsi:", self.input_deskripsi)

        self.spin_jumlah = QDoubleSpinBox()
        self.spin_jumlah.setRange(0.01, 999_999_999.99)
        self.spin_jumlah.setDecimals(0)
        self.spin_jumlah.setPrefix("Rp ")
        self.spin_jumlah.setSingleStep(10000)
        form.addRow("Nominal (Rp):", self.spin_jumlah)

        self.input_ket = QTextEdit()
        self.input_ket.setPlaceholderText("Keterangan tambahan (opsional)...")
        self.input_ket.setMaximumHeight(70)
        form.addRow("Keterangan:", self.input_ket)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btn_secondary")
        self.btn_simpan = QPushButton("💾  Simpan Data Operasional")

        self.btn_batal.clicked.connect(self.reject)
        self.btn_simpan.clicked.connect(self._on_simpan)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        layout.addLayout(btn_layout)

    def _on_simpan(self):
        tipe  = self.combo_tipe.currentText()
        desk  = self.input_deskripsi.text()
        juml  = self.spin_jumlah.value()
        ket   = self.input_ket.toPlainText()

        konfirm = QMessageBox.question(
            self, "Konfirmasi",
            f"Simpan data operasional:<br><b>{tipe}</b> — {desk}<br>Nominal: <b>Rp {juml:,.0f}</b>?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirm != QMessageBox.Yes:
            return

        ok, pesan = ctrl.simpan_operasional(tipe, desk, juml, ket)
        if ok:
            QMessageBox.information(self, "Berhasil", pesan)
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", pesan)
