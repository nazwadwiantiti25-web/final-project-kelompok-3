import sqlite3

# Membuat koneksi ke database
conn = sqlite3.connect("scholartrack.db", timeout=10, check_same_thread=False)

# Membuat cursor
cursor = conn.cursor()

# Membuat tabel mahasiswa jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa (
    nim TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    password TEXT NOT NULL,
    ipk REAL NOT NULL,
    penghasilan INTEGER NOT NULL,
    tanggungan INTEGER NOT NULL,
    skor_akhir REAL DEFAULT 0,
    status_seleksi TEXT DEFAULT 'Belum Diproses'
)
""")
# Memebuat tabel admin jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

# Simpan perubahan
conn.commit()

print("Database berhasil dibuat!")

cursor.execute("""
INSERT OR IGNORE INTO admin
(username, password)
VALUES ('admin', 'admin123')
""")

conn.commit()

# Fungsi untuk menyimpan data mahasiswa ke database

def simpan_mahasiswa(
    nim,
    nama,
    password,
    ipk,
    penghasilan,
    tanggungan
):
    
    try:
        # Menyimpan data mahasiswa ke database
        cursor.execute("""
        INSERT INTO mahasiswa
        (nim, nama, password, ipk, penghasilan, tanggungan)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nim,
            nama,
            password,
            ipk,
            penghasilan,
            tanggungan
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        print("NIM sudah terdaftar di database.")

# Fungsi mencari mahasiswa untuk login
def cari_mahasiswa(nim, password):
    cursor.execute("""
    SELECT * FROM mahasiswa 
    WHERE nim = ? AND password = ?
    """, (nim, password))

    return cursor.fetchone()

def ambil_semua_mahasiswa():
    cursor.execute("""
    SELECT * FROM mahasiswa
    """)

    return cursor.fetchall()

def login_admin(username, password):
    cursor.execute("""
    SELECT * FROM admin
    WHERE username = ? AND password = ?
    """, (username, password))

    return cursor.fetchone()

def urutkan_ipk():
    cursor.execute("""
    SELECT * FROM mahasiswa
    ORDER BY ipk DESC
    """)

    return cursor.fetchall()

def urutkan_penghasilan():
    cursor.execute("""
    SELECT * FROM mahasiswa
    ORDER BY penghasilan ASC
    """)

    return cursor.fetchall()

def hitung_nilai_ekonomi(penghasilan):
    if penghasilan <= 2000000:
        return 100
    elif penghasilan <= 4000000:
        return 80
    elif penghasilan <= 6000000:
        return 60
    else:
        return 40
        
def hitung_skor(ipk, penghasilan):
    nilai_ekonomi = hitung_nilai_ekonomi(penghasilan)

    skor = (ipk * 40) + (nilai_ekonomi * 60)

    return skor

def update_skor_mahasiswa(nim, skor):
    cursor.execute("""
    UPDATE mahasiswa
    SET skor_akhir = ?
    WHERE nim = ?
    """, (skor, nim))

    conn.commit()

def update_status_mahasiswa(nim, status):
    cursor.execute("""
    UPDATE mahasiswa
    SET status_seleksi = ?
    WHERE nim = ?
    """, (status, nim))

    conn.commit()    

def hitung_total_pendaftar():
    cursor.execute("""
    SELECT COUNT(*) FROM mahasiswa
    """)

    return cursor.fetchone()[0]

def hitung_total_diterima():
    cursor.execute("""
    SELECT COUNT(*)
    FROM mahasiswa
    WHERE status_seleksi = 'DITERIMA'
    """)

    return cursor.fetchone()[0]

def hitung_total_ditolak():
    cursor.execute("""
    SELECT COUNT(*)
    FROM mahasiswa
    WHERE status_seleksi = 'DITOLAK'
    """)

    return cursor.fetchone()[0]

def hitung_rata_rata_ipk():
    cursor.execute("""
    SELECT AVG(ipk)
    FROM mahasiswa
    """)

    hasil = cursor.fetchone()[0]

    if hasil is None:
        return 0

    return round(hasil, 2)

def ambil_top_10_skor():
    cursor.execute("""
    SELECT *
    FROM mahasiswa
    ORDER BY skor_akhir DESC
    LIMIT 10
    """)

    return cursor.fetchall()

def hapus_data_mahasiswa(nim):

    cursor.execute("""
    DELETE FROM mahasiswa
    WHERE nim = ?
    """,(nim,))

    conn.commit()

def update_data_mahasiswa(nim, nama, ipk, penghasilan, tanggungan):

    cursor.execute("""
    UPDATE mahasiswa
    SET nama = ?,
        ipk = ?,
        penghasilan = ?,
        tanggungan = ?
    WHERE nim = ?
    """, (
        nama,
        ipk,
        penghasilan,
        tanggungan,
        nim
    ))

    conn.commit()