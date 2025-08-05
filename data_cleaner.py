import pandas as pd

df = pd.read_csv("group1_2025.csv", encoding='utf-8')

def clean_language(row):
    dep = str(row['Department']).lower()
    if "tədris ingilis" in dep or "tədris ingilis dilində" in dep or "ingilis" in dep:
        return "ingilis dili"
    else:
        return "azərbaycan dili"

# apply fonksiyonunu satır bazında kullanıyoruz
df['language_clean'] = df.apply(clean_language, axis=1)

# Sonuçları kontrol et
print(df[['Department', 'language_clean']].head(20))

# Dosyayı kaydet
df.to_csv("cleaned_group1_2025.csv", index=False, encoding='utf-8')
