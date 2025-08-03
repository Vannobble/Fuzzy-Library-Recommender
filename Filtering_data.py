import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
#
# Definisi Variabel Fuzzy untuk mengetahui rentang nilai dari poin yang diperhitungkan as (Fuzzification)
rating = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'Rating')
minat = ctrl.Antecedent(np.arange(0, 11, 1), 'Minat')
rekomendasi = ctrl.Consequent(np.arange(0, 11, 1), 'Rekomendasi')

# Deklarasi nilai pengelompokan dari fuzzy 
rating['rendah'] = fuzz.trimf(rating.universe, [0, 0, 2.5])
rating['sedang'] = fuzz.trimf(rating.universe, [2, 3, 4])
rating['tinggi'] = fuzz.trimf(rating.universe, [3.5, 5, 5])

minat['rendah'] = fuzz.trimf(minat.universe, [0, 0, 5])
minat['sedang'] = fuzz.trimf(minat.universe, [3, 5, 7])
minat['tinggi'] = fuzz.trimf(minat.universe, [6, 10, 10])

rekomendasi['rendah'] = fuzz.trimf(rekomendasi.universe, [0, 0, 5])
rekomendasi['sedang'] = fuzz.trimf(rekomendasi.universe, [3, 5, 8])
rekomendasi['tinggi'] = fuzz.trimf(rekomendasi.universe, [6, 10, 10])

# Aturan fuzzy sebagai Rules Base (aturan if then untuk menentukan logika sistem)
rules = [
    ctrl.Rule(rating['tinggi'] & minat['tinggi'], rekomendasi['tinggi']),
    ctrl.Rule(rating['tinggi'] & minat['sedang'], rekomendasi['sedang']),
    ctrl.Rule(rating['sedang'] & minat['tinggi'], rekomendasi['sedang']),
    ctrl.Rule(rating['rendah'] | minat['rendah'], rekomendasi['rendah']),
]

# Otak dari proses inferensi fuzzy logic yang menggabungkan semua aturan fuzzy aktif dan melakukan perhitungan
rekomendasi_ctrl = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(rekomendasi_ctrl)

# Membaca dataset
df = pd.read_csv(r"C:\Users\acern\Hansel\Semester 4\Sistem Cerdas\filtered_data.csv")

# Input user ascrsip values(nilai yang tidak pasti)
print("\n" + "="*100)
nama = str(input("Nama: "))

input_genres = input("Masukkan genre favorit (pisahkan dengan koma jika lebih dari satu): ")
user_genres = [genre.strip().lower() for genre in input_genres.split(',')]

print("\nSeberapa kamu suka genre-genre tersebut?")
tingkat_suka = int(input(
    "1 = Sangat suka\n"
    "2 = Suka\n"
    "3 = Standar\n"
    "4 = Kurang suka\n"
    "5 = Tidak suka\n"
    "Pilihan (1-5): "
))

# Mapping minat
map_minat = {
    1: 10,  # Sangat suka
    2: 7,   # Suka
    3: 5,   # Standar
    4: 3,   # Kurang suka
    5: 1    # Tidak suka
}
minat_user = map_minat.get(tingkat_suka, 5)

# Filter buku berdasarkan genre buku yang sudah dipilih
df_filtered = df[df['Categories'].str.lower().str.contains('|'.join(user_genres), na=False)].copy()

if df_filtered.empty:
    print("\n⚠ Tidak ditemukan buku dengan genre tersebut!")
else:
    # Hitung skor rekomendasi
    skor = []
    for i, row in df_filtered.iterrows():
        simulasi.input['Rating'] = row['Average_rating']
        simulasi.input['Minat'] = minat_user
        simulasi.compute() # menjalankan seluruh proses (fuzzifikasi(konversi input crisp) - inferensi(aplikasi rule base) - defuzzifikasi(konversi output))
        skor.append(simulasi.output['Rekomendasi'])  # Mendapatkan nilai dari output (sudah berupa nilai akhir perhitungan)
    
    # Untuk pengelompokan dari rating yang diberikan orang pada dataset
    df_filtered.loc[:, 'Rekomendasi_score'] = skor
    
    # Melakukan perhitungan seberapa cocok tiap buku yang ada dengan genre favorit dari pengguna
    df_filtered.loc[:, 'Match_score'] = df_filtered['Categories'].apply(
        lambda x: sum(genre in x.lower() for genre in user_genres)
    )
    
    # Melakukan penjumlahan antara rating dan pencocokan score
    df_filtered.loc[:, 'Final_score'] = df_filtered['Rekomendasi_score'] + df_filtered['Match_score']
    
    # Urutkan hasil dari yang paling direkomendasikan
    df_result = df_filtered.sort_values(
        by=['Final_score', 'Rekomendasi_score'], 
        ascending=False
    )
    
    # Tampilkan hasil
    print("\n" + "="*110)
    print(f"                                      📚 Rekomendasi Buku untuk {nama} ({', '.join(user_genres)}):")
    print("="*110)
    
    pd.set_option('display.max_columns', None)
    print(df_result[['Title', 'Authors', 'Categories', 'Published_year', 'Average_rating', 'Final_score']].head(20).to_string(index=False))