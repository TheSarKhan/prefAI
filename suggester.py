import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("group1_2025.csv", encoding='utf-8')

# MinScore sütununu sayısal hale getir
df['MinScore'] = pd.to_numeric(df['MinScore'], errors='coerce')

# Dil temizliği (Department içinde ingilis dili kontrolü)
def clean_language(row):
    dep = str(row['Department']).lower()
    if "tədris ingilis" in dep or "ingilis" in dep:
        return "ingilis dili"
    else:
        return "azərbaycan dili"

df['language_clean'] = df.apply(clean_language, axis=1)

# Kullanıcının puanına göre öneri fonksiyonu
def suggest_departments(df, user_score):
    suitable = df[df['MinScore'] <= user_score]
    suggestions = suitable[['University', 'Department', 'MinScore', 'language_clean']]
    return suggestions.sort_values(by='MinScore', ascending=False)

# Kullanıcıdan puan al
user_score = float(input("Sınav puanınızı girin: "))

# Önerileri al ve yazdır
result = suggest_departments(df, user_score)

print(f"\nPuanınıza uygun bölümler:\n")
print(result.to_string(index=False))
