# UTS Lab Pemrograman — Sistem Data Mahasiswa

Aplikasi CRUD mahasiswa menggunakan Python, Flask, SQLite, dan HTML/CSS.

## Fitur
- Menambah, melihat daftar/detail, mengubah, dan menghapus data mahasiswa.
- Validasi kolom wajib, IPK 0,00–4,00, dan NIM unik.
- Lama studi dihitung otomatis: tahun sekarang dikurangi angkatan.
- Database SQLite disimpan pada file `mahasiswa.db` di folder proyek.

## Cara menjalankan (Windows)
1. Pastikan Python sudah terpasang. Saat instalasi Python, centang **Add Python to PATH**.
2. Ekstrak folder proyek.
3. Buka folder proyek di VS Code.
4. Buka terminal di VS Code (`Terminal > New Terminal`).
5. Jalankan:

   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   py -m pip install -r requirements.txt
   py app.py
   ```

   Jika perintah `py` tidak tersedia, coba ganti `py` dengan `python`.

6. Buka browser dan akses `http://127.0.0.1:5000`.
7. Tambahkan data uji, lalu coba fitur detail, edit, hapus, validasi IPK, dan NIM duplikat.

## Catatan database
File `mahasiswa.db` dibuat otomatis saat aplikasi dijalankan. Jangan menghapus file tersebut jika ingin mempertahankan data yang sudah dimasukkan.

## Saran minimal 4 commit Git
1. `Initial project structure`
2. `Add SQLite database and student model`
3. `Implement CRUD routes and validation`
4. `Add responsive interface and documentation`

Buat commit secara bertahap sesuai perubahan yang benar-benar kamu lakukan. Jangan membuat commit palsu atau mengunggah database berisi data pribadi.
