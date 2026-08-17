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
    # 1. Copy files to /root/.nomadnetwork/storage/pages/
    run_ssh("mkdir -p /root/.nomadnetwork/storage/pages && cp /root/.nomadnet/storage/pages/*.mu /root/.nomadnetwork/storage/pages/ 2>/dev/null || true")
    
    # 2. Check if index.mu exists, if not create default
    index_check, _ = run_ssh("ls /root/.nomadnetwork/storage/pages/index.mu 2>/dev/null")
    if not index_check.strip():
        sample_index = """# Çınarcık Mesh Düğümü - Ana Sayfa

> **Hoş Geldiniz!** -TA2LRW Hüseyin- Bu sayfa Çınarcık / Yalova RNode LoRa Mesh ağı üzerinden 433.325 MHz frekansında yayın yapmaktadır.

## Sayfa Menüsü
Aşağıdaki bağlantılara tıklayarak sayfalar arasında gezinebilirsiniz:

[ 1. Hakkımda ve Düğüm Bilgileri ](page://about.mu)
[ 2. Amatör Telsizcilik & Frekans Rehberi ](page://hamradio.mu)
[ 3. Acil Durum & Hayatta Kalma Rehberi ](page://survival.mu)

---
```
Düğüm Konumu: KN40NP Çınarcık / Yalova (24/7 Kesintisiz)
Frekans: 433.325 MHz (SF9 / BW 125 kHz / CR 4/5)
```
"""
        run_ssh(f"cat << 'EOF' > /root/.nomadnetwork/storage/pages/index.mu\n{sample_index}\nEOF")

    # 3. Read config and update
    config_content, _ = run_ssh("cat /root/.nomadnetwork/config")
    
    lines = config_content.splitlines()
    new_lines = []
    in_node = False
    
    for line in lines:
        l = line.strip()
        if l.startswith('[') and l.endswith(']'):
            in_node = (l == '[node]')
            new_lines.append(line)
        else:
            if in_node:
                if l.startswith('enable_node'):
                    new_lines.append('enable_node = True')
                elif l.startswith('node_name'):
                    new_lines.append('node_name = TA2LRW-Cinarcik')
                elif l.startswith('enable_pages'):
                    new_lines.append('enable_pages = True')
                elif l.startswith('pages_path'):
                    new_lines.append('pages_path = /root/.nomadnetwork/storage/pages')
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
    final_config = "\n".join(new_lines) + "\n"
    
    write_cmd = f"cat << 'EOF' > /root/.nomadnetwork/config\n{final_config}EOF"
    run_ssh(write_cmd)
    
    print("--- Config Update Complete ---")
    out_pages, _ = run_ssh("ls -la /root/.nomadnetwork/storage/pages/")
    print("Pages Directory Content:\n", out_pages)
