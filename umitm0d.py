import requests
import json
import re

# Ülke isimlerini Türkçeye çevirme eşleme tablosu
country_mapping = {
    "Germany": ("Almanya", "Almanca"),
    "United Kingdom": ("Birleşik Krallık", "İngilizce"),
    "France": ("Fransa", "Fransızca"),
    "Turkey": ("Türkiye", "Türkçe"),
    "Italy": ("İtalya", "İtalanca"),
    "Spain": ("İspanya", "İspanyolca"),
    "Albania": ("Arnavutluk", "Arnavutça"),
    "Arabia": ("Arabistan", "Arapça"),
    "Balkans": ("Balkanlar", "Türkçe"),
    "Bulgaria": ("Bulgaristan", "Bulgarca"),
    "Netherlands": ("Hollanda", "Felemenkçe"),
    "Poland": ("Polonya", "Lehçe"),
    "Portugal": ("Portekiz", "Portekizce"),
    "Russia": ("Rusya", "Rusça"),
}

DEFAULT_TVG_LOGO_URL = "https://i.hizliresim.com/t6e66bt.png"

def sort_key(tvg_name):
    """Sıralama önceliği belirleme"""
    tvg_name_lower = tvg_name.lower()
    is_bein_spor = "bein" in tvg_name_lower and "spor" in tvg_name_lower
    is_spor = "spor" in tvg_name_lower or "sport" in tvg_name_lower
    
    if is_bein_spor:
        group_priority = 0
    elif is_spor:
        group_priority = 1
    else:
        group_priority = 2
    
    return (group_priority, tvg_name_lower)

# JSON verisini çek
url = "https://www2.vavoo.to/live2/index?countries=all&output=json"
response = requests.get(url)
channels = response.json()

# Türkiye kanallarını filtrele ve işle
turkey_channels = []

for channel in channels:
    group = channel["group"]
    
    # Sadece Turkey (Türkiye) kategorisindeki kanalları işle
    if group != "Turkey":
        continue
    
    logo = channel["logo"]
    name = channel["name"]
    channel_url = channel["url"]
    
    # Ülke adına göre tvg-country ve tvg-language belirleme
    country_name, language_code = country_mapping.get(group, (group, "xx"))
    
    # tvg-id oluşturma (kanal adı + ülke kodu)
    tvg_id = f"{name.lower().replace(' ', '').replace('.', '')}.{language_code}"
    
    # URL formatını değiştirme
    stream_url = channel_url.replace("live2/play", "play").replace(".ts", "/index.m3u8")
    
    # Logo yoksa varsayılan logo kullan
    if not logo:
        logo = DEFAULT_TVG_LOGO_URL
    
    # Kanal bilgilerini listeye ekle
    turkey_channels.append({
        'name': name,
        'tvg_id': tvg_id,
        'logo': logo,
        'language_code': language_code,
        'stream_url': stream_url,
        'sort_priority': sort_key(name)
    })

print(f"Toplam {len(turkey_channels)} kanal bulundu.")

# Sıralama: Önce Bein Spor, sonra diğer spor kanalları, sonra genel kanallar
# Her grup içinde alfabetik
turkey_channels.sort(key=lambda x: x['sort_priority'])

# Kanal sayılarını hesapla
bein_spor_count = sum(1 for c in turkey_channels if c['sort_priority'][0] == 0)
other_spor_count = sum(1 for c in turkey_channels if c['sort_priority'][0] == 1)
general_count = sum(1 for c in turkey_channels if c['sort_priority'][0] == 2)
total_count = len(turkey_channels)

print(f"Bein Spor kanalları: {bein_spor_count}")
print(f"Diğer Spor kanalları: {other_spor_count}")
print(f"Genel kanallar: {general_count}")

# M3U dosya içeriği oluştur
m3u_content = "#EXTM3U\n"

for channel in turkey_channels:
    m3u_content += f'#EXTINF:-1 tvg-id="{channel["tvg_id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["logo"]}" group-title="Vavoo Tv" tvg-country="TR" tvg-language="{channel["language_code"]}", {channel["name"]}\n {channel["stream_url"]}\n'

# Dosyayı bulunduğu dizine kaydet
with open("vavoo.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print(f"M3U listesi oluşturuldu: vavoo.m3u")
print("İşlem tamamlandı.")    {"dosya": "yayinex2.m3u8", "tvg_id": "ExxenSpor2.tr", "kanal_adi": "Exxen Spor 2 HD"},
    {"dosya": "yayinex3.m3u8", "tvg_id": "ExxenSpor3.tr", "kanal_adi": "Exxen Spor 3 HD"},
    {"dosya": "yayinex4.m3u8", "tvg_id": "ExxenSpor4.tr", "kanal_adi": "Exxen Spor 4 HD"},
    {"dosya": "yayinex5.m3u8", "tvg_id": "ExxenSpor5.tr", "kanal_adi": "Exxen Spor 5 HD"},
    {"dosya": "yayinex6.m3u8", "tvg_id": "ExxenSpor6.tr", "kanal_adi": "Exxen Spor 6 HD"},
    {"dosya": "yayinex7.m3u8", "tvg_id": "ExxenSpor7.tr", "kanal_adi": "Exxen Spor 7 HD"},
    {"dosya": "yayinex8.m3u8", "tvg_id": "ExxenSpor8.tr", "kanal_adi": "Exxen Spor 8 HD"},
]

def siteyi_bul():
    print(f"\n{GREEN}[*] Site aranıyor...{RESET}")
    for i in range(1459, 1750):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            print(f"{RED}[-] {url} erişilemedi.{RESET}")
    return None

def find_baseurl(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None
    match = re.search(r'baseurl\s*[:=]\s*["\']([^"\']+)["\']', r.text)
    if match:
        return match.group(1)
    return None

def generate_m3u(base_url, referer, user_agent):
    lines = ["#EXTM3U"]
    for idx, k in enumerate(KANALLAR, start=1):
        name = f"ÜmitM0d {k['kanal_adi']}"
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(base_url + k["dosya"])
        print(f"  ✔ {idx:02d}. {name}")
    return "\n".join(lines)

if __name__ == "__main__":
    site = siteyi_bul()
    if not site:
        print(f"{RED}[HATA] Yayın yapan site bulunamadı.{RESET}")
        sys.exit(1)

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_baseurl(channel_url)
    if not base_url:
        print(f"{RED}[HATA] Base URL bulunamadı.{RESET}")
        sys.exit(1)

    playlist = generate_m3u(base_url, site, "Mozilla/5.0")
    with open("umitm0d.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"{GREEN}[OK] Playlist oluşturuldu: umitm0d.m3u{RESET}")
