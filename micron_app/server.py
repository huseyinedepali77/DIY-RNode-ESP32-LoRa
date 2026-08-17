#!/usr/bin/env python3
# Safe Micron File Publisher for Reticulum / NomadNet
import http.server
import socketserver
import json
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Try .nomadnetwork first, then .nomadnet
NOMADNET_PAGES_DIR = os.path.expanduser("~/.nomadnetwork/storage/pages")
if not os.path.exists(os.path.expanduser("~/.nomadnetwork")):
    NOMADNET_PAGES_DIR = os.path.expanduser("~/.nomadnet/storage/pages")

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class MicronHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/publish':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', 'index.mu')
                content = data.get('content', '')

                if not filename.endswith('.mu'):
                    filename += '.mu'

                os.makedirs(NOMADNET_PAGES_DIR, exist_ok=True)
                target_path = os.path.join(NOMADNET_PAGES_DIR, filename)

                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Copy to both locations for safety
                alt_dir = os.path.expanduser("~/.nomadnet/storage/pages")
                os.makedirs(alt_dir, exist_ok=True)
                with open(os.path.join(alt_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(content)

                response = {
                    "status": "success",
                    "message": f"'{filename}' dosyasi {target_path} klasorune kaydedildi!",
                    "path": target_path
                }
                self.send_response(200)
            except Exception as e:
                response = {
                    "status": "error",
                    "message": f"Dosya kaydetme hatasi: {str(e)}"
                }
                self.send_response(500)

            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    os.makedirs(NOMADNET_PAGES_DIR, exist_ok=True)
    
    server_port = PORT
    httpd = None
    for try_port in [8080, 8088, 8090, 8888]:
        try:
            httpd = ReuseTCPServer(("", try_port), MicronHandler)
            server_port = try_port
            break
        except OSError:
            continue

    if httpd:
        print(f"==================================================")
        print(f"Safe Micron Page Publisher (NomadNet)")
        print(f"==================================================")
        print(f"Web Editor: http://localhost:{server_port}")
        print(f"Yerel Ag Erisimi: http://0.0.0.0:{server_port}")
        print(f"Hedef Klasor: {NOMADNET_PAGES_DIR}")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu durduruldu.")
    else:
        print("Hata: Uygun port bulunamadi.")
