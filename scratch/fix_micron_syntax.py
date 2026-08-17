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
    index_content = """# Çınarcık Mesh Düğümü - Ana Sayfa

> **Hoş Geldiniz!** -TA2LRW Hüseyin- Bu sayfa Çınarcık / Yalova RNode LoRa Mesh ağı üzerinden 433.325 MHz frekansında yayın yapmaktadır.

## Sayfa Menüsü
Aşağıdaki bağlantılara tıklayarak sayfalar arasında gezinebilirsiniz:

[1. Hakkımda ve Düğüm Bilgileri](page://about.mu)
[2. Amatör Telsizcilik & Frekans Rehberi](page://hamradio.mu)
[3. Acil Durum & Hayatta Kalma Rehberi](page://survival.mu)

---
```
Düğüm Konumu: KN40NP Çınarcık / Yalova (24/7 Kesintisiz)
Frekans: 433.325 MHz (SF9 / BW 125 kHz / CR 4/5)
```
"""

    about_content = """# Hakkımda & Çınarcık Düğüm Bilgileri

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

[Ana Sayfaya Dön](page://index.mu)
"""

    hamradio_content = """# Amatör Telsizcilik & Frekans Rehberi

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

[Ana Sayfaya Dön](page://index.mu)
"""

    survival_content = """# Acil Durum & Hayatta Kalma Rehberi

> **İnternet veya GSM Kesildiğinde Uygulanacak Adımlar**

## 1. Su Arıtma ve Hijyen
* **Kaynatma:** Suyu en az 3 dakika boyunca fokurdayacak şekilde kaynatın.

## 2. Acil Durum Çantası Kontrol Listesi
- [x] RNode LoRa Telsiz Cihazı & Powerbank
- [x] Düdük ve El Feneri
- [x] İlk Yardım Çantası & İlaçlar

[Ana Sayfaya Dön](page://index.mu)
"""

    def write_remote(filename, content):
        p1 = f"/root/.nomadnetwork/storage/pages/{filename}"
        p2 = f"/root/.nomadnet/storage/pages/{filename}"
        cmd = f"cat << 'EOF' > {p1}\n{content}\nEOF\ncat << 'EOF' > {p2}\n{content}\nEOF"
        run_ssh(cmd)

    write_remote("index.mu", index_content)
    write_remote("about.mu", about_content)
    write_remote("hamradio.mu", hamradio_content)
    write_remote("survival.mu", survival_content)
    
    print("All .mu page files updated with exact clean Micron link syntax [Label](page://file.mu) without spaces!")
