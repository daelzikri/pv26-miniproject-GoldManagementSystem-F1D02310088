from datetime import datetime
import database as db

NAMA = "PUDAEL ZIKRI"
NIM  = "F1D02310088"

#FILE INI AKAN MELAKUKAN PENGECEKAN TERHADAP SEMUA AKTIVITAS YANG DILAKUKAN USER SEBELUM DISIMPAN KE DATABASE
#KEGUNAAN SETIAP FUNCTION SUDAH SESUAI DENGAN NAMA MASING-MASING FUNCTION
def get_petugas_string():
    return f"{NAMA} / {NIM}"

def get_tanggal_sekarang():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_tanggal_hari_ini():
    return datetime.now().strftime("%Y-%m-%d")

def validasi_tidak_kosong(fields: dict) -> tuple[bool, str]:
    for label, nilai in fields.items():
        if isinstance(nilai, str) and not nilai.strip():
            return False, f"Field '{label}' tidak boleh kosong."
        if nilai is None:
            return False, f"Field '{label}' tidak boleh kosong."
    return True, ""

def validasi_angka_positif(nilai, label) -> tuple[bool, str]:
    try:
        angka = float(nilai)
        if angka <= 0:
            return False, f"'{label}' harus lebih dari 0."
        return True, ""
    except (ValueError, TypeError):
        return False, f"'{label}' harus berupa angka."

def simpan_inventaris(kode, nama, kategori, kadar, berat, lokasi, status) -> tuple[bool, str]:
    ok, pesan = validasi_tidak_kosong({
        "Kode Barang": kode,
        "Nama Perhiasan": nama,
        "Kategori": kategori,
        "Kadar": kadar,
        "Lokasi": lokasi,
        "Status": status,
    })
    if not ok:
        return False, pesan

    ok, pesan = validasi_angka_positif(berat, "Berat Gram")
    if not ok:
        return False, pesan

    tgl = get_tanggal_hari_ini()
    return db.tambah_stok(kode.strip().upper(), nama.strip(), kategori, kadar,
                          float(berat), lokasi, status, tgl)


def edit_inventaris(id_barang, kode, nama, kategori, kadar, berat, lokasi, status) -> tuple[bool, str]:
    ok, pesan = validasi_tidak_kosong({
        "Kode Barang": kode,
        "Nama Perhiasan": nama,
    })
    if not ok:
        return False, pesan

    ok, pesan = validasi_angka_positif(berat, "Berat Gram")
    if not ok:
        return False, pesan

    if db.cek_kode_duplikat(kode.strip().upper(), exclude_id=id_barang):
        return False, f"Kode barang '{kode}' sudah digunakan barang lain."

    return db.update_stok(id_barang, kode.strip().upper(), nama.strip(),
                          kategori, kadar, float(berat), lokasi, status)


def hapus_inventaris(id_barang):
    db.hapus_stok(id_barang)


def ambil_inventaris():
    return db.ambil_semua_stok()


def ambil_stok_untuk_penjualan():
    return db.ambil_stok_tersedia()

def simpan_transaksi(jenis, id_barang, nama_barang, kategori,
                     berat, harga_gram, keterangan) -> tuple[bool, str]:
    ok, pesan = validasi_tidak_kosong({
        "Nama Barang": nama_barang,
        "Kategori": kategori,
        "Jenis Transaksi": jenis,
    })
    if not ok:
        return False, pesan

    ok, pesan = validasi_angka_positif(berat, "Berat Gram")
    if not ok:
        return False, pesan

    ok, pesan = validasi_angka_positif(harga_gram, "Harga Per Gram")
    if not ok:
        return False, pesan

    berat_f      = float(berat)
    harga_gram_f = float(harga_gram)
    total        = berat_f * harga_gram_f
    tanggal      = get_tanggal_sekarang()
    petugas      = get_petugas_string()

    db.tambah_transaksi(tanggal, jenis, id_barang, nama_barang.strip(),
                        kategori, berat_f, harga_gram_f, total,
                        keterangan.strip() if keterangan else "", petugas)

    if id_barang:
        if jenis == "Penjualan":
            db.update_status_barang(id_barang, "Terjual")
        elif jenis == "Buyback":
            db.update_status_barang(id_barang, "Buyback - Masuk Kembali")

    return True, f"Transaksi {jenis} berhasil disimpan. Total: Rp {total:,.0f}"

def hapus_transaksi(id_transaksi):
    db.hapus_transaksi(id_transaksi)

def ambil_transaksi():
    return db.ambil_semua_transaksi()

def hitung_total_transaksi(berat, harga_gram) -> float:
    try:
        return float(berat) * float(harga_gram)
    except (ValueError, TypeError):
        return 0.0
    
def simpan_operasional(tipe, deskripsi, jumlah, keterangan) -> tuple[bool, str]:
    ok, pesan = validasi_tidak_kosong({
        "Tipe": tipe,
        "Deskripsi": deskripsi,
    })
    if not ok:
        return False, pesan

    ok, pesan = validasi_angka_positif(jumlah, "Jumlah/Nominal")
    if not ok:
        return False, pesan

    tanggal = get_tanggal_sekarang()
    db.tambah_operasional(tanggal, tipe, deskripsi.strip(),
                          float(jumlah), keterangan.strip() if keterangan else "")
    return True, f"Data operasional '{tipe}' berhasil disimpan."

def hapus_operasional(id_ops):
    db.hapus_operasional(id_ops)

def ambil_operasional():
    return db.ambil_semua_operasional()

def ambil_data_dashboard() -> dict:
    hari_ini = get_tanggal_hari_ini()

    total_jual    = db.hitung_total_penjualan_hari_ini(hari_ini)
    total_buyback = db.hitung_total_buyback_hari_ini(hari_ini)
    total_keluar  = db.hitung_total_pengeluaran_hari_ini(hari_ini)
    stok_tersedia = db.hitung_jumlah_stok_tersedia()

    saldo_kas = total_jual - total_buyback - total_keluar

    return {
        "omzet_penjualan":  total_jual,
        "total_buyback":    total_buyback,
        "total_pengeluaran": total_keluar,
        "saldo_kas":         saldo_kas,
        "stok_tersedia":     stok_tersedia,
        "tanggal":           hari_ini,
    }
