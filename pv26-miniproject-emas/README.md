# Gold-MS — Gold Management System

Aplikasi manajemen data toko perhiasan emas berbasis **PySide6** dengan database **SQLite**.

---

## Deskripsi Aplikasi

**Gold-MS** adalah sistem manajemen toko emas yang dirancang dengan antarmuka bersih dan minimalis untuk efisiensi operasional. Fitur utama meliputi:
- Pencatatan transaksi **Penjualan** dan **Buyback** perhiasan.
- Manajemen **Inventaris** stok barang (kalung, cincin, gelang, dll.).
- Pencatatan **Operasional Toko** (pengeluaran bulanan, gaji, dll.).
- **Dashboard Real-time** untuk memantau omzet, pengeluaran, dan saldo kas harian.

---

## Cara Menjalankan

### Persyaratan
- Python 3.10+
- PySide6

### Instalasi
```bash
pip install PySide6
```

### Jalankan Aplikasi
```bash
python main.py
```

Database `toko_emas.db` akan dibuat otomatis di folder `data/` saat aplikasi pertama kali dijalankan.

---

## Struktur Project (Separation of Concerns)

Aplikasi ini dibangun dengan arsitektur **SoC** untuk memisahkan tanggung jawab setiap komponen:

```
pv26-miniproject-emas/
│
├── main.py               # Entry point: Inisialisasi app & load styling
├── database.py           # Model: Operasi database SQLite (CRUD)
├── controllers.py        # Controller: Logika bisnis & validasi data
├── views/                # View: Komponen antarmuka pengguna
│   ├── __init__.py
│   ├── main_window.py    # Jendela utama (Dashboard & Tabel)
│   └── dialogs.py        # Form input (Dialog terpisah)
├── assets/
│   └── style.qss         # Styling QSS eksternal (Tema Minimalist Light)
├── data/
│   └── toko_emas.db      # Database SQLite (Auto-generated)
└── README.md
```

---

## Desain Database

### Tabel inventaris
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER PK | Auto Increment |
| kode_barang | TEXT | Kode unik SKU |
| nama_barang | TEXT | Nama perhiasan |
| kategori | TEXT | Kalung/Cincin/dll |
| kadar | TEXT | 16K, 18K, 24K, dll |
| berat | REAL | Berat dalam gram |
| lokasi | TEXT | Etalase A/B/C |
| status | TEXT | Tersedia/Terjual/dll |
| tgl_input | TEXT | Tanggal pendaftaran |

### Tabel transaksi
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER PK | Auto Increment |
| tanggal | TEXT | Waktu transaksi |
| jenis | TEXT | Penjualan / Buyback |
| id_barang | INTEGER | FK ke inventaris |
| nama_barang | TEXT | Nama barang |
| kategori | TEXT | Kategori barang |
| berat | REAL | Berat gram |
| harga_gram | REAL | Harga per gram (Rp) |
| total_harga | REAL | Total nilai transaksi |
| keterangan | TEXT | Catatan tambahan |
| petugas | TEXT | Identitas petugas |

---

## Checklist Fitur Wajib

- [x] **Form input minimal 5 field**: Terpenuhi pada form Inventaris dan Transaksi.
- [x] **Signals & Slots**: Digunakan untuk seluruh interaksi komponen.
- [x] **Layout Manager**: Menggunakan QVBoxLayout, QHBoxLayout, dan QFormLayout.
- [x] **Tampilan Data**: Menggunakan QTableWidget untuk riwayat dan stok.
- [x] **Integrasi SQLite**: Mendukung operasi Create, Read, Update, dan Delete.
- [x] **Menu bar**: Menu "Tentang" yang menampilkan identitas mahasiswa.
- [x] **Dialog Terpisah**: Form input menggunakan QDialog (SoC).
- [x] **QMessageBox**: Dialog konfirmasi pada aksi krusial (hapus/simpan).
- [x] **Identitas Mahasiswa**: Nama dan NIM tampil permanen di Header dan Status Bar.
- [x] **Styling QSS Eksternal**: Tema Minimalist Light dimuat dari file `.qss`.
- [x] **Arsitektur SoC**: Pemisahan folder View, Controller, dan Model yang jelas.

---

## Teknologi yang Digunakan

- **Python 3.10+**
- **PySide6** (Qt for Python)
- **SQLite3**
- **QSS** (Qt Style Sheets)

---

## Video YouTube (Penjelasan CRUD)

> Link: [Akan diisi oleh mahasiswa]

Penjelasan alur fitur **Create** (Tambah Data):
`View (Dialog)` → `Controller (Simpan)` → `Database (Query)` → `View (Refresh Table)`

---
*Mini Project — Pemrograman Visual (PV26) | PySide6*
