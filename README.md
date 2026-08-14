# 📡 DIY ESP32 + SX1278 LoRa - RNode Firmware & Mesh Ağ Kurulumu

Bu proje, standart bir **ESP32** kartı ve **SX1278 LoRa modülü** kullanarak tamamen **internetsiz, şebekesiz ve bağımsız (Off-Grid)** çalışan bir telsiz/mesajlaşma ağı kurmanızı sağlar.

Hiç teknik bilgisi olmayan kişilerin bile evindeki parçalarla adım adım kurabilmesi için en basit dille hazırlanmıştır.

---

## 💡 Temel Mantık: Bu Cihaz Ne İşe Yarar?

Bu cihaz, telefonunuzun veya bilgisayarınızın **internete, Wi-Fi'a veya GSM hattına ihtiyaç duymadan** diğer cihazlarla kilometrelerce uzaktan radyo dalgaları (LoRa RF) üzerinden haberleşmesini sağlar. Afet durumlarında, dağda, kampta veya altyapının olmadığı her yerde kesintisiz mesajlaşabilirsiniz.

---

## 🛠️ Donanım Malzemeleri (Neler Gerekli?)

1. **ESP32 NodeMCU Geliştirme Kartı** (30 veya 38 Pin)
2. **SX1278 veya SX1276 LoRa Modülü** (433 MHz frekansında çalışan)
3. *(İsteğe Bağlı)* **OLED Ekran** (0.96" veya 1.3" SH1106/SSD1306 ekran)
4. **Jumper Kablolar** ve USB Kablosu

---

## 🔌 Donanım Pin Bağlantı Şeması (Kablolar Nereye Takılacak?)

ESP32 kartınız ile LoRa modülünü aşağıdaki tabloya bakarak jumper kablolarla birbirine bağlayın:

### 📡 LoRa Modülü (SX1278) -> ESP32 Bağlantısı:

| LoRa Modülündeki Pin Adı | ESP32 Kartındaki Pin Adı | Açıklama ve Uyarılar |
| :--- | :--- | :--- |
| **VCC** | **3.3V** | ⚠️ **Çok Önemli:** Sadece 3.3V pinine bağlayın. Sakın 5V vermeyin! |
| **GND** | **GND** | Toprak / Eksi Uç |
| **SCK** | **GPIO 5** | Veri Saat Hattı |
| **MISO** | **GPIO 19** | Veri Alış Hattı |
| **MOSI** | **GPIO 27** | Veri Gönderim Hattı |
| **NSS / CS** | **GPIO 18** | Modül Seçim Pini |
| **RESET** | **GPIO 23** | Yeniden Başlatma Pini |
| **DIO0** | **GPIO 26** | Sinyal Bildirim Pini |

### 📺 OLED Ekran Bağlantısı (Eğer Ekranınız Varsa):
- **VCC** ➔ ESP32 **3.3V**
- **GND** ➔ ESP32 **GND**
- **SDA** ➔ ESP32 **GPIO 21**
- **SCL** ➔ ESP32 **GPIO 22**

---

## 🚀 1. Bölüm: Yazılımın ESP32 Kartına Yüklenmesi

1. Bilgisayarınıza **VS Code** programını ve içine **PlatformIO** eklentisini kurun.
2. Bu projeyi **ZIP** olarak indirip klasöre çıkarın ve VS Code ile açın (`File -> Open Folder`).
3. ESP32 kartınızı USB kablosuyla bilgisayara bağlayın.
4. VS Code'un en altındaki mavi çubukta yer alan **`➔` (Upload)** butonuna basın.
5. Yazılım karta yüklenecek ve frekans ayarları (`433.325 MHz`) otomatik yapılacaktır.

---

## 💻 2. Bölüm: Windows ve Linux Üzerinde Reticulum Ayarları

Cihazı bilgisayara bağladıktan sonra NomadNet/Reticulum uygulamasının cihazı görebilmesi için konfigürasyon dosyasını düzenlememiz gerekir.

---

### 🪟 A. WINDOWS KULLANICILARI İÇİN:

#### 1. COM Portunuzu Bulun:
- Başlat menüsüne sağ tıklayıp **Aygıt Yöneticisi**'ni (Device Manager) açın.
- **Bağlantı Noktaları (COM ve LPT)** bölümünü genişletin.
- Cihazınızın yanındaki COM numarasını öğrenin (Örneğin: **`COM3`** veya **`COM4`**).

