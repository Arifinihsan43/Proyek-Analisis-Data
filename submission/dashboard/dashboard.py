import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# Konfigurasi Halaman Streamlit
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling tema visualisasi seaborn
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# ==========================================
# Memuat Data (Caching untuk Performa Cepat)
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "main_data.csv"),
        "main_data.csv",
        "dashboard/main_data.csv",
        "submission/dashboard/main_data.csv"
    ]
    data_path = next((p for p in candidates if os.path.exists(p)), None)
    
    if data_path is None:
        st.error("File main_data.csv tidak ditemukan!")
        st.stop()
        
    df = pd.read_csv(data_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# ==========================================
# Sidebar Filter
# ==========================================
with st.sidebar:
    st.title("🚲 Bike Sharing System")
    st.markdown("Dashboard Analisis Permintaan & Operasional Sewa Sepeda")
    st.markdown("---")
    
    # 1. Filter Rentang Tanggal
    min_date = df['dteday'].min().date()
    max_date = df['dteday'].max().date()
    
    st.subheader("📅 Filter Periode Tanggal")
    date_range = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Penanganan rentang tanggal
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_date, max_date
        
    # 2. Filter Musim
    all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    selected_seasons = st.multiselect(
        label="🌦️ Filter Musim (Season)",
        options=all_seasons,
        default=all_seasons
    )
    if not selected_seasons:
        selected_seasons = all_seasons
        
    # 3. Filter Kondisi Cuaca
    all_weathers = [
        'Clear/Partly Cloudy',
        'Misty/Cloudy',
        'Light Snow/Rain',
        'Severe Weather/Heavy Rain'
    ]
    available_weathers = [w for w in all_weathers if w in df['weather_label'].unique()]
    selected_weathers = st.multiselect(
        label="☁️ Filter Kondisi Cuaca",
        options=available_weathers,
        default=available_weathers
    )
    if not selected_weathers:
        selected_weathers = available_weathers
        
    # 4. Filter Tipe Hari
    day_type_option = st.selectbox(
        label="🗓️ Filter Tipe Hari",
        options=['Semua Tipe Hari', 'Hari Kerja (Working Day)', 'Akhir Pekan / Libur']
    )
    
    st.markdown("---")
    st.markdown("**Profil Pengembang:**")
    st.markdown("- **Nama:** Arifin Ihsan Nugroho")
    st.markdown("- **ID Dicoding:** `DS183B6Y0241`")
    st.markdown("- **Program:** Asah 2026 - Hard Skill")

# ==========================================
# Menerapkan Filter pada Data
# ==========================================
filtered_df = df[
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date) &
    (df['season_label'].isin(selected_seasons)) &
    (df['weather_label'].isin(selected_weathers))
]

if day_type_option == 'Hari Kerja (Working Day)':
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif day_type_option == 'Akhir Pekan / Libur':
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# Jika filter menghasilkan data kosong
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan sesuaikan kembali filter.")
    st.stop()

# ==========================================
# Header Utama
# ==========================================
st.title("🚲 Bike Sharing Demand & Operational Dashboard")
st.markdown(
    f"Menampilkan ringkasan data operasional dari **{start_date.strftime('%d %B %Y')}** hingga **{end_date.strftime('%d %B %Y')}**."
)

# ==========================================
# Ringkasan Metrik KPI
# ==========================================
st.subheader("📊 Key Performance Indicators (KPI)")
col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_df['cnt'].sum()
total_registered = filtered_df['registered'].sum()
total_casual = filtered_df['casual'].sum()

reg_pct = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
cas_pct = (total_casual / total_rentals * 100) if total_rentals > 0 else 0

# Hitung jumlah hari unik yang terfilter
unique_days = filtered_df['dteday'].dt.date.nunique()
daily_avg = (total_rentals / unique_days) if unique_days > 0 else 0

with col1:
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,} unit")
with col2:
    st.metric(label="Pengguna Terdaftar (Registered)", value=f"{total_registered:,} unit", delta=f"{reg_pct:.1f}%")
