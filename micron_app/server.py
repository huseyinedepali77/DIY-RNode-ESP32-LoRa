#!/usr/bin/env python3
# Safe Micron File Publisher & Persistent Server for Reticulum / NomadNet
import http.server
import socketserver
import json
import os
import re

try:
    from RNS.Utilities.rngit.util import MarkdownToMicron
    HAS_CONVERTER = True
except Exception:
    HAS_CONVERTER = False

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

NOMADNET_PAGES_DIR = os.path.expanduser("~/.nomadnetwork/storage/pages")
if not os.path.exists(os.path.expanduser("~/.nomadnetwork")):
    NOMADNET_PAGES_DIR = os.path.expanduser("~/.nomadnet/storage/pages")

def sanitize_links(text):
    if not text: return text
    def clean_link(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        if url.startswith(":/page/"): url = url[7:]
        elif url.startswith("/page/"): url = url[6:]
        elif url.startswith("page://"): url = url[7:]
        return f"[{label}]({url})"
    return re.sub(r'\[\s*([^\]]+?)\s*\]\(([^)]+)\)', clean_link, text)

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class MicronHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/pages':
            pages_data = {}
            os.makedirs(NOMADNET_PAGES_DIR, exist_ok=True)
            try:
                for fname in os.listdir(NOMADNET_PAGES_DIR):
                    if fname.endswith('.mu'):
                        src_path = os.path.join(NOMADNET_PAGES_DIR, fname + ".src")
                        mu_path = os.path.join(NOMADNET_PAGES_DIR, fname)
                        
                        if os.path.exists(src_path):
                            with open(src_path, 'r', encoding='utf-8', errors='replace') as f:
                                pages_data[fname] = f.read()
                        elif os.path.exists(mu_path):
                            with open(mu_path, 'r', encoding='utf-8', errors='replace') as f:
                                pages_data[fname] = f.read()
            except Exception as e:
                pages_data = {"error": str(e)}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"pages": pages_data}).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/publish':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', 'index.mu')
                raw_content = data.get('content', '')

                if not filename.endswith('.mu'):
                    filename += '.mu'

                # Automatically sanitize markdown link syntax
                clean_content = sanitize_links(raw_content)

                # Save clean markdown source
                src_path = os.path.join(NOMADNET_PAGES_DIR, filename + ".src")
                with open(src_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)

                if HAS_CONVERTER:
                    try:
                        converter = MarkdownToMicron()
                        final_content = converter.format_block(clean_content)
                    except Exception:
                        final_content = clean_content
                else:
                    final_content = clean_content

                os.makedirs(NOMADNET_PAGES_DIR, exist_ok=True)
                target_path = os.path.join(NOMADNET_PAGES_DIR, filename)

                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)

                # Mirror save to both directories
                alt_dir = os.path.expanduser("~/.nomadnet/storage/pages")
                os.makedirs(alt_dir, exist_ok=True)
                with open(os.path.join(alt_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(final_content)
                with open(os.path.join(alt_dir, filename + ".src"), 'w', encoding='utf-8') as f:
                    f.write(clean_content)

                response = {
                    "status": "success",
                    "message": f"'{filename}' derlenip kaydedildi!",
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

        elif self.path == '/api/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', '')

                if filename and filename != 'index.mu':
                    for d in [NOMADNET_PAGES_DIR, os.path.expanduser("~/.nomadnet/storage/pages")]:
                        p1 = os.path.join(d, filename)
                        p2 = os.path.join(d, filename + ".src")
                        if os.path.exists(p1): os.remove(p1)
                        if os.path.exists(p2): os.remove(p2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()

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
        print(f"Safe Micron Page Publisher & Compiler (NomadNet)")
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
