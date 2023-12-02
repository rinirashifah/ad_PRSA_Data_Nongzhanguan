# app.py
import streamlit as st
import pandas as pd
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

# Extracting file ID from Google Drive link
file_id = "1BmjD8cxHqTxpLlNr6KWDmRDkp3h14D7R"
file_path = f"https://drive.google.com/uc?id={file_id}"
df = pd.read_csv(file_path)

# Sidebar
st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Start Date", df["time"].min())
end_date = st.sidebar.date_input("End Date", df["time"].max())

# Filter data based on date range
filtered_data = df[(df["time"] >= str(start_date)) & (df["time"] <= str(end_date))]

# Main content
st.title("Air Quality Analysis Dashboard")

# Pertanyaan 1: Hubungan antara PM2.5 dan Suhu
st.subheader("Pertanyaan 1: Hubungan antara PM2.5 dan Suhu")
plt.figure(figsize=(12, 8))
sns.regplot(x='TEMP', y='PM2.5', data=filtered_data, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
plt.title('Hubungan antara PM2.5 dan Suhu')
plt.xlabel('Suhu (Celsius)')
plt.ylabel('PM2.5')
st.pyplot()

# Pertanyaan 2: Perbedaan Tingkat Polusi Udara antara Jam dalam Sehari
st.subheader("Pertanyaan 2: Perbedaan Tingkat Polusi Udara antara Jam dalam Sehari")
# Menampilkan distribusi tingkat polusi udara berdasarkan jam
plt.figure(figsize=(12, 8))
sns.boxplot(x='hour', y='PM2.5', data=filtered_data)
plt.title('Distribusi Tingkat Polusi Udara Berdasarkan Jam')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('PM2.5')
st.pyplot()

# Melakukan uji statistik ANOVA
hours = filtered_data['hour'].unique()
groups = [filtered_data[filtered_data['hour'] == hour]['PM2.5'] for hour in hours]
statistic, p_value = f_oneway(*groups)

# Menampilkan hasil uji statistik
st.write(f'Hasil Uji Statistik ANOVA: F = {statistic}, p-value = {p_value}')

# Menentukan apakah perbedaan signifikan (umumnya menggunakan alpha = 0.05)
alpha = 0.05
if p_value < alpha:
    st.write('Terdapat perbedaan yang signifikan dalam tingkat polusi udara antara jam-jam tertentu.')
else:
    st.write('Tidak terdapat perbedaan yang signifikan dalam tingkat polusi udara antara jam-jam tertentu.')

# Footer
st.sidebar.markdown("Created with Streamlit by Rini")
