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
    cmd = "grep -rn 'page:' /usr/local/lib/python3.11/dist-packages/nomadnet/ | head -n 30"
    out, _ = run_ssh(cmd)
    print("Grep page: in NomadNet:\n", out)
    
    cmd2 = "grep -rn 'link' /usr/local/lib/python3.11/dist-packages/nomadnet/ui/ | head -n 30"
    out2, _ = run_ssh(cmd2)
    print("Grep link in NomadNet UI:\n", out2)