#### 2. Config Dosyasını Açın:
- `Windows Tuşu + R` basarak **Çalıştır** penceresini açın.
- Şu adresi yapıştırıp Enter'a basın:  
  `%USERPROFILE%\.reticulum`
- Klasördeki **`config`** dosyasını Not Defteri (Notepad) ile açın.  
  *(Veya dosya yolu: `C:\Users\KullanıcıAdınız\.reticulum\config`)*

#### 3. Ayarları Yapıştırın:
Dosya içindeki `[interfaces]` başlığının altına şu satırları ekleyin:

```ini
[[RNode LoRa]]
  type = RNodeInterface
  interface_enabled = True
  outgoing = True
  port = COM3
  frequency = 433325000
  bandwidth = 125000
  txpower = 14
  spreadingfactor = 9
  codingrate = 5
  flow_control = False
```
*(⚠️ **Dikkat:** `port = COM3` kısmındaki `COM3` yerine Aygıt Yöneticisi'nde kendi bulduğunuz COM numarasını yazın).*

---

### 🐧 B. LINUX / DEBIAN / RASPBERRY PI KULLANICILARI İÇİN:

#### 1. Portunuzu Bulun:
- Terminali açın ve şu komutu yazın:
  ```bash
  ls /dev/ttyUSB* /dev/ttyACM*
  ```
- Çıkan yazı sizin port adınızdır (Örneğin: `/dev/ttyUSB0`).

> 💡 **Erişim Engeli (Permission Denied) Alırsanız:**  
> Terminale şu satırı yazarak izni açın: `sudo chmod 666 /dev/ttyUSB0`

#### 2. Config Dosyasını Açın ve Yapıştırın:
- Terminalde: `nano ~/.reticulum/config`
- `[interfaces]` altına ekleyin:

```ini
[[RNode LoRa]]
  type = RNodeInterface
  interface_enabled = True
  outgoing = True
  port = /dev/ttyUSB0
  frequency = 433325000
  bandwidth = 125000
  txpower = 14
  spreadingfactor = 9
  codingrate = 5
  flow_control = False
```
*(Kaydetmek için `Ctrl + O` ➔ `Enter`, çıkmak için `Ctrl + X`)*

---

## 📻 TX Power (`txpower`) Ayarı Nedir? (Ne İşe Yarar?)

Ayardaki `txpower = 14` satırı, cihazın **Radyo Çıkış Gücünü (Sinyal Yayma Şiddetini)** belirler:

- **`txpower` Yükseltilirse (Örn: 14 - 20 dBm):**
  - 🟢 **Daha Uzak Menzil:** Sinyal binaları, duvarları ve tepeleri daha kolay aşar. Kilometrelerce uzağa ulaşır.
  - 🔴 **Daha Fazla Pil Tüketimi:** Cihaz veri gönderirken daha fazla elektrik harcar, pil daha çabuk biter ve modül bir miktar ısınabilir.

- **`txpower` Düşürülürse (Örn: 2 - 10 dBm):**
  - 🟢 **Pil Tasarrufu:** Cihaz çok az elektrik tüketir, pil ömrü kat kat uzar.
  - 🔴 **Kısa Menzil:** Sinyal sadece yakın mesafedeki (ev içi, bahçe, aynı sokak) cihazlara ulaşır.

> 💡 **Tavsiye:** Türkiye ve Avrupa yasal 433 MHz standartlarına ve ideal pil/menzil dengesine en uygun değer **14 dBm** (25 milliwatt)'dır.

---

## 🎯 3. Bölüm: Çalıştırma ve Test

1. **Cihaz Durumunu Kontrol Edin:**
   - Windows (Komut Satırı / PowerShell):
     ```cmd
     rnodeconf COM3 --info
     ```
   - Linux (Terminal):
     ```bash
     rnodeconf /dev/ttyUSB0 --info
     ```
   *Ekranda `EEPROM checksum correct` yazıyorsa cihazınız tam doğrulama almıştır.*

2. **NomadNet Uygulamasını Başlatın:**
   ```bash
   nomadnet
   ```
   Artık şebekesiz, internetsiz RF üzerinden diğer düğümlerle mesajlaşabilirsiniz! 🚀
