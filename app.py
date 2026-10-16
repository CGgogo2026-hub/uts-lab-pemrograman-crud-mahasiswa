from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "ganti-dengan-kunci-rahasia-anda"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "mahasiswa.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            nim INTEGER PRIMARY KEY,
            nama TEXT NOT NULL,
            program_studi TEXT NOT NULL,
            angkatan INTEGER NOT NULL,
            ipk REAL NOT NULL CHECK (ipk >= 0 AND ipk <= 4)
        )
    """)
    return conn


def hitung_lama_studi(angkatan):
    return date.today().year - int(angkatan)


def validasi_form(form):
    nim_text = form.get("nim", "").strip()
    nama = form.get("nama", "").strip()
    program_studi = form.get("program_studi", "").strip()
    angkatan_text = form.get("angkatan", "").strip()
    ipk_text = form.get("ipk", "").strip()

    if not nim_text or not nama or not program_studi or not angkatan_text or not ipk_text:
        return None, "Semua kolom wajib diisi."

    try:
        nim = int(nim_text)
        angkatan = int(angkatan_text)
        ipk = float(ipk_text.replace(",", "."))
    except ValueError:
        return None, "NIM dan angkatan harus berupa bilangan bulat, sedangkan IPK harus berupa angka."

    if nim <= 0:
        return None, "NIM harus berupa bilangan bulat positif."
    if angkatan < 1900 or angkatan > date.today().year:
        return None, f"Angkatan harus berada di antara 1900 dan {date.today().year}."
    if not 0 <= ipk <= 4:
        return None, "IPK harus berada dalam rentang 0,00 sampai 4,00."

    return {
        "nim": nim,
        "nama": nama,
        "program_studi": program_studi,
        "angkatan": angkatan,
        "ipk": ipk,
    }, None


def mahasiswa_dengan_lama_studi(row):
    data = dict(row)
    data["lama_studi"] = hitung_lama_studi(data["angkatan"])
    return data


@app.route("/")
def index():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM mahasiswa ORDER BY nim").fetchall()
    conn.close()
    mahasiswa = [mahasiswa_dengan_lama_studi(row) for row in rows]
    return render_template("index.html", mahasiswa=mahasiswa, tahun_sekarang=date.today().year)


@app.route("/mahasiswa/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data, error = validasi_form(request.form)
        if error:
            flash(error, "error")
            return render_template("form.html", judul="Tambah Mahasiswa", mahasiswa=request.form, mode="tambah")

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO mahasiswa (nim, nama, program_studi, angkatan, ipk) VALUES (?, ?, ?, ?, ?)",
                (data["nim"], data["nama"], data["program_studi"], data["angkatan"], data["ipk"])
            )
            conn.commit()
            flash("Data mahasiswa berhasil ditambahkan.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("NIM sudah terdaftar. Gunakan NIM yang berbeda.", "error")
        finally:
            conn.close()
        return render_template("form.html", judul="Tambah Mahasiswa", mahasiswa=request.form, mode="tambah")

    return render_template("form.html", judul="Tambah Mahasiswa", mahasiswa={}, mode="tambah")


@app.route("/mahasiswa/<int:nim>")
def detail(nim):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    if row is None:
        flash("Data mahasiswa tidak ditemukan.", "error")
        return redirect(url_for("index"))
    mahasiswa = mahasiswa_dengan_lama_studi(row)
    return render_template("detail.html", mahasiswa=mahasiswa)


@app.route("/mahasiswa/<int:nim>/edit", methods=["GET", "POST"])
def edit(nim):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    if row is None:
        flash("Data mahasiswa tidak ditemukan.", "error")
        return redirect(url_for("index"))

    data_awal = dict(row)
    if request.method == "POST":
        data, error = validasi_form(request.form)
        if error:
            flash(error, "error")
            return render_template("form.html", judul="Ubah Data Mahasiswa", mahasiswa=request.form, mode="edit", nim_lama=nim)

        if data["nim"] != nim:
            conn = get_db_connection()
            existing = conn.execute("SELECT nim FROM mahasiswa WHERE nim = ?", (data["nim"],)).fetchone()
            conn.close()
            if existing:
                flash("NIM tersebut sudah digunakan mahasiswa lain.", "error")
                return render_template("form.html", judul="Ubah Data Mahasiswa", mahasiswa=request.form, mode="edit", nim_lama=nim)

        conn = get_db_connection()
        try:
            conn.execute(
                """UPDATE mahasiswa
                   SET nim = ?, nama = ?, program_studi = ?, angkatan = ?, ipk = ?
                   WHERE nim = ?""",
                (data["nim"], data["nama"], data["program_studi"], data["angkatan"], data["ipk"], nim)
            )
            conn.commit()
            flash("Data mahasiswa berhasil diperbarui.", "success")
            return redirect(url_for("detail", nim=data["nim"]))
        except sqlite3.IntegrityError:
            flash("NIM sudah digunakan. Gunakan NIM yang berbeda.", "error")
        finally:
            conn.close()
        return render_template("form.html", judul="Ubah Data Mahasiswa", mahasiswa=request.form, mode="edit", nim_lama=nim)

    return render_template("form.html", judul="Ubah Data Mahasiswa", mahasiswa=data_awal, mode="edit", nim_lama=nim)


@app.route("/mahasiswa/<int:nim>/hapus", methods=["POST"])
def hapus(nim):
    conn = get_db_connection()
    conn.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
    conn.commit()
    conn.close()
    flash("Data mahasiswa berhasil dihapus.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Database dan tabel dibuat otomatis saat aplikasi pertama kali dijalankan.
    get_db_connection().close()
    app.run(debug=True)
