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
    test_script = """python3 -c "
import nomadnet.ui.micron as micron 2>/dev/null or import nomadnetwork.ui.micron as micron 2>/dev/null
print('Micron module imported successfully')
" 2>/dev/null || python3 -c "
import sys
import os
for path in sys.path:
    for root, dirs, files in os.walk(path):
        if 'micron.py' in files:
            print('Found micron.py:', os.path.join(root, 'micron.py'))
"
"""
    out, err = run_ssh(test_script)
    print("Micron test output:\n", out)
    print("Err:\n", err)
