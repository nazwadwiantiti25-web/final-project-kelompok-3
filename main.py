from database import (
    simpan_mahasiswa,
    cari_mahasiswa,
    ambil_semua_mahasiswa,
    login_admin,
    urutkan_ipk,
    urutkan_penghasilan,
    hitung_skor,
    update_skor_mahasiswa,
    update_status_mahasiswa,
    hitung_total_pendaftar,
    hitung_total_diterima,
    hitung_total_ditolak,
    hitung_rata_rata_ipk,
    ambil_top_10_skor,
    hapus_data_mahasiswa,
    update_data_mahasiswa
)

# Menyimpan mahasiswa yang sedang login
user_login = None

def registrasi_mahasiswa():
    print("===== REGISTRASI MAHASISWA =====")
    nim = input("Masukkan NIM: ")
    nama = input("Masukkan Nama: ")
    password = input("Masukkan Password: ")
    ipk = float(input("Masukkan IPK: "))
    penghasilan = int(input("Masukkan Penghasilan Orang Tua: "))
    tanggungan = int(input("Masukkan Jumlah Tanggungan: "))

    # Validasi NIM
    if nim == "":
       print("NIM tidak boleh kosong.")
       return

    # Validasi Nama
    if nama == "":
       print("Nama tidak boleh kosong.")
       return

    # Validasi Password
    if password == "":
       print("Password tidak boleh kosong.")
       return

    # Validasi IPK
    if ipk < 3.00:
       print("Maaf. Anda tidak memenuhi syarat minimum IPK.")
       return

    # Validasi Penghasilan
    if penghasilan < 0:
       print("Penghasilan tidak boleh kurang dari 0.")
       return

    # Validasi Tanggungan
    if tanggungan < 1:
       print("Jumlah tanggungan harus minimal 1.")
       return

    print("Sebelum simpan database")
    
    simpan_mahasiswa(
        nim,
        nama,
        password,
        ipk,
        penghasilan,
        tanggungan
)
    print("Setelah simpan database")

    print("Registrasi berhasil!")

    print("Data yang diinput:")
    print("NIM :", nim)
    print("Nama :", nama)
    print("Password :", password)
    print("IPK :", ipk)
    print("Penghasilan :", penghasilan)
    print("Tanggungan :", tanggungan)


