import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

hostname = "192.168.1.12"
username = "root"
password = "1234"

def run_ssh(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=22, username=username, password=password, timeout=30)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    client.close()
    return out, err

if __name__ == "__main__":
    recompile_script = """
import os
import re
from RNS.Utilities.rngit.util import MarkdownToMicron

def sanitize_links(text):
    if not text: return text
    def clean_link(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        if url.startswith(":/page/"): url = url[7:]
        elif url.startswith("/page/"): url = url[6:]
        elif url.startswith("page://"): url = url[7:]
        return f"[{label}]({url})"
    return re.sub(r'\[\s*([^\]]+?)\s*\]\(([^)]+)\)', clean_link, text)

pages = {
"index.mu": '''# Çınarcık Mesh Düğümü - Ana Sayfa

> **Hoş Geldiniz!** -TA2LRW Hüseyin- Bu sayfa Çınarcık / Yalova RNode LoRa Mesh ağı üzerinden 433.325 MHz frekansında yayın yapmaktadır.

## Sayfa Menüsü
Aşağıdaki bağlantılara tıklayarak sayfalar arasında gezinebilirsiniz:

[1. Hakkımda ve Düğüm Bilgileri](about.mu)
[2. Amatör Telsizcilik & Frekans Rehberi](hamradio.mu)
[3. Acil Durum & Hayatta Kalma Rehberi](survival.mu)

---
```
Düğüm Konumu: KN40NP Çınarcık / Yalova (24/7 Kesintisiz)
Frekans: 433.325 MHz (SF9 / BW 125 kHz / CR 4/5)
```
''',

"about.mu": '''# Hakkımda & Çınarcık Düğüm Bilgileri

> **Amatör Telsiz & Off-Grid Çınarcık İletişim İstasyonu**

## QTH ve Konum Bilgileri
* **Çağrı Kodu:** TA2LRW
* **Operatör:** Hüseyin
* **Bölge:** Yalova / Çınarcık (KN40NP)
* **Düğüm Kimliği:** RNode-Cinarcik-Server

## Donanım Detayları

| Donanım | Özellik |
| :--- | :--- |
| **Ana Sunucu** | Debian Linux (24/7 Kesintisiz) |
| **RTM / RNode** | ESP32 + SX1278 (433.325 MHz) |
| **Anten** | 3m UHF/VHF Yüksek Kazançlı Anten |

[Ana Sayfaya Dön](index.mu)
''',

"hamradio.mu": '''# Amatör Telsizcilik & Frekans Rehberi

> **"Amatör Telsizcilik, Afet Anında Tek Kesintisiz İletişim Hattıdır."**

## Çınarcık LoRa RNode Ağ Parametreleri

* **Çalışma Frekansı:** 433.325 MHz (ISM Bandı)
* **Spreading Factor (SF):** SF9
* **Bant Genişliği (BW):** 125 kHz
* **Coding Rate (CR):** 4/5
* **Yayın Gücü (TX Power):** 14 dBm (25 mW)

## Sık Kullanılan Q-Kodları

| Kod | Anlamı |
| :--- | :--- |
| **QTH** | Bulunduğum konum / İstasyona olan konum |
| **QSO** | Birebir telsiz görüşmesi yapma |
| **QRM** | İnsan kaynaklı parazit / gürültü |

[Ana Sayfaya Dön](index.mu)
''',

"survival.mu": '''# Acil Durum & Hayatta Kalma Rehberi

> **Şebeke ve İnternet Kesintisinde Uygulanacak Acil Saha Prosedürleri**

## Alt Konu Rehberleri
Aşağıdaki başlıklara tıklayarak saha kılavuzlarına ulaşabilirsiniz:

[1. Enkaz Altından İletişim & SOS Mors Teknikleri](survival_sos.mu)
[2. Saha Şartlarında Su Arıtma & Dezenfeksiyon](survival_water.mu)
[3. Kritik İlkyardım & Kanama Durdurma](survival_firstaid.mu)

---
```
Düğüm Kodu: TA2LRW | Bölge: Çınarcık / Yalova (KN40NP)
Yayın Frekansı: 433.325 MHz (SF9 / BW 125 kHz / CR 4/5)
```

[Ana Sayfaya Dön](index.mu)
''',

"survival_sos.mu": '''# Enkaz Altı İletişim & SOS Mors Teknikleri

## 1. Ses ve Vurmalı İşaret (Sistemli Ses Çıkarma)
* **Enerji Koruması:** Bağırmak toz yutturur ve çabuk tüketir. Vurmalı ses kullan.
* **Nesne Seçimi:** Beton, kalorifer borusu veya demir donatıya sert nesneyle vur.
* **3'lü Kural:** 3 darbe vur -> 3 saniye dinle. Sesi periyodik tekrar et.

## 2. Mors Kodu SOS İşareti
* **Mors Dizilimi:** `... --- ...` (3 Kısa - 3 Uzun - 3 Kısa)
* **Vuruş Ritmi:**
  - 3 Hızlı Vuruş (Kısa)
  - 3 Yavaş/Güçlü Vuruş (Uzun)
  - 3 Hızlı Vuruş (Kısa)
* **Bekleme:** Her dizilimden sonra 5 saniye ses dinleme molası ver.

## 3. Telsiz / LoRa Kullanımı
* RNode veya Telsiz açık ise cihazı göğüs hizasında tut, bataryayı koru.

[Acil Durum Rehberine Dön](survival.mu) | [Ana Sayfaya Dön](index.mu)
''',

"survival_water.mu": '''# Saha Şartlarında Su Arıtma & Dezenfeksiyon

## 1. Ön Filtreleme (Tortu ve Çamur Ayrıştırma)
* Temiz bez, tişört veya kum/kömür katmanından suyu süzerek kaba tortuyu ayır.

## 2. Isıl Dezenfeksiyon (Kaynatma)
* Suyu en az 3 dakika boyunca fokurdayacak şekilde kaynat.
* Yüksek rakımda kaynama süresini 5 dakikaya çıkar.

## 3. Kimyasal Dezenfeksiyon (Çamaşır Suyu / Klor)
* **Oran:** 1 Litre berrak suya 2 damla kokusuz çamaşır suyu (%5-6 sodyum hipoklorit).
* **Bekleme:** Karıştırıp 30 dakika kapağı kapalı bekle. Klor kokusu gelmeli.

## 4. SODIS (Güneşle Sterilizasyon)
* Şeffaf pet şişeye süzülmüş suyu doldur. 6 saat doğrudan güneş altında tut.

[Acil Durum Rehberine Dön](survival.mu) | [Ana Sayfaya Dön](index.mu)
''',

"survival_firstaid.mu": '''# Kritik İlkyardım & Kanama Durdurma

## 1. Şiddetli Atardamar Kanamaları (Turnike)
* **Konum:** Kanamalı bölgenin 5-7 cm yukarısına (eklem üstüne değil).
* **Uygulama:** Geniş bez/kemer bağla, sopa ile döndürerek kanama durana kadar sık.
* **Zaman Kaydı:** Turnike saati alına/kıyafete mutlaka yazılmalıdır (Örn: T-14:30).

## 2. Basınçlı Tampon
* Temiz bez veya gazlı bezi yaranın üzerine koy, en az 10 dakika kesintisiz bastır.

## 3. Şok Pozisyonu
* Yaralıyı sırtüstü yatır, bacaklarını 30 cm yukarı kaldır, üstünü ört.

[Acil Durum Rehberine Dön](survival.mu) | [Ana Sayfaya Dön](index.mu)
'''
}

dirs = ["/root/.nomadnetwork/storage/pages", "/root/.nomadnet/storage/pages"]
for d in dirs:
    os.makedirs(d, exist_ok=True)

converter = MarkdownToMicron()
for fname, content in pages.items():
    cleaned = sanitize_links(content)
    compiled = converter.format_block(cleaned)
    for d in dirs:
        with open(os.path.join(d, fname + ".src"), "w", encoding="utf-8") as f:
            f.write(cleaned)
        with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
            f.write(compiled)
    print(f"Recompiled survival guide page {fname} successfully!")
"""

    run_ssh("cat << 'EOF' > /root/update_survival.py\n" + recompile_script + "\nEOF")
    out, err = run_ssh("python3 /root/update_survival.py")
    print("Survival update output:\n", out)
    print("Survival update err:\n", err)
    
    # Restart server.py cleanly
    run_ssh("pkill -9 -f 'server.py' 2>/dev/null")
    cmd = "cd ~/DIY-RNode-ESP32-LoRa/micron_app && nohup python3 server.py > /tmp/server.log 2>&1 &"
    out_srv, err_srv = run_ssh(cmd)
    print("Server restart output:\n", out_srv)
