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
├── Proyek_Analisis_Data.ipynb
├── README.md                # Panduan instruksi proyek & dashboard
├── requirements.txt         # Daftar pustaka dependensi Python
└── url.txt                  # Tautan URL deployment Streamlit Cloud
``````

---

## 📌 Pertanyaan Bisnis yang Dianalisis
1. **Pertanyaan 1:** Bagaimana pengaruh pergantian musim (*season*) dan kondisi cuaca (*weather situation*) terhadap rata-rata jumlah penyewaan sepeda harian (*cnt*) pada periode 2011–2012?
2. **Pertanyaan 2:** Bagaimana perbedaan pola penyewaan sepeda per jam (*hour*) antara hari kerja (*working day*) dan akhir pekan/hari libur (*weekend/holiday*), serta bagaimana karakteristik pengguna kasual (*casual*) dibandingkan pengguna terdaftar (*registered*)?

---

## 🚀 Panduan Menjalankan Proyek

### 1. Menyiapkan Lingkungan (Environment)
Pastikan Anda telah memasang **Python 3.9+** pada sistem Anda. Sangat disarankan menggunakan virtual environment:

```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Pada Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Pada Windows (Command Prompt):
.\venv\Scripts\activate.bat
# Pada macOS / Linux:
source venv/bin/activate
```

### 2. Memasang Dependensi
Pasang semua pustaka yang dibutuhkan menggunakan file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Jupyter Notebook
Untuk melihat atau menjalankan kembali seluruh tahapan analisis data:
```bash
jupyter notebook notebook.ipynb
# atau buka langsung file notebook.ipynb / Proyek_Analisis_Data.ipynb di VS Code
```

### 4. Menjalankan Dashboard Interaktif (Streamlit)
Jalankan perintah berikut pada terminal dari direktori `submission/` (atau direktori root proyek):

```bash
streamlit run dashboard/dashboard.py
```
atau jika berada di dalam folder `dashboard/`:
```bash
cd dashboard
streamlit run dashboard.py
```
Aplikasi dashboard akan terbuka secara otomatis pada peramban web (*browser*) Anda di alamat `http://localhost:8501`.

---

## 🌐 Tautan Dashboard Online
Dashboard telah siap untuk dideploy ke **Streamlit Community Cloud**. Tautan publik dashboard dapat dicek pada file `url.txt`.

