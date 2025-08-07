import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_qebulol_page(html):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all("p")

    data = []
    current_uni = None

    for p in elements:
        text = p.get_text(separator="\n").strip()

        # Universitet adı gəldikdə dəyiş
        if "Universiteti" in text:
            current_uni = text.strip()
        elif "▶" in text and current_uni:
            lines = text.split("▶")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Regex nümunəsi:
                # Bölüm Adı (məsələn: İnformasiya təhlükəsizliyi (tədris ingilis dilində))
                # Sonra boşluq, sonra Ə və ya Q (təhsil forması)
                # Sonra boşluq, sonra ödənişli puan (məsələn 200.0)
                # Sonra ( içində pulsuz puan (məsələn 394.8)
                pattern = r"(.+?)\s+(Ə|Q)\s+(\d{1,3}\.\d)\s*\((\d{1,3}\.\d|–)\)"

                match = re.search(pattern, line)
                if match:
                    dept, edu_code, paid_score, free_score = match.groups()

                    education_form = "Əyani" if edu_code == "Ə" else "Qiyabi"

                    # Dil təyini (department içində "tədris ingilis" varsa ingilis dili)
                    lang = "Azərbaycan dili"
                    if "tədris ingilis" in dept.lower() or "ingilis dilində" in dept.lower():
                        lang = "İngilis dili"

                    data.append({
                        "University": current_uni,
                        "Department": dept.strip(),
                        "EducationForm": education_form,
                        "Language": lang,
                        "PaidScore": float(paid_score),
                        "FreeScore": float(free_score) if free_score != "–" else None
                    })

    df = pd.DataFrame(data)
    return df


# İstifadəçi URL daxil edir
url = input("Parse ediləcək səhifənin URL-ni daxil et: ").strip()
html = fetch_html(url)
df = parse_qebulol_page(html)

# CSV kimi saxla
output_file = "qrup1_clean.csv"
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"✅ Veriler '{output_file}' faylına yazıldı.")
