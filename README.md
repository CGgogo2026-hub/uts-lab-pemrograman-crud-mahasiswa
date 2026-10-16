# Sistem Data Mahasiswa

Program ini dibuat untuk memenuhi tugas UTS Lab Pemrograman. Aplikasi digunakan untuk mengelola data mahasiswa melalui halaman web menggunakan Python, Flask, dan SQLite.

## Fitur Aplikasi

Beberapa fitur yang tersedia:

- Menambahkan data mahasiswa.
- Melihat daftar dan detail mahasiswa.
- Mengubah data mahasiswa yang sudah tersimpan.
- Menghapus data mahasiswa.
- Menghitung lama studi secara otomatis berdasarkan tahun angkatan.
- Menyimpan data menggunakan database SQLite agar tetap tersedia setelah aplikasi dijalankan ulang.

## Data yang Dikelola

Setiap data mahasiswa terdiri dari:

| Kolom | Keterangan |
|---|---|
| NIM | Nomor induk mahasiswa dan harus unik |
| Nama | Nama mahasiswa |
| Program Studi | Program studi mahasiswa |
| Angkatan | Tahun masuk mahasiswa |
| IPK | Nilai IPK dari 0,00 sampai 4,00 |
| Lama Studi | Dihitung dari tahun sekarang dikurangi tahun angkatan |

Kolom nama, program studi, angkatan, dan NIM harus diisi. NIM yang sama tidak dapat digunakan untuk dua data mahasiswa.

## Teknologi

- Python
- Flask
- SQLite
- HTML dan CSS

## Cara Menjalankan Aplikasi

Langkah berikut menggunakan Windows dan terminal Command Prompt di VS Code.

1. Pastikan Python sudah terpasang.
2. Buka folder proyek di VS Code.
3. Buka terminal melalui menu **Terminal → New Terminal**.
4. Jalankan perintah berikut secara berurutan:

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py app.py
```

5. Setelah server berjalan, buka browser dan akses:

```text
http://127.0.0.1:5000
```

Aplikasi dapat digunakan selama server Flask masih berjalan. Untuk menghentikannya, tekan `Ctrl + C` pada terminal.

## Penyimpanan Data

Data disimpan dalam file `mahasiswa.db` di folder proyek. File database dibuat otomatis ketika aplikasi dijalankan.

Jika ingin mempertahankan data yang sudah dimasukkan, jangan menghapus file `mahasiswa.db`. File tersebut juga tidak disertakan dalam repository GitHub.

## Pengujian

Beberapa hal yang dapat diuji saat menggunakan aplikasi:

- Menambahkan data mahasiswa baru.
- Membuka detail dan mengubah data mahasiswa.
- Menghapus data mahasiswa.
- Memasukkan NIM yang sudah digunakan.
- Mengosongkan kolom wajib atau memasukkan IPK di luar rentang yang diperbolehkan.
- Mematikan dan menjalankan kembali server untuk memastikan data tetap tersimpan.
