import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "toko_emas.db")

def get_connection():#agar dapat memulai koneksi database
    conn = sqlite3.connect(DB_PATH)#sesuaikan dengan path database yang dismpan dalam variabel DB_PATH
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor() # harus pakai cursor agar dapat menjalankan sql nya, tidak bisa hanya conn saja

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventaris (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_barang TEXT    NOT NULL UNIQUE,
            nama_barang TEXT    NOT NULL,
            kategori    TEXT    NOT NULL,
            kadar       TEXT    NOT NULL,
            berat       REAL    NOT NULL,
            lokasi      TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'Tersedia',
            tgl_input   TEXT    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal     TEXT    NOT NULL,
            jenis       TEXT    NOT NULL,
            id_barang   INTEGER,
            nama_barang TEXT    NOT NULL,
            kategori    TEXT    NOT NULL,
            berat       REAL    NOT NULL,
            harga_gram  REAL    NOT NULL,
            total_harga REAL    NOT NULL,
            keterangan  TEXT,
            petugas     TEXT    NOT NULL,
            FOREIGN KEY (id_barang) REFERENCES inventaris(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operasional (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal     TEXT    NOT NULL,
            tipe        TEXT    NOT NULL,
            deskripsi   TEXT    NOT NULL,
            jumlah      REAL    NOT NULL,
            keterangan  TEXT
        )
    """)

    conn.commit()
    conn.close()

    #FUNGSI SELANJUTNYA HINGGA AKHIR MEMILIKI KEGUNAAN YANG SAMA SEPERTI NAMA FUNGSINYA

def tambah_stok(kode, nama, kategori, kadar, berat, lokasi, status, tgl_input):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO inventaris (kode_barang, nama_barang, kategori, kadar, berat, lokasi, status, tgl_input)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (kode, nama, kategori, kadar, berat, lokasi, status, tgl_input))
        conn.commit()
        return True, "Barang berhasil ditambahkan ke inventaris."
    except sqlite3.IntegrityError:
        return False, f"Kode barang '{kode}' sudah ada. Gunakan kode yang berbeda."
    finally:
        conn.close()

def ambil_semua_stok():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM inventaris ORDER BY tgl_input DESC").fetchall()
    conn.close()
    return rows

def ambil_stok_tersedia():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, kode_barang, nama_barang, kategori, berat FROM inventaris WHERE status = 'Tersedia' ORDER BY nama_barang"
    ).fetchall()
    conn.close()
    return rows

def update_status_barang(id_barang, status_baru):
    conn = get_connection()
    conn.execute("UPDATE inventaris SET status = ? WHERE id = ?", (status_baru, id_barang))
    conn.commit()
    conn.close()


def update_stok(id_barang, kode, nama, kategori, kadar, berat, lokasi, status):
    conn = get_connection()
    try:
        conn.execute("""
            UPDATE inventaris
            SET kode_barang=?, nama_barang=?, kategori=?, kadar=?, berat=?, lokasi=?, status=?
            WHERE id=?
        """, (kode, nama, kategori, kadar, berat, lokasi, status, id_barang))
        conn.commit()
        return True, "Data barang berhasil diperbarui."
    except sqlite3.IntegrityError:
        return False, f"Kode barang '{kode}' sudah digunakan barang lain."
    finally:
        conn.close()

def hapus_stok(id_barang):
    conn = get_connection()
    conn.execute("DELETE FROM inventaris WHERE id = ?", (id_barang,))
    conn.commit()
    conn.close()

def cek_kode_duplikat(kode, exclude_id=None):
    conn = get_connection()
    if exclude_id:
        row = conn.execute(
            "SELECT id FROM inventaris WHERE kode_barang = ? AND id != ?", (kode, exclude_id)
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT id FROM inventaris WHERE kode_barang = ?", (kode,)
        ).fetchone()
    conn.close()
    return row is not None

def tambah_transaksi(tanggal, jenis, id_barang, nama_barang, kategori, berat,
                     harga_gram, total_harga, keterangan, petugas):
    conn = get_connection()
    conn.execute("""
        INSERT INTO transaksi
            (tanggal, jenis, id_barang, nama_barang, kategori, berat, harga_gram, total_harga, keterangan, petugas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tanggal, jenis, id_barang, nama_barang, kategori, berat,
          harga_gram, total_harga, keterangan, petugas))
    conn.commit()
    conn.close()

def ambil_semua_transaksi():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM transaksi ORDER BY tanggal DESC").fetchall()
    conn.close()
    return rows

def hapus_transaksi(id_transaksi):
    conn = get_connection()
    conn.execute("DELETE FROM transaksi WHERE id = ?", (id_transaksi,))
    conn.commit()
    conn.close()

def tambah_operasional(tanggal, tipe, deskripsi, jumlah, keterangan):
    conn = get_connection()
    conn.execute("""
        INSERT INTO operasional (tanggal, tipe, deskripsi, jumlah, keterangan)
        VALUES (?, ?, ?, ?, ?)
    """, (tanggal, tipe, deskripsi, jumlah, keterangan))
    conn.commit()
    conn.close()

def ambil_semua_operasional():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM operasional ORDER BY tanggal DESC").fetchall()
    conn.close()
    return rows

def hapus_operasional(id_ops):
    conn = get_connection()
    conn.execute("DELETE FROM operasional WHERE id = ?", (id_ops,))
    conn.commit()
    conn.close()

def hitung_total_penjualan_hari_ini(tanggal_hari_ini):
    conn = get_connection()
    row = conn.execute("""
        SELECT COALESCE(SUM(total_harga), 0) as total
        FROM transaksi
        WHERE jenis = 'Penjualan' AND tanggal LIKE ?
    """, (f"{tanggal_hari_ini}%",)).fetchone()
    conn.close()
    return row["total"]

def hitung_total_buyback_hari_ini(tanggal_hari_ini):
    conn = get_connection()
    row = conn.execute("""
        SELECT COALESCE(SUM(total_harga), 0) as total
        FROM transaksi
        WHERE jenis = 'Buyback' AND tanggal LIKE ?
    """, (f"{tanggal_hari_ini}%",)).fetchone()
    conn.close()
    return row["total"]

def hitung_total_pengeluaran_hari_ini(tanggal_hari_ini):
    conn = get_connection()
    row = conn.execute("""
        SELECT COALESCE(SUM(jumlah), 0) as total
        FROM operasional
        WHERE tipe = 'Pengeluaran Toko' AND tanggal LIKE ?
    """, (f"{tanggal_hari_ini}%",)).fetchone()
    conn.close()
    return row["total"]

def hitung_jumlah_stok_tersedia():
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as total FROM inventaris WHERE status = 'Tersedia'"
    ).fetchone()
    conn.close()
    return row["total"]