def menu_utama():
    while True:
        print("===== SCHOLAR TRACK =====")
        print("1. Registrasi")
        print("2. Login Mahasiswa")
        print("3. Login Admin")
        print("4. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            registrasi_mahasiswa()
        elif pilihan == "2":
            login_mahasiswa()
        elif pilihan == "3":
            login_admin_menu()
        elif pilihan == "4":
           print("Program selesai")
           break
        
        else:
            print("Pilihan tidak valid")

def login_mahasiswa():
    global user_login
    print("===== LOGIN MAHASISWA =====")

    nim = input("Masukkan NIM: ")
    password = input("Masukkan Password: ")

    mahasiswa = cari_mahasiswa(nim, password)

    if mahasiswa:
        user_login = {
            "nim": mahasiswa[0],
            "nama": mahasiswa[1],
            "password": mahasiswa[2],
            "ipk": mahasiswa[3],
            "penghasilan": mahasiswa[4],
            "tanggungan": mahasiswa[5],
            "skor_akhir": mahasiswa[6],
            "status_seleksi": mahasiswa[7]
        }

        print("Login berhasil!")
        menu_mahasiswa()
    else:
         print("Login gagal!")

def hapus_data():

    print("===== HAPUS DATA MAHASISWA =====")

    nim = input("Masukkan NIM mahasiswa: ")

    hapus_data_mahasiswa(nim)

    print("Data mahasiswa berhasil dihapus!")

def edit_data_mahasiswa():

    print("===== EDIT DATA MAHASISWA =====")

    nim = input("Masukkan NIM mahasiswa: ")

    nama = input("Nama baru: ")
    ipk = float(input("IPK baru: "))
    penghasilan = int(input("Penghasilan baru: "))
    tanggungan = int(input("Jumlah tanggungan baru: "))

    update_data_mahasiswa(
        nim,
        nama,
        ipk,
        penghasilan,
        tanggungan
    )

    print("Data mahasiswa berhasil diubah!")

def login_admin_menu():
    print("===== LOGIN ADMIN =====")

    username = input("Masukkan Username: ")
    password = input("Masukkan Password: ")

    admin = login_admin(username, password)

    if admin:
        print("Login admin berhasil!")
        menu_admin()
    else:
        print("Username atau password salah!")

def menu_admin():
    while True:
        print("===== MENU ADMIN =====")
        print("1. Lihat Semua Pendaftar")
        print("2. Urutkan Berdasarkan IPK")
        print("3. Urutkan Berdasarkan Penghasilan")
        print("4. Proses Hitung Skor Seleksi")
        print("5. Tentukan Kelulusan")
        print("6. Laporan Seleksi")
        print("7. Hapus Data Mahasiswa")
        print("8. Edit Data Mahasiswa")
        print("9. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_semua_mahasiswa()
        elif pilihan == "2":
            tampilkan_ipk_terurut()
        elif pilihan == "3":
            tampilkan_penghasilan_terurut()
        elif pilihan == "4":
            proses_hitung_skor()
        elif pilihan == "5":
            tentukan_kelulusan()
        elif pilihan == "6":
            laporan_seleksi()
        elif pilihan == "7":
            hapus_data()
        elif pilihan == "8":
            edit_data_mahasiswa()
        elif pilihan == "9":
            print("Logout admin berhasil")
            break
        else:
            print("Pilihan tidak valid")

def lihat_profil():
    print("===== PROFIL SAYA =====")
    print("NIM :", user_login["nim"])
    print("Nama :", user_login["nama"])
    print("IPK :", user_login["ipk"])
    print("Penghasilan :", user_login["penghasilan"])
    print("Tanggungan :", user_login["tanggungan"])

def lihat_skor():
    print("===== SKOR SELEKSI =====")
    print("Skor Akhir :", user_login["skor_akhir"])

def lihat_status():
    print("===== STATUS SELEKSI =====")
    print("Status :", user_login["status_seleksi"])

def tampilkan_semua_mahasiswa():
    data = ambil_semua_mahasiswa()

    print("===== DATA MAHASISWA =====")

    for mahasiswa in data:
        print("NIM :", mahasiswa[0])
        print("Nama :", mahasiswa[1])
        print("IPK :", mahasiswa[3])
        print("Penghasilan :", mahasiswa[4])
        print("Tanggungan :", mahasiswa[5])
        print("Skor Akhir :", mahasiswa[6])
        print("Status :", mahasiswa[7])
        print("-" * 30)

def tampilkan_ipk_terurut():
    data = urutkan_ipk()

    print("===== DATA BERDASARKAN IPK =====")

    for mahasiswa in data:
        print("NIM :", mahasiswa[0])
        print("Nama :", mahasiswa[1])
        print("IPK :", mahasiswa[3])
        print("-" * 30)

def tampilkan_penghasilan_terurut():
    data = urutkan_penghasilan()

    print("===== DATA BERDASARKAN PENGHASILAN =====")

    rangking = 1

    for mahasiswa in data:
        print("Rangking :", rangking)
        print("NIM :", mahasiswa[0])
        print("Nama :", mahasiswa[1])
        print("Penghasilan :", mahasiswa[4])
        print("-" * 30)

        rangking += 1

def menu_hapus_mahasiswa_():

    print("===== HAPUS DATA MAHASISWA =====")

    nim = input("Masukkan NIM mahasiswa yang ingin dihapus: ")

    hapus_data_mahasiswa(nim)

    print("Data mahasiswa berhasil dihapus!")

def proses_hitung_skor():
    data = ambil_semua_mahasiswa()

    for mahasiswa in data:
        nim = mahasiswa[0]
        ipk = mahasiswa[3]
        penghasilan = mahasiswa[4]

        skor = hitung_skor(ipk, penghasilan)

        update_skor_mahasiswa(nim, skor)

    print("Skor seluruh mahasiswa berhasil dihitung!")

def tentukan_kelulusan():
    data = ambil_semua_mahasiswa()

    data_urut = sorted(
        data,
        key=lambda mahasiswa: mahasiswa[6],
        reverse=True
    )

    kuota = 50

    for i, mahasiswa in enumerate(data_urut):
        nim = mahasiswa[0]

        if i < kuota:
            update_status_mahasiswa(nim, "DITERIMA")
        else:
            update_status_mahasiswa(nim, "DITOLAK")

    print("Status kelulusan berhasil ditentukan!")

def laporan_seleksi():
    print("===== LAPORAN SELEKSI =====")

    print("Total Pendaftar :", hitung_total_pendaftar())
    print("Total Diterima :", hitung_total_diterima())
    print("Total Ditolak :", hitung_total_ditolak())
    print("Rata-rata IPK :", hitung_rata_rata_ipk())

    print("===== TOP 10 MAHASISWA =====")

    data = ambil_top_10_skor()

    ranking = 1

    for mahasiswa in data:
        print("Ranking :", ranking)
        print("Nama :", mahasiswa[1])
        print("Skor :", mahasiswa[6])
        print("Status :", mahasiswa[7])
        print("-" * 30)

        ranking += 1

def menu_mahasiswa():
    while True:
        print("===== MENU MAHASISWA =====")
        print("1. Profil Saya")
        print("2. Lihat Skor Seleksi")
        print("3. Lihat Status Seleksi")
        print("4. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_profil() 
        elif pilihan == "2":
            lihat_skor()
        elif pilihan == "3":
            lihat_status()
        elif pilihan == "4":
            print("Logout berhasil")
            break
        else:
            print("Pilihan tidak valid")

menu_utama()



