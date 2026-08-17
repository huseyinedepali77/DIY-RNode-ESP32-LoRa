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
import re
from RNS.Utilities.rngit.util import MarkdownToMicron

def sanitize_links(text):
    if not text: return text
    def clean_link(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        if url.startswith(':/page/'): url = url[7:]
        elif url.startswith('/page/'): url = url[6:]
        elif url.startswith('page://'): url = url[7:]
        return f'[{label}]({url})'
    return re.sub(r'\\[\\s*([^\\]]+?)\\s*\\]\\(([^)]+)\\)', clean_link, text)

raw_user_text = '''[ 1. Hakkımda ve Düğüm Bilgileri ](:/page/about.mu)
[ 2. Amatör Telsizcilik & Frekans Rehberi ](:/page/hamradio.mu)
[ 3. Acil Durum & Hayatta Kalma Rehberi ](:/page/survival.mu)'''

sanitized = sanitize_links(raw_user_text)
compiled = MarkdownToMicron().format_block(sanitized)

print('--- Cleaned Source ---')
print(sanitized)
print('--- Compiled Micron ---')
print(repr(compiled))
"
"""
    out, err = run_ssh(script)
    print("Output:\n", out)
    print("Err:\n", err)
