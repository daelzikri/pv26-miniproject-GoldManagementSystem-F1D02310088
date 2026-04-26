# Gold-MS — Gold Management System

Aplikasi manajemen data toko perhiasan emas berbasis **PySide6** dengan database **SQLite**.

---

## Deskripsi Aplikasi

**Gold-MS** adalah solusi perangkat lunak manajemen inventaris dan operasional berbasis desktop yang dirancang khusus untuk sektor perdagangan perhiasan emas skala kecil hingga menengah. Aplikasi ini dikembangkan menggunakan framework PySide6 dengan arsitektur yang modular untuk mentransformasi proses pembukuan tradisional yang bersifat manual dan rentan terhadap kesalahan (human error) menjadi sistem digital yang terintegrasi. Fitur utama meliputi:
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


## Teknologi yang Digunakan
- **Python 3.10+**
- **PySide6** 
- **SQLite3**
- **QSS** 
