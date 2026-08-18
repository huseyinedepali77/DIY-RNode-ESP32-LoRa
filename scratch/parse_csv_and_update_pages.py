import csv
import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

csv_file_path = r"C:\Users\Hüseyin\Desktop\md390\Channels.csv"

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
    repeaters = []
    simplex = []
    special = []

    with open(csv_file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            name = row.get("Channel Name", "").strip()
            rx = row.get("Rx Frequency", "").strip().replace("\t", "").replace(",", ".")
            tx = row.get("Tx Frequency", "").strip().replace("\t", "").replace(",", ".")
            tone = row.get("TX Tone", "").strip().replace(",", ".")

            if not name or not rx:
                continue

            if rx != tx:
                repeaters.append((name, rx, tx, tone))
            else:
                if "APRS" in name or "ISS" in name or "SSTV" in name or "RTTY" in name:
                    special.append((name, rx))
                elif name.startswith("CB-"):
                    special.append((name, rx))
                else:
                    simplex.append((name, rx))

    # Format freq_tr.mu markdown
    md_lines = []
    md_lines.append("# Türkiye Telsiz Röle ve Frekans Rehberi\n")
    md_lines.append("> **Marmara ve Türkiye Geneli VHF/UHF Röle, Simplex ve Acil Durum Frekans Listesi**\n")
    
    md_lines.append("## Marmara ve Türkiye Geneli Röleler\n")
    md_lines.append("| Bölge / Kod | Rx (MHz) | Tx (MHz) | Ton (Hz) |")
    md_lines.append("| :--- | :--- | :--- | :--- |")
    for r in repeaters[:35]:  # Top 35 repeaters for MTU efficiency
        tone_str = r[3] if r[3] and r[3] != "None" else "-"
        md_lines.append(f"| **{r[0]}** | {r[1]} | {r[2]} | {tone_str} |")

    md_lines.append("\n## Acil Durum, APRS & Uydu Frekansları\n")
    md_lines.append("| Kanal / Mod | Frekans (MHz) |")
    md_lines.append("| :--- | :--- |")
    for s in special[:15]:
        md_lines.append(f"| **{s[0]}** | {s[1]} |")

    md_lines.append("\n## Sık Kullanılan Simplex Frekanslar\n")
    md_lines.append("| Kanal Kod | Frekans (MHz) |")
    md_lines.append("| :--- | :--- |")
    for sx in simplex[:15]:
        md_lines.append(f"| **{sx[0]}** | {sx[1]} |")

    md_lines.append("\n[Ana Sayfaya Dön](index.mu)\n")

    freq_tr_content = "\n".join(md_lines)

    # Index page with link to freq_tr.mu
    index_content = """# Çınarcık Mesh Düğümü - Ana Sayfa

> **Hoş Geldiniz!** -TA2LRW Hüseyin- Bu sayfa Çınarcık / Yalova RNode LoRa Mesh ağı üzerinden 433.325 MHz frekansında yayın yapmaktadır.

## Sayfa Menüsü
Aşağıdaki bağlantılara tıklayarak sayfalar arasında gezinebilirsiniz:

[1. Hakkımda ve Düğüm Bilgileri](about.mu)
[2. Amatör Telsizcilik & Frekans Rehberi](hamradio.mu)
[3. Acil Durum & Hayatta Kalma Rehberi](survival.mu)
[4. Türkiye Telsiz Röle & Frekans Listesi](freq_tr.mu)

---
```
Düğüm Konumu: KN40NP Çınarcık / Yalova (24/7 Kesintisiz)
Frekans: 433.325 MHz (SF9 / BW 125 kHz / CR 4/5)
```
"""

    remote_code = """
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
    return re.sub(r'\\[\\s*([^\\]]+?)\\s*\\]\\(([^)]+)\\)', clean_link, text)

freq_tr_md = '''""" + freq_tr_content.replace("'", "\\'") + """'''
index_md = '''""" + index_content.replace("'", "\\'") + """'''

dirs = ["/root/.nomadnetwork/storage/pages", "/root/.nomadnet/storage/pages"]
for d in dirs:
    os.makedirs(d, exist_ok=True)

converter = MarkdownToMicron()

c_idx = converter.format_block(sanitize_links(index_md))
for d in dirs:
    with open(os.path.join(d, "index.mu.src"), "w", encoding="utf-8") as f: f.write(index_md)
    with open(os.path.join(d, "index.mu"), "w", encoding="utf-8") as f: f.write(c_idx)

c_freq = converter.format_block(sanitize_links(freq_tr_md))
for d in dirs:
    with open(os.path.join(d, "freq_tr.mu.src"), "w", encoding="utf-8") as f: f.write(freq_tr_md)
    with open(os.path.join(d, "freq_tr.mu"), "w", encoding="utf-8") as f: f.write(c_freq)

print("freq_tr.mu and index.mu updated successfully!")
"""

    run_ssh("cat << 'EOF' > /root/update_freq_tr.py\n" + remote_code + "\nEOF")
    out, err = run_ssh("python3 /root/update_freq_tr.py")
    print("Output:\n", out)
    print("Err:\n", err)

    # Restart server.py cleanly
    run_ssh("pkill -9 -f 'server.py' 2>/dev/null")
    cmd = "cd ~/DIY-RNode-ESP32-LoRa/micron_app && nohup python3 server.py > /tmp/server.log 2>&1 &"
    out_srv, _ = run_ssh(cmd)
    print("Server restart done!")
