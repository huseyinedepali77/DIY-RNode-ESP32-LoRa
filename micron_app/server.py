#!/usr/bin/env python3
# Micron Web Composer & Parser Server for Debian RNode / Reticulum
import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    print(f"==================================================")
    print(f"📻 Micron Web Composer for Debian RNode / Reticulum")
    print(f"==================================================")
    print(f"Web Arayüzü Başlatıldı: http://localhost:{PORT}")
    print(f"Yerel Ağ Erişimi: http://0.0.0.0:{PORT}")
    print(f"Çıkmak için: Ctrl+C")
    print(f"==================================================")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu durduruldu.")
