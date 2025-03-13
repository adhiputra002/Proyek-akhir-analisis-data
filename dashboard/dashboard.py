import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set judul aplikasi
st.title("📊 Dashboard Analisis Data Polusi Udara")

# **Load dataset dengan cache**
@st.cache_data
def load_data():
    df = pd.read_csv("data/PRSA_Data_Nongzhanguan_20130301-20170228.csv")

    # Gabungkan kolom menjadi datetime
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')

    # Hapus baris dengan nilai NaN pada date
    df = df.dropna(subset=['date'])

    return df

df = load_data()

# **Sidebar untuk filter**
st.sidebar.header("🛠 Filter Data")
start_date = st.sidebar.date_input("Pilih tanggal mulai", df['date'].min().date())
end_date = st.sidebar.date_input("Pilih tanggal akhir", df['date'].max().date())

# **Filter data berdasarkan tanggal**
df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# **Tampilkan Data**
st.subheader("📄 Data Polusi Udara")
st.write(df_filtered.head() if not df_filtered.empty else "⚠ Tidak ada data yang sesuai dengan rentang tanggal yang dipilih.")

# **Visualisasi Tren Polusi**
if not df_filtered.empty:
    st.subheader("📈 Tren Polusi Udara")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_filtered['date'], df_filtered['PM2.5'], label="PM2.5", color='red', alpha=0.6)
    ax.plot(df_filtered['date'], df_filtered['PM10'], label="PM10", color='blue', alpha=0.6)

    # Format sumbu x agar lebih rapi
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    ax.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # **Insight Singkat**
    st.subheader("📌 Insight")
    st.write("- Polusi udara (PM2.5 dan PM10) cenderung meningkat pada musim dingin.")
    st.write("- Tren fluktuasi polusi udara menunjukkan adanya pengaruh musiman dan faktor lingkungan.")
else:
    st.warning("⚠ Tidak ada data untuk ditampilkan. Coba pilih rentang tanggal yang berbeda.")

# **Analisis Hubungan Curah Hujan dengan Polusi**
if not df_filtered.empty:
    st.subheader("🌧 Hubungan Curah Hujan dan Polusi Udara")

    # Scatter plot hubungan RAIN dengan masing-masing polutan
    polutan = ["PM2.5", "PM10", "NO2", "CO"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for ax, pol in zip(axes.flatten(), polutan):
        sns.scatterplot(data=df_filtered, x="RAIN", y=pol, alpha=0.5, ax=ax)
        ax.set_title(f"Curah Hujan vs {pol}")
        ax.set_xlabel("Curah Hujan (mm)")
        ax.set_ylabel(f"Konsentrasi {pol} (µg/m³)")

    plt.tight_layout()
    st.pyplot(fig)

    # **Korelasi antara Curah Hujan dan Polusi**
    st.subheader("📊 Korelasi Curah Hujan dan Polusi")
    correlation = df_filtered[["RAIN", "PM2.5", "PM10", "NO2", "CO"]].corr()
    st.write(correlation)

    # **Insight**
    st.subheader("📌 Insight Hubungan Curah Hujan dan Polusi")
    st.write("- Jika korelasi negatif: Curah hujan membantu menurunkan tingkat polusi.")
    st.write("- Jika korelasi mendekati nol: Tidak ada hubungan signifikan antara curah hujan dan polusi.")
else:
    st.warning("⚠ Tidak ada data yang cukup untuk analisis hubungan curah hujan dan polusi.")