with col3:
    st.metric(label="Pengguna Kasual (Casual)", value=f"{total_casual:,} unit", delta=f"{cas_pct:.1f}%")
with col4:
    st.metric(label="Rata-rata Sewa per Hari", value=f"{int(daily_avg):,} unit/hari")

st.markdown("---")

# ==========================================
# Visualisasi 1: Tren Harian Penyewaan Sepeda
# ==========================================
st.subheader("📈 Tren Harian Penyewaan Sepeda")
daily_trend = filtered_df.groupby('dteday')[['cnt', 'casual', 'registered']].sum().reset_index()

fig_trend, ax_trend = plt.subplots(figsize=(14, 4.5))
ax_trend.plot(daily_trend['dteday'], daily_trend['cnt'], label='Total Penyewaan', color='#2A9D8F', linewidth=2)
ax_trend.plot(daily_trend['dteday'], daily_trend['registered'], label='Registered', color='#1D3557', linestyle='--', alpha=0.7)
ax_trend.plot(daily_trend['dteday'], daily_trend['casual'], label='Casual', color='#E76F51', linestyle=':', alpha=0.7)
ax_trend.set_title('Fluktuasi Volume Penyewaan Sepeda dari Waktu ke Waktu', fontsize=13, fontweight='bold', pad=10)
ax_trend.set_xlabel('Tanggal', fontsize=11)
ax_trend.set_ylabel('Total Penyewaan (Unit)', fontsize=11)
ax_trend.legend(loc='upper left', frameon=True)
plt.tight_layout()
st.pyplot(fig_trend)

st.markdown("---")

# ==========================================
# Visualisasi 2: Menjawab Pertanyaan Bisnis 1 (Musim & Cuaca)
# ==========================================
st.subheader("🌦️ Pertanyaan 1: Pengaruh Musim & Kondisi Cuaca terhadap Penyewaan")

col_m1, col_m2 = st.columns(2)

