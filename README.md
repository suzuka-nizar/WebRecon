# Web Recon Tool — Inspect Header & IDOR Scanner

Tool sederhana berbasis Python untuk keperluan **reconnaissance** dan **pengujian keamanan web** secara dasar. Tool ini menyediakan dua metode/menu yang bisa dipilih user saat dijalankan.

> ⚠️ **Disclaimer**
> Tool ini dibuat untuk tujuan edukasi dan pengujian keamanan pada sistem/aset **milik sendiri** atau yang **memiliki izin eksplisit** (misalnya melalui program bug bounty resmi). Menjalankan tool ini terhadap sistem pihak lain tanpa izin adalah pelanggaran hukum di banyak negara (termasuk UU ITE di Indonesia). Penulis tidak bertanggung jawab atas penyalahgunaan tool ini.

---

## Daftar Isi
- [Metode yang Tersedia](#metode-yang-tersedia)
- [Requirement](#requirement)
- [Instalasi & Menjalankan](#instalasi--menjalankan)
  - [Windows](#windows)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Android (Termux)](#android-termux)
- [Struktur File](#struktur-file)

---

## Metode yang Tersedia

### 1. Inspect Header
Mengirim HTTP GET request ke URL target, lalu menampilkan seluruh **HTTP response header** yang dikembalikan server. Berguna untuk reconnaissance awal, misalnya mendeteksi:
- Versi/tipe web server yang digunakan (header `Server`)
- Header keamanan yang hilang (`X-Frame-Options`, `Content-Security-Policy`, dll — bisa dicek manual dari output)
- Teknologi backend yang bocor lewat header custom

**Cara kerja:** kirim request → tangkap `response.headers` → loop dan cetak setiap pasangan key-value.

### 2. IDOR (Insecure Direct Object Reference) Scanner
Menguji apakah suatu endpoint yang menerima parameter ID (misalnya `?id=` atau `/user/123`) bisa diakses dengan mengganti nilai ID secara berurutan/acak — mengindikasikan kemungkinan celah **IDOR**, yaitu ketika sistem tidak memverifikasi kepemilikan/otorisasi data berdasarkan ID yang diminta.

**Cara kerja:** user memasukkan base URL + daftar ID (dipisah koma) → tool menyusun endpoint untuk setiap ID → menandai jika ID sensitif seperti `admin`/`root` ditemukan dapat diakses.

> Catatan: versi ini masih tahap dasar (belum memverifikasi status code/response body untuk memastikan akses benar-benar berhasil). Cocok untuk dikembangkan lebih lanjut.

---

## Requirement
- Python **3.7+**
- Library `requests`

---

## Instalasi & Menjalankan

### Windows
1. Install Python dari [python.org](https://www.python.org/downloads/) (centang **"Add Python to PATH"** saat instalasi).
2. Clone atau download repo ini:
   ```bash
   git clone https://github.com/USERNAME/NAMA-REPO.git
   cd NAMA-REPO
   ```
3. Install dependency:
   ```bash
   pip install requests
   ```
4. Jalankan:
   ```bash
   python script.py
   ```

### Linux
1. Pastikan Python sudah terinstal (biasanya sudah bawaan distro):
   ```bash
   python3 --version
   ```
2. Clone repo:
   ```bash
   git clone https://github.com/suzuka-nizar/WebRecon.git
   cd WebRecon
   ```
3. Install dependency:
   ```bash
   pip3 install requests
   ```
4. Jalankan:
   ```bash
   python3 script.py
   ```

### macOS
1. Pastikan Python 3 terinstal (bisa lewat [python.org](https://www.python.org/downloads/) atau Homebrew: `brew install python`).
2. Clone repo:
   ```bash
   git clone https://github.com/suzuka-nizar/WebRecon.git
   cd WebRecon
   ```
3. Install dependency:
   ```bash
   pip3 install requests
   ```
4. Jalankan:
   ```bash
   python3 script.py
   ```

### Android (Termux)
1. Install [Termux](https://f-droid.org/en/packages/com.termux/) dari F-Droid (disarankan, bukan Play Store karena versi lama).
2. Update paket & install Python + git:
   ```bash
   pkg update && pkg upgrade
   pkg install python git -y
   ```
3. Clone repo:
   ```bash
   git clone https://github.com/suzuka-nizar/WebRecon.git
   cd NAMA-REPO
   ```
4. Install dependency:
   ```bash
   pip install requests
   ```
5. Jalankan:
   ```bash
   python script.py
   ```

## Struktur File
```
.
├── script.py       # Script utama (gabungan kedua metode)
└── README.md     # Dokumentasi ini
```

---
