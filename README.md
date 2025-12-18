# README - Proyek ETL Pipeline Fashion Studio

## Deskripsi Proyek
Proyek ini adalah implementasi ETL (Extract, Transform, Load) Pipeline sederhana yang mengambil data produk fashion dari website https://fashion-studio.dicoding.dev/, membersihkan dan mentransformasi data, kemudian menyimpannya ke berbagai repositori data.

## Fitur Utama
- ✅ Web scraping dari 50 halaman website (~1000 produk)
- ✅ Data cleaning dan transformasi (hapus duplikat, null, invalid data)
- ✅ Konversi harga USD ke Rupiah
- ✅ Timestamp untuk setiap ekstraksi
- ✅ Error handling di setiap fungsi
- ✅ Simpan ke CSV dan Google Sheets
- ✅ Unit testing dengan coverage >80%
- ✅ Modular code structure

## Struktur Proyek
```
submission-pemda/
├── tests/
│   ├── test_extract.py      # Unit test untuk ekstraksi
│   ├── test_transform.py    # Unit test untuk transformasi
│   └── test_load.py         # Unit test untuk loading
├── utils/
│   ├── extract.py           # Modul ekstraksi data
│   ├── transform.py         # Modul transformasi data
│   └── load.py              # Modul loading data
├── main.py                  # Script utama
├── requirements.txt         # Dependencies
├── submission.txt           # Instruksi lengkap
└── README.md               # File ini
```

## Instalasi

1. Clone atau extract project ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan

### Menjalankan ETL Pipeline
```bash
python main.py
```

### Menjalankan Unit Test
```bash
# Semua test
pytest tests/

# Test spesifik
pytest tests/test_extract.py

# Dengan verbose
pytest tests/ -v
```

### Menjalankan Test Coverage
```bash
# Dengan pytest-cov
pytest tests/ --cov=utils --cov-report=term-missing

# Dengan coverage
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report
```

## Konfigurasi

### Google Sheets
File `google-sheets-api.json` sudah tersedia. Pastikan:
1. Service account memiliki akses Google Sheets API dan Google Drive API
2. File JSON berada di root folder proyek
3. Spreadsheet akan otomatis dibuat dengan permission "Anyone with the link" sebagai Editor
4. URL Google Sheets akan ditampilkan di console setelah ETL selesai

## Data Output

### Format Data
- **Title**: String - Nama produk
- **Price**: Float - Harga dalam Rupiah
- **Rating**: Float - Rating produk (0-5)
- **Colors**: Integer - Jumlah warna tersedia
- **Size**: String - Ukuran produk
- **Gender**: String - Target gender (Male/Female/Unisex)
- **timestamp**: String - Waktu ekstraksi

### Contoh Data
```
Title,Price,Rating,Colors,Size,Gender,timestamp
Casual T-Shirt,800000.0,4.5,3,"M, L, XL",Male,2025-12-18 10:30:00
Summer Dress,1200000.0,4.8,5,"S, M, L",Female,2025-12-18 10:30:00
```

## Testing

Project ini memiliki comprehensive unit tests dengan coverage target >80%:
- `test_extract.py`: Test untuk web scraping dan ekstraksi
- `test_transform.py`: Test untuk data cleaning dan transformasi
- `test_load.py`: Test untuk loading ke berbagai repositori

## Error Handling

Setiap fungsi utama dilengkapi dengan error handling:
- Request timeout saat scraping
- Data parsing error
- File I/O error
- Database connection error
- Google Sheets API error

## Kriteria Submission

### ✅ Kriteria 1: ETL Pipeline Modular (Advanced - 4 pts)
- Kode terpisah dalam file berbeda (extract.py, transform.py, load.py)
- Scraping dari 50 halaman website
- Konversi harga ke Rupiah (Rp16.000)
- Hapus duplikat, null, dan invalid data
- Timestamp untuk setiap ekstraksi
- Error handling di setiap fungsi

### ✅ Kriteria 2: Repositori Data (Skilled - 3 pts)
- Simpan ke CSV
- Simpan ke Google Sheets dengan permission "Anyone with link" sebagai Editor

### ✅ Kriteria 3: Unit Testing (Advanced - 4 pts)
- Unit test untuk semua modul
- Test coverage target >80%
- Semua test dalam folder `tests/`

## Troubleshooting

**Error saat scraping:**
- Pastikan koneksi internet stabil
- Website mungkin sedang maintenance

**Error Google Sheets:**
- Cek file google-sheets-api.json ada dan valid
- Pastikan API sudah dienable di Google Cloud Console
- Pastikan service account memiliki permission yang benar

**Error PostgreSQL:**
- PostgreSQL tidak digunakan dalam proyek ini

**Test gagal:**
- Pastikan semua dependencies terinstall
- Jalankan `pip install -r requirements.txt` lagi

## Lisensi
Project ini dibuat untuk submission Dicoding - Kelas Data Engineering

## Author
Submission untuk Kelas Data Engineering - Dicoding Indonesia
