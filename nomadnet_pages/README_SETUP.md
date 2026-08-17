# 🌐 Debian Üzerinde 24/7 Çalışan NomadNet Micron Sayfa Sunucusu Kurulumu

Bu klasördeki `.mu` (Micron) sayfaları, Reticulum & RNode LoRa ağındaki diğer kullanıcıların NomadNet ekranından **sizin sunucunuzu ziyaret edip gezinebilmesini** sağlar.

---

## 🛠️ Debian Üzerinde Adım Adım Kurulum:

### 1. Adım: Micron Sayfalarını NomadNet Klasörüne Kopyalayın
Debian terminalinizde şu komutları çalıştırın:

```bash
# NomadNet sayfaları klasörünü oluşturun
mkdir -p ~/.nomadnet/storage/pages

# Hazırladığımız .mu sayfalarını kopyalayın
cp nomadnet_pages/*.mu ~/.nomadnet/storage/pages/
```

---

### 2. Adım: NomadNet Node Hosting Özelliğini Açın
NomadNet ayar dosyasını açın:

```bash
nano ~/.nomadnet/config
```

Aşağıdaki satırları bulun veya ekleyin:

```ini
[node]
enable_node = True
node_name = Istanbul RNode Mesh Node
enable_pages = True
pages_path = ~/.nomadnet/storage/pages
```

---

### 3. Adım: Sunucuyu 24/7 Kesintisiz Arka Planda Çalıştırma (Systemd Service)

Debian cihazınız her açıldığında sayfa sunucunuzun otomatik başlaması için bir servis oluşturun:

```bash
sudo nano /etc/systemd/system/nomadnet-host.service
```

İçine şu satırları yapıştırın:

```ini
[Unit]
Description=NomadNet 24/7 Mesh Page Server
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/nomadnet --daemon
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Servisi aktif edin ve başlatın:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nomadnet-host.service
sudo systemctl start nomadnet-host.service
```

---

## 📲 Diğer Kullanıcılar Sayfalarınıza Nasıl Ulaşacak?

Ağdaki (LoRa, HaLow veya Ethernet üzerinden bağlı) herhangi bir kullanıcı kendi NomadNet ekranını açtığında:

1. **`Network` ➔ `Nodes`** sekmesine girecek.
2. Sizin düğümünüzün adını (**`Istanbul RNode Mesh Node`**) seçecek.
3. **`Pages`** butonuna tıkladığında sizin hazırladığınız **Ana Sayfa (index.mu)**, **Hakkımda**, **Amatör Telsizcilik** ve **Hayatta Kalma Rehberi** sayfalarında bağlantılara tıklayarak gezinecektir! 🚀
