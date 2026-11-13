# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan submission akhir untuk kelas **Belajar Analisis Data dengan Python** pada program pelatihan Dicoding Indonesia / Asah 2026. Proyek ini mencakup proses *Data Wrangling*, *Exploratory Data Analysis (EDA)*, visualisasi data berbasis kaidah *SMART questions*, hingga pembuatan dashboard interaktif berbasis **Streamlit**.

---

## 👤 Identitas
- **Nama:** Arifin Ihsan Nugroho
- **Email:** ds183b6y0241@student.devacademy.id
- **ID Dicoding:** DS183B6Y0241

---

## 📁 Struktur Direktori
```text
submission/
├── dashboard/
│   ├── main_data.csv        # Data agregasi bersih untuk dashboard
│   └── dashboard.py         # Skrip aplikasi dashboard Streamlit
├── data/
│   ├── data_1.csv           # Dataset harian (day.csv)
│   ├── data_2.csv           # Dataset per jam (hour.csv)
│   ├── day.csv              # File asli harian
│   └── hour.csv             # File asli per jam
├── notebook.ipynb           # Jupyter Notebook analisis data lengkap & tervalidasi
├── README.md                # Panduan instruksi proyek & dashboard
├── requirements.txt         # Daftar pustaka dependensi Python
└── url.txt                  # Tautan URL deployment Streamlit Cloud
```

---

## 📌 Pertanyaan Bisnis yang Dianalisis
1. **Pertanyaan 1:** Bagaimana pengaruh pergantian musim (*season*) dan kondisi cuaca (*weather situation*) terhadap rata-rata jumlah penyewaan sepeda harian (*cnt*) pada periode 2011–2012?
2. **Pertanyaan 2:** Bagaimana perbedaan pola penyewaan sepeda per jam (*hour*) antara hari kerja (*working day*) dan akhir pekan/hari libur (*weekend/holiday*), serta bagaimana karakteristik pengguna kasual (*casual*) dibandingkan pengguna terdaftar (*registered*)?

---

## 🚀 Panduan Menjalankan Proyek (Setup Environment)

### Setup Environment - Anaconda
```bash
conda create --name bike-sharing python=3.12
conda activate bike-sharing
pip install -r requirements.txt
```

### Setup Environment - Shell / Terminal (venv / pipenv)
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# Memasang dependensi
pip install -r requirements.txt
```

### Menjalankan Jupyter Notebook
Untuk meninjau proses analisis data:
```bash
jupyter notebook notebook.ipynb
```
*(Atau buka langsung file `notebook.ipynb` di VS Code / Google Colab)*.

### Menjalankan Dashboard Streamlit
Jalankan perintah berikut di terminal:
```bash
streamlit run dashboard/dashboard.py
```
atau jika berada di dalam folder `dashboard/`:
```bash
cd dashboard
streamlit run dashboard.py
```
Aplikasi dashboard akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

---

## 🌐 Tautan Dashboard Online
Tautan deployment dashboard dapat dicek pada berkas `url.txt`.
