# MONITORING UDARA JAKARTA
Tim Pengembang
1. Lely Hiryanto ST., M.Sc.,PH.D
2. Janson Hendryli S.Kom. M.KOM
3. Valeroy Putra Sientika / 535220151

## Latar Belakang

Kota DKI Jakarta merupakan salah satu kota yang memiliki aktivitas sosial terbesar di Indonesia. Pada kota Jakarta, pencemaran udara merupakan salah satu masalah yang dihadapi sehari-hari. Pencemaran udara yang tinggi dapat berdampak pada kesehatan masyarakat dan kualitas hidup. Untuk itu, diperlukan sistem monitoring yang komprehensif dan dapat diakses oleh masyarakat. Sistem ini dikembangkan untuk meningkatkan kualitas hidup warga.

Pada proyek ini dikembangkan sebuah sistem prediksi kualitas udara berbasis web dengan menerapkan metode **Multivariate Singular Spectrum Analysis (MSSA)**. Metode MSSA digunakan untuk menangkap pola, tren, dan hubungan antar variabel pada data polutan dan meteorologi, sehingga diharapkan mampu menghasilkan prediksi kualitas udara yang lebih representatif.

---

## Tujuan

Tujuan dari pengembangan sistem ini adalah:
1. Menghasilkan sebuah sistem yang mampu memberikan prediksi kondisi kualitas udara dengan akurasi yang terukur melalui evaluasi menggunakan metrik statistik
2. Menyajikan hasil prediksi dalam bentuk informasi yang jelas, interaktif, dan mudah dipahami
3. Menyediakan sistem prediksi kualitas udara yang menyajikan informasi secara jelas dan mudah dipahami.
4. Menyumbang kontribusi dalam pengembangan metode analisis deret waktu multivariat pada bidang lingkungan.

---

## Cara Penggunaan

### 1. Import Github
Lakukan import github dengan melakukan :
```bash
git clone https://github.com/valeroy51/Website-Monitoring-Udara-Jakarta
```

### 2. Persiapan Environment
Pastikan Python dan Node.js telah terpasang, kemudian install dependency Python:
```bash
pip install -r requirements.txt
```

### 3. Instalasi Node.js dan npm untuk Tailwind
Dikarenakan sistem ini menggunakan Tailwind CSS maka diperlukan Node.js dan npm.
### a. Cek apakah npm sudah terpasang
```bash
npm --version
```
Jika perintah di atas tidak dikenali, maka Node.js dan npm belum terpasang.
### b. Instal Node.js
```bash
https://nodejs.org/
```
Instalasi Node.js akan otomatis menyertakan npm.

### 4. Konfigurasi Environment
Salin file `.env.example` menjadi `.env`, lalu sesuaikan isinya dengan konfigurasi lokal (SECRET_KEY dan database).

### 5. Setup Awal (First Time)
Jalankan script berikut untuk setup pertama kali:
```bash
python "Start Website First Time.py"
```

### 6. Menjalankan Aplikasi
Jalankan aplikasi Django dengan perintah:
```bash
python manage.py runserver
```

Jika menggunakan Tailwind CSS dalam mode development:
```bash
python manage.py tailwind dev
```

atau dengan mengaktifkan keduanya dengan menjalankan program:
```bash
python "Start Website.py"
```

dapat juga dengan menjalankan perintah:
```bash
python manage.py tailwind dev
```

### 7. Akses Website
Buka browser dan akses:
```
http://127.0.0.1:8000/
```

---

## Catatan
Sistem ini dikembangkan untuk keperluan akademik. Dataset input disediakan dalam format file Excel, sedangkan data hasil preprocessing dan output prediksi tidak disertakan dalam repository.