import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://qebulol.az/1-ci-qrup-kecid-ballari-2025/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

# Üniversite başlıklarını ve sonrasındaki bölüm satırlarını ayıklama
data = []
current_univ = None

for element in soup.find_all(["h1", "p"]):
    text = element.get_text(separator="\n", strip=True)
    # Üniversite adı: genellikle tek satır ve başlık
    if element.name in ("h1",) or (element.name=="p" and not text.startswith("▶")):
        current_univ = text
    elif element.name=="p":
        # bölümlerin olduğu p etiketinde ▶ ile satırlar
        for line in text.split("\n"):
            if line.strip().startswith("▶"):
                # Örnek: ▶ Kompüter elmləri Ə 414.8(414.8)
                m = re.match(r"▶\s*(.+?)\s+([ƏQ])\s+([0-9.]+)", line)
                if m:
                    dept = m.group(1).strip()
                    lang = m.group(2)
                    score = m.group(3)
                    data.append([current_univ, dept, lang, score])

# CSV oluştur
with open("group1_2025.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["University", "Department", "Language", "MinScore"])
    writer.writerows(data)

print("✅ Veri kaydedildi: group1_2025.csv")
