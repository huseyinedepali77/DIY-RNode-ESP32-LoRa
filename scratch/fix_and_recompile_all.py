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
from RNS.Utilities.rngit.util import MarkdownToMicron

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

> **İnternet veya GSM Kesildiğinde Uygulanacak Adımlar**

## 1. Su Arıtma ve Hijyen
* **Kaynatma:** Suyu en az 3 dakika boyunca fokurdayacak şekilde kaynatın.

## 2. Acil Durum Çantası Kontrol Listesi
- [x] RNode LoRa Telsiz Cihazı & Powerbank
- [x] Düdük ve El Feneri
- [x] İlk Yardım Çantası & İlaçlar

[Ana Sayfaya Dön](index.mu)
'''
}

dirs = ["/root/.nomadnetwork/storage/pages", "/root/.nomadnet/storage/pages"]
for d in dirs:
    os.makedirs(d, exist_ok=True)

converter = MarkdownToMicron()
for fname, content in pages.items():
    compiled = converter.format_block(content)
    for d in dirs:
        # Save source markdown
        with open(os.path.join(d, fname + ".src"), "w", encoding="utf-8") as f:
            f.write(content)
        # Save compiled micron
        with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
            f.write(compiled)
    print(f"Recompiled {fname} and created .src!")
"""

    run_ssh("cat << 'EOF' > /root/recompile_clean.py\n" + recompile_script + "\nEOF")
    run_ssh("python3 /root/recompile_clean.py")
    
    cmd = "pkill -9 -f 'server.py' 2>/dev/null; cd ~/DIY-RNode-ESP32-LoRa && git pull && cd micron_app && nohup python3 server.py > /tmp/server.log 2>&1 &"
    out, err = run_ssh(cmd)
    print("Server restart output:\n", out)
    print("Server restart err:\n", err)
