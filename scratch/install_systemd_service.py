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
    service_content = """[Unit]
Description=Micron Page Studio Publisher Service for Reticulum / NomadNet
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/DIY-RNode-ESP32-LoRa/micron_app
ExecStart=/usr/bin/python3 /root/DIY-RNode-ESP32-LoRa/micron_app/server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

    run_ssh("cat << 'EOF' > /etc/systemd/system/micron-studio.service\n" + service_content + "\nEOF")
    out_reload, _ = run_ssh("systemctl daemon-reload && systemctl enable micron-studio.service && systemctl restart micron-studio.service")
    out_status, _ = run_ssh("systemctl status micron-studio.service --no-pager")
    print("Service Status Output:\n", out_status)
