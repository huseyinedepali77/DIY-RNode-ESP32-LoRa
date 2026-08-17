#!/usr/bin/env python3
# Micron Web Composer & Automatic RNode Publisher Server for Debian
import http.server
import socketserver
import json
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NOMADNET_PAGES_DIR = os.path.expanduser("~/.nomadnet/storage/pages")

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

                response = {
                    "status": "success",
                    "message": f"'{filename}' sayfası Çınarcık RNode LoRa ağında başarıyla yayınlandı!",
                    "path": target_path
                }
                self.send_response(200)
            except Exception as e:
                response = {
                    "status": "error",
                    "message": f"Yayınlama hatası: {str(e)}"
                }
                self.send_response(500)

            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    os.makedirs(NOMADNET_PAGES_DIR, exist_ok=True)
    print(f"==================================================")
    print(f"📻 Çınarcık RNode Micron Publisher Server (Debian)")
    print(f"==================================================")
    print(f"Web Editör: http://localhost:{PORT}")
    print(f"Yerel Ağ Erişimi: http://0.0.0.0:{PORT}")
    print(f"NomadNet Yayın Dizin: {NOMADNET_PAGES_DIR}")
    print(f"==================================================")
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MicronHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu durduruldu.")
