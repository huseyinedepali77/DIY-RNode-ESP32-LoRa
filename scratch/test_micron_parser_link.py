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
    script = """python3 -c "
import nomadnet.ui.textui.MicronParser as MP
test_line1 = '`[`1. Hakkımda ve Düğüm Bilgileri`:/page/about.mu]'
test_line2 = '`[`1. Hakkımda ve Düğüm Bilgileri`about.mu]'
print('Parse 1:', MP.markup_to_attrmaps(test_line1))
print('Parse 2:', MP.markup_to_attrmaps(test_line2))
"
"""
    out, err = run_ssh(script)
    print("Result:\n", out)
    print("Err:\n", err)
