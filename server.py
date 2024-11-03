from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv, stdout, stderr
import os
import mimetypes
import sqlite3
from urllib.parse import parse_qs, urlparse
import json
import ssl  # Import SSL module

db_name = "data"

db = sqlite3.connect(f"{db_name}.db")
cursor = db.cursor()

BIND_HOST = "0.0.0.0"
PORT = 8008
DEFAULT_FILE_PATH = './index.html'
LOG_FILE = "server_output.log"
STATIC_DIR = './src'

# SSL certificate and key paths (change these paths to your own certificate and key)
CERT_FILE = "cert.pem"
KEY_FILE = "private.key"

def get_code_data(code: str):
    print("Processing code: " + code)
    try:
        cursor.execute('SELECT * FROM ids WHERE id=?', (code,))
        result = cursor.fetchone()
        cursor.execute('SELECT * FROM books WHERE id=?', (result[1],))
        result2 = cursor.fetchone()
    except TypeError:
        result = ('null', 'null', 'null', 'null')
        result2 = ('null', 'null', 'null', 'null', 'null', 'null')
    except:
        result = ('null', 'null', 'null', 'null')
        result2 = ('null', 'null', 'null', 'null', 'null', 'null')

    try:
        cursor.execute('SELECT * FROM borrows WHERE id=?', (code,))
        result3 = cursor.fetchone()
        result3[1]
    except:
        result3 = ('0', '0', 0, 0)

    json_data = {
        "id": result[0],
        "type": result[1],
        "donator": result[2],
        "donation_day": result[3],
        "title": result2[1],
        "author": result2[2],
        "year_published": result2[3],
        "description": result2[4],
        "use": result2[5],
        "borrower": result3[1],
        "borrow_date": result3[2],
        "borrow_expire": result3[3]
    }

    return json.dumps(json_data, ensure_ascii=False).encode('utf-8')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header('Location', '/about.html')
            self.end_headers()
        elif self.path == "/get":
            request_header = self.headers.get("Request")
            if request_header:
                self.write_response(get_code_data(request_header), content_type="text/plain; charset=utf-8")
        else:
            parsed_path = urlparse(self.path)
            file_path = '.' + parsed_path.path

            if parsed_path.path.startswith("/get") and parsed_path.query:
                params = parse_qs(parsed_path.query)
                code = params.get("code", [None])[0]
                if code:
                    self.write_response(get_code_data(code), content_type="text/plain; charset=utf-8")
                else:
                    self.send_error(400, "Missing 'code' parameter")
            elif os.path.exists(file_path):
                self.serve_static_file(file_path)
            else:
                self.send_error(404, "File not found")

    def serve_static_file(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type is None:
            mime_type = "text/plain"

        with open(file_path, 'rb') as file:
            content = file.read()

        self.send_response(200)
        self.send_header('Content-Type', f"{mime_type}; charset=utf-8")
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)

        try:
            body_decoded = body.decode('utf-8')
            print("Received POST data (UTF-8 decoded):", body_decoded)
        except UnicodeDecodeError:
            self.send_error(400, "Invalid UTF-8 encoding")
            return

        self.write_response(body, content_type="text/plain; charset=utf-8")

    def write_response(self, content, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

class Logger:
    def __init__(self, logfile):
        self.terminal = stdout
        self.logfile = open(logfile, 'a', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        pass

stdout = Logger(LOG_FILE)
stderr = stdout

if len(argv) > 1:
    arg = argv[1].split(":")
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f"Listening on https://{BIND_HOST}:{PORT}\n")

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

# Wrap the server socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

# Start the HTTPS server
httpd.serve_forever()
