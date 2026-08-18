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

> **Kriz ve Afet Anlarında Saha Hayatta Kalma Kılavuzları**

## Saha Kılavuzları
İlgili konuya tıklayarak saha talimatını görüntüleyin:

[1. Enkaz Altından İletişim & SOS Mors](survival_sos.mu)
[2. Su Arıtma & Dezenfeksiyon](survival_water.mu)
[3. Kritik İlkyardım & Kanama Durdurma](survival_firstaid.mu)
[4. Nükleer Serpinti & Radyasyondan Korunma](survival_radiation.mu)
[5. Tsunami & Kıyı Afet Tahliyesi](survival_tsunami.mu)
[6. Aşırı Soğuktan Korunma & Geçici Barınak](survival_cold.mu)

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
''',

"survival_radiation.mu": '''# Nükleer Serpinti & Radyasyondan Korunma

## 1. Temel Korunma Kuralları (TDS İlkesi)
* **Zaman:** Radyasyona maruz kalma süresini minimuma indir.
* **Mesafe:** Radyasyon kaynağından/patlama merkezinden olabildiğince uzaklaş.
* **Siperleme:** Kalın beton ve toprak yapıların arkasına sığın.

## 2. Serpinti (Fallout) Zamanlama Kuralı (7/10 Kuralı)
* Patlamadan sonraki her 7 katlık süre artışında radyasyon 10 kat düşer.
* İlk 24-48 saat sığınaktan kesinlikle dışarı çıkma.

## 3. Bina İçi Sığınma Prosedürü
* Binanın ortasına veya bodrum katına in (Pencerelerden uzak dur).
* Havalandırma, klima ve pencereleri bantla/kapat.
* Dışarıdan girdiysen kıyafetlerini çıkarıp poşetle, cildini sabunlu suyla yıka.

## 4. Tiroid Koruma (İyot Tableti)
* Potasyum İyodür tabletlerini sadece resmi makam uyarısıyla kullan.

[Acil Durum Rehberine Dön](survival.mu) | [Ana Sayfaya Dön](index.mu)
''',

"survival_tsunami.mu": '''# Tsunami & Kıyı Afet Tahliye Kılavuzu

## 1. Erken Uyarı Emareleri
* Şiddetli deniz tabanı depremi veya denizin aniden çekilmesi/kıyıdan kaybolması.
* Denizden gelen anormal gürültü ve Uğultu sesi.

## 2. Tahliye Kuralı (Yüksek Yere Kaçış)
* **İrtifa:** Deniz seviyesinden en az 20-30 metre yükseğe çık.
* **Mesafe:** Kıyı çizgisinden en az 2-3 km içeri/karaya doğru kaç.
* Yürüyerek veya koşarak kaç (Araçlar trafiği tıkar).

## 3. İlk Dalga Tuzağı
* İlk gelen dalga en büyüğü olmayabilir. 2. ve 3. dalgalar saatler sonra ve daha büyük gelebilir.
* Yetkili duyuru yapılana kadar kıyıya ve plaja asla geri dönme.

[Acil Durum Rehberine Dön](survival.mu) | [Ana Sayfaya Dön](index.mu)
''',

"survival_cold.mu": '''# Aşırı Soğuktan Korunma & Barınma Kılavuzu

## 1. Hipotermi Önleme ve İlk Müdahale
* **Belirtiler:** Şiddetli titreme, zihinsel bulanıklık, yavaş konuşma.
* **Islak Kıyafet:** Islak elbiseleri hemen çıkar; ıslak kumaş vücut ısısını 25 kat hızlı düşürür.
* **Isıtma:** Hastanın kasık, koltuk altı ve göğüs bölgesini ılık/kuru bezle ısıt.

## 2. Katmanlı Giyim (Soğan Kabuğu Kuralı)
* **İç Katman:** Nemi dışarı atan sentetik/yün içlik (Pamuklu giyme).
* **Orta Katman:** Isıyı tutan polar/yün giysi.
* **Dış Katman:** Rüzgar ve su geçirmeyen mont/ceket.

## 3. Geçici Barınak & İzolasyon
* **Toprak Yalıtımı:** Doğrudan toprağa yatma! Altına karton, yaprak, kuru dal yerleştir.
* **Küçük Hacim:** Barınağı iç hacmi küçük tut ki vücut ısın ortamı kolay ısıtsın.

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
    print(f"Compiled advanced survival guide {fname} successfully!")
"""

    run_ssh("cat << 'EOF' > /root/update_advanced_survival.py\n" + recompile_script + "\nEOF")
    out, err = run_ssh("python3 /root/update_advanced_survival.py")
    print("Advanced survival update output:\n", out)
    print("Advanced survival update err:\n", err)
