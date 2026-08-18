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
    ps_out, _ = run_ssh("ps aux | grep server.py | grep -v grep")
    print("PS Check Output:\n", ps_out)
    
    log_out, _ = run_ssh("cat /tmp/server.log 2>/dev/null || echo 'No log file'")
    print("Server Log:\n", log_out)
    
    # Restart cleanly
    run_ssh("pkill -9 -f 'server.py' 2>/dev/null")
    cmd = "cd ~/DIY-RNode-ESP32-LoRa/micron_app && nohup python3 server.py > /tmp/server.log 2>&1 &"
    out, err = run_ssh(cmd)
    print("Restart cmd output:\n", out)
    print("Restart cmd err:\n", err)
    
    # Verify process after restart
    ps_after, _ = run_ssh("ps aux | grep server.py | grep -v grep")
    print("PS After Restart:\n", ps_after)
