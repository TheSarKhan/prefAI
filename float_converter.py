import pandas as pd

# Dosyayı oku
df = pd.read_csv("group1_2025.csv", encoding='utf-8')

# MinScore sütununu sayısal hale getiriyoruz
df['MinScore'] = pd.to_numeric(df['MinScore'], errors='coerce')

# Eksik değerlerin sayısını yazdırıyoruz
print("Eksik MinScore sayısı:", df['MinScore'].isna().sum())

# Eksik değerlerin olduğu satırları gösteriyoruz
print(df[df['MinScore'].isna()])