with col_m1:
    # Agregasi data per musim
    season_stats = filtered_df.groupby('season_label')['cnt'].agg(
        rata_rata='mean'
    ).reindex([s for s in ['Spring', 'Summer', 'Fall', 'Winter'] if s in filtered_df['season_label'].unique()]).reset_index()
    
    fig_season, ax_season = plt.subplots(figsize=(7, 4.5))
    season_colors = {'Spring': '#A8D5BA', 'Summer': '#F7B267', 'Fall': '#E76F51', 'Winter': '#457B9D'}
    palette_s = [season_colors.get(s, '#2A9D8F') for s in season_stats['season_label']]
    
    sns.barplot(data=season_stats, x='season_label', y='rata_rata', palette=palette_s, ax=ax_season)
    ax_season.set_title('Rata-rata Penyewaan per Jam Berdasarkan Musim', fontsize=12, fontweight='bold')
    ax_season.set_xlabel('Musim (Season)', fontsize=10)
    ax_season.set_ylabel('Rata-rata Sewa per Jam (Unit)', fontsize=10)
    
    for p in ax_season.patches:
        val = int(p.get_height())
        ax_season.annotate(f'{val} unit', (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='bottom', fontsize=9, fontweight='semibold', xytext=(0, 4), textcoords='offset points')
    plt.tight_layout()
    st.pyplot(fig_season)

with col_m2:
    # Agregasi data per kondisi cuaca
    weather_stats = filtered_df.groupby('weather_label')['cnt'].agg(
        rata_rata='mean'
    ).reset_index().sort_values(by='rata_rata', ascending=False)
    
    fig_weather, ax_weather = plt.subplots(figsize=(7, 4.5))
    weather_colors = {
        'Clear/Partly Cloudy': '#2A9D8F',
        'Misty/Cloudy': '#E9C46A',
        'Light Snow/Rain': '#E63946',
        'Severe Weather/Heavy Rain': '#6c757d'
    }
    palette_w = [weather_colors.get(w, '#2A9D8F') for w in weather_stats['weather_label']]
    
    sns.barplot(data=weather_stats, x='weather_label', y='rata_rata', palette=palette_w, ax=ax_weather)
    ax_weather.set_title('Rata-rata Penyewaan per Jam Berdasarkan Kondisi Cuaca', fontsize=12, fontweight='bold')
    ax_weather.set_xlabel('Kondisi Cuaca (Weather)', fontsize=10)
    ax_weather.set_ylabel('Rata-rata Sewa per Jam (Unit)', fontsize=10)
    ax_weather.tick_params(axis='x', rotation=12)
    
    for p in ax_weather.patches:
        val = int(p.get_height())
        ax_weather.annotate(f'{val} unit', (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='bottom', fontsize=9, fontweight='semibold', xytext=(0, 4), textcoords='offset points')
    plt.tight_layout()
    st.pyplot(fig_weather)

st.info(
    "💡 **Insight Pertanyaan 1:**\n"
    "- **Musim Gugur (Fall)** mencatatkan permintaan penyewaan tertinggi, disusul oleh **Musim Panas (Summer)**.\n"
    "- Cuaca **Cerah (Clear/Partly Cloudy)** memberikan kontribusi terbesar. Ketika cuaca berubah menjadi **Hujan/Salju (Light Snow/Rain)**, volume penyewaan mengalami penurunan drastis hingga lebih dari 60%."
)

st.markdown("---")

# ==========================================
# Visualisasi 3: Menjawab Pertanyaan Bisnis 2 (Pola Jam & Tipe Pengguna)
# ==========================================
st.subheader("⏰ Pertanyaan 2: Pola Jam Sibuk & Perilaku Pengguna (Hari Kerja vs Akhir Pekan)")

col_h1, col_h2 = st.columns(2)

hourly_working = filtered_df[filtered_df['workingday'] == 1].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
hourly_weekend = filtered_df[filtered_df['workingday'] == 0].groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()

with col_h1:
    fig_w1, ax_w1 = plt.subplots(figsize=(7.5, 4.5))
    if not hourly_working.empty:
        ax_w1.plot(hourly_working['hr'], hourly_working['registered'], marker='o', color='#1D3557', label='Registered', linewidth=2.2)
        ax_w1.plot(hourly_working['hr'], hourly_working['casual'], marker='s', color='#E76F51', label='Casual', linestyle='--', linewidth=1.8)
        ax_w1.plot(hourly_working['hr'], hourly_working['cnt'], marker='^', color='#2A9D8F', label='Total', linestyle=':', linewidth=1.8)
        ax_w1.set_title('Hari Kerja (Working Day): Pola Komuter', fontsize=12, fontweight='bold')
        ax_w1.set_xlabel('Jam (0 - 23)', fontsize=10)
        ax_w1.set_ylabel('Rata-rata Penyewaan (Unit)', fontsize=10)
        ax_w1.set_xticks(range(0, 24, 2))
        ax_w1.axvspan(7.5, 9, color='#1D3557', alpha=0.1, label='Jam Sibuk Pagi')
        ax_w1.axvspan(16.5, 18.5, color='#E76F51', alpha=0.1, label='Jam Sibuk Sore')
        ax_w1.legend(loc='upper right', fontsize=8.5)
    else:
        ax_w1.text(0.5, 0.5, 'Tidak ada data Hari Kerja terpilih', ha='center', va='center')
    plt.tight_layout()
    st.pyplot(fig_w1)

with col_h2:
    fig_w2, ax_w2 = plt.subplots(figsize=(7.5, 4.5))
    if not hourly_weekend.empty:
        ax_w2.plot(hourly_weekend['hr'], hourly_weekend['registered'], marker='o', color='#1D3557', label='Registered', linewidth=2.2)
        ax_w2.plot(hourly_weekend['hr'], hourly_weekend['casual'], marker='s', color='#E76F51', label='Casual', linestyle='--', linewidth=1.8)
        ax_w2.plot(hourly_weekend['hr'], hourly_weekend['cnt'], marker='^', color='#2A9D8F', label='Total', linestyle=':', linewidth=1.8)
        ax_w2.set_title('Akhir Pekan & Libur: Pola Santai / Rekreasi', fontsize=12, fontweight='bold')
        ax_w2.set_xlabel('Jam (0 - 23)', fontsize=10)
        ax_w2.set_ylabel('Rata-rata Penyewaan (Unit)', fontsize=10)
        ax_w2.set_xticks(range(0, 24, 2))
        ax_w2.axvspan(11.5, 15.5, color='#F4A261', alpha=0.15, label='Puncak Siang')
        ax_w2.legend(loc='upper right', fontsize=8.5)
    else:
        ax_w2.text(0.5, 0.5, 'Tidak ada data Akhir Pekan terpilih', ha='center', va='center')
    plt.tight_layout()
    st.pyplot(fig_w2)

st.info(
    "💡 **Insight Pertanyaan 2:**\n"
    "- **Hari Kerja:** Memiliki dua puncak jam sibuk (*bimodal*) pada pukul **08:00** dan **17:00–18:00**, yang didominasi oleh pengguna terdaftar (*registered*) untuk aktivitas perjalanan kerja/sekolah.\n"
    "- **Akhir Pekan & Hari Libur:** Memiliki kurva santai (*unimodal*) dengan puncak penggunaan pada siang hari (pukul **12:00–15:00**), di mana pengguna kasual (*casual*) melonjak tajam untuk kebutuhan rekreasi."
)

st.markdown("---")

# ==========================================
# Visualisasi 4: Segmentasi Waktu (Dayparting)
# ==========================================
st.subheader("🌓 Analisis Segmentasi Waktu Harian (Dayparting)")

segment_order = [
    'Dini Hari (00:00 - 05:59)',
    'Pagi (06:00 - 10:59)',
    'Siang (11:00 - 14:59)',
    'Sore (15:00 - 18:59)',
    'Malam (19:00 - 23:59)'
]

segment_df = filtered_df.groupby('time_segment').agg(
    total_casual=('casual', 'sum'),
    total_registered=('registered', 'sum'),
    total_cnt=('cnt', 'sum'),
    rata_rata_per_jam=('cnt', 'mean')
).reindex([s for s in segment_order if s in filtered_df['time_segment'].unique()]).reset_index()

fig_seg, ax_seg = plt.subplots(figsize=(10, 4.5))
x_indices = np.arange(len(segment_df))
b_width = 0.5

ax_seg.bar(x_indices, segment_df['total_registered'], width=b_width, label='Registered', color='#1D3557')
ax_seg.bar(x_indices, segment_df['total_casual'], bottom=segment_df['total_registered'], width=b_width, label='Casual', color='#E76F51')
ax_seg.set_title('Distribusi Total Penyewaan Berdasarkan Segmen Waktu', fontsize=12, fontweight='bold')
ax_seg.set_xlabel('Segmen Waktu', fontsize=10)
ax_seg.set_ylabel('Total Unit Sewa', fontsize=10)
ax_seg.set_xticks(x_indices)
ax_seg.set_xticklabels(segment_df['time_segment'], fontsize=9, rotation=10)
ax_seg.legend(loc='upper left', frameon=True)

for i, tot in enumerate(segment_df['total_cnt']):
    ax_seg.annotate(f'{tot:,} unit', (x_indices[i], tot), ha='center', va='bottom', fontsize=8.5, fontweight='semibold', xytext=(0, 3), textcoords='offset points')

plt.tight_layout()
st.pyplot(fig_seg)

st.markdown("---")

# ==========================================
# Sampel Data & Fitur Unduh CSV
# ==========================================
with st.expander("🔍 Lihat Sampel Data yang Telah Difilter (100 Baris Pertama)"):
    st.dataframe(filtered_df.head(100))
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Hasil Filter (CSV)",
        data=csv_data,
        file_name="filtered_bike_sharing_data.csv",
        mime="text/csv"
    )

st.caption("© 2026 Arifin Ihsan Nugroho | Dicoding Proyek Analisis Data - Bike Sharing Dataset")

