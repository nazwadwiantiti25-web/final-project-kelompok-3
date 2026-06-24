from flask import Flask, render_template, request, redirect
from database import (
    cari_mahasiswa, 
    simpan_mahasiswa,
    login_admin,
    ambil_semua_mahasiswa,
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
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nim = request.form["nim"]
        nama = request.form["nama"]
        password = request.form["password"]
        ipk = float(request.form["ipk"])
        penghasilan = int(request.form["penghasilan"])
        tanggungan = int(request.form["tanggungan"])


        if ipk < 3.00:
            return "Maaf. Anda tidak memenuhi syarat minimum IPK."


        simpan_mahasiswa(
            nim,
            nama,
            password,
            ipk,
            penghasilan,
            tanggungan
        )

        return "Registrasi berhasil!"


    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        nim = request.form["nim"]
        password = request.form["password"]

        mahasiswa = cari_mahasiswa(nim, password)

        if mahasiswa:
           return render_template(
              "dashboard.html",
               mahasiswa=mahasiswa
           )

        else:
            return "Login gagal!"


    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = login_admin(username, password)

        if admin:

            data = ambil_semua_mahasiswa()

            return render_template(
                "admin.html",
                data=data
            )

        else:
            return "Login admin gagal!"


    return render_template("admin_login.html")

@app.route("/admin/ipk")
def admin_ipk():

    data = urutkan_ipk()

    return render_template(
        "admin.html",
        data=data
    )

@app.route("/admin/penghasilan")
def admin_penghasilan():

    data = urutkan_penghasilan()

    return render_template(
        "admin.html",
        data=data
    )

@app.route("/admin/hitung-skor")
def admin_hitung_skor():

    data = ambil_semua_mahasiswa()

    for mahasiswa in data:

        nim = mahasiswa[0]
        ipk = mahasiswa[3]
        penghasilan = mahasiswa[4]

        skor = hitung_skor(
            ipk,
            penghasilan
        )

        update_skor_mahasiswa(
            nim,
            skor
        )


    data_baru = ambil_semua_mahasiswa()

    return render_template(
        "admin.html",
        data=data_baru
    )

@app.route("/admin/kelulusan")
def admin_kelulusan():

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
            update_status_mahasiswa(
                nim,
                "DITERIMA"
            )

        else:
            update_status_mahasiswa(
                nim,
                "DITOLAK"
            )


    data_baru = ambil_semua_mahasiswa()


    return render_template(
        "admin.html",
        data=data_baru
    )

@app.route("/admin/laporan")
def admin_laporan():

    data = ambil_top_10_skor()

    return render_template(
        "laporan.html",
        total_pendaftar=hitung_total_pendaftar(),
        total_diterima=hitung_total_diterima(),
        total_ditolak=hitung_total_ditolak(),
        rata_ipk=hitung_rata_rata_ipk(),
        top10=data
    )

if __name__ == "__main__":
    app.run(debug=True)