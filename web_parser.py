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

    data = []
    current_uni = None

    # Üniversite isimleri genellikle h2 veya <p><strong><em> gibi yerlerde
    # Öncelikle tüm h2 ve p içindeki strong>em elementlerini topla
    uni_headers = []
    for h2 in soup.find_all('h2'):
        uni_headers.append((h2, h2.get_text(strip=True)))
    for p in soup.find_all('p'):
        strong_em = p.find('strong')
        if strong_em and strong_em.find('em'):
            uni_headers.append((p, strong_em.get_text(strip=True)))

    # Sort uni_headers by their position in the document to iterate orderly
    uni_headers = sorted(uni_headers, key=lambda x: x[0].sourceline if x[0].sourceline else 0)

    # Üniversiteler arasında gezinerek bölümleri çek
    for i, (header_elem, uni_name) in enumerate(uni_headers):
        # Başlangıç elementi ve bitiş elementi belirle (bir sonraki üniversitenin başlığına kadar)
        start = header_elem
        end = uni_headers[i + 1][0] if i + 1 < len(uni_headers) else None

        # Üniversite içindeki tüm p taglarını topla
        content_ps = []
        sibling = start.find_next_sibling()
        while sibling and sibling != end:
            if sibling.name == 'p':
                content_ps.append(sibling)
            sibling = sibling.find_next_sibling()

        # Her p içinde bölümleri ayrıştır
        for p in content_ps:
            text = p.get_text(separator="\n").strip()

            # Her satırı işle
            for line in text.split('\n'):
                line = line.strip()
                if not line.startswith('▶'):
                    continue

                # Örnek satır:
                # ▶ Kompüter elmləri (tədris ingilis dilində) Ə 250.0 (431.9)
                # Regex ile parse edelim:
                pattern = re.compile(
                    r'▶\s*'  # başındaki ▶ işareti
                    r'(?P<dept>.+?)\s*'  # bölüm adı (tembel)
                    r'(\(tədris ingilis dilində\))?\s*'  # optional ingilizce ibaresi
                    r'(?P<eduform>[ƏQ])\s*'  # eğitim formu Ə veya Q
                    r'(?P<paid>\d+\.?\d*)\s*\(?\s*'  # paid score
                    r'(?P<free>[\d\–\.]+)\)?'  # free score veya –
                )

                match = pattern.match(line)
                if match:
                    dept = match.group("dept").strip()
                    eduform_code = match.group("eduform")
                    paid_score = match.group("paid")
                    free_score = match.group("free")

                    # Eğitim formu
                    eduform = "Əyani" if eduform_code == "Ə" else "Qiyabi"
                    # Dil
                    language = "İngilis dili" if '(tədris ingilis dilində)' in line else "Azərbaycan dili"

                    # free_score '-' ise None yap
                    free_score_val = None if free_score == '–' else float(free_score)
                    paid_score_val = float(paid_score)

                    data.append({
                        "University": uni_name,
                        "Department": dept,
                        "EducationForm": eduform,
                        "Language": language,
                        "PaidScore": paid_score_val,
                        "FreeScore": free_score_val
                    })

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    url = input("Parse etmek istediğiniz sayfanın URL'sini girin: ").strip()
    html = fetch_html(url)
    df = parse_qebulol_page(html)

    output_file = input("Çıktı CSV dosya adını girin (örnek: cikti.csv): ").strip()
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✅ Veriler '{output_file}' dosyasına başarıyla yazıldı.")
