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
from RNS.Utilities.rngit.util import MarkdownToMicron
m = MarkdownToMicron('')
print('LINK_RE pattern:', m.LINK_RE.pattern)
print('Formatted line:', repr(m.format_line('[1. Hakkımda](page://about.mu)')))
print('Formatted line relative:', repr(m.format_line('[1. Hakkımda](about.mu)')))
"
"""
    out, err = run_ssh(script)
    print("Result:\n", out)
    print("Err:\n", err)
