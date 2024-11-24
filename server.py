from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv, stdout, stderr
import os
import mimetypes
import sqlite3
from urllib.parse import parse_qs, urlparse
import json
import ssl  # Import SSL module
from search import search_books, normalize_unicode, all_books
from hashlib import sha256

db_name = "data"

db = sqlite3.connect(f"{db_name}.db")
cursor = db.cursor()

BIND_HOST = "0.0.0.0"
PORT = 443
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

def get_search_data(idstr: str):
    ids = search_books(cursor, idstr, 55)

    valid_ids = []
    bktypes = []
    ranks = []
    titles = []
    for i in range(len(ids[0])):
        valid_ids.append(ids[0][i])
        bktypes.append(ids[1][i][0])
        ranks.append(ids[1][i][1])

        cursor.execute("SELECT title FROM books WHERE id=?", (ids[1][i][0],))
        titles.append(cursor.fetchone()[0])

    json_data = {
        "valid_ids": valid_ids,
        "bktypes": bktypes,
        "ranks": ranks,
        "titles": titles
    }

    return json.dumps(json_data, ensure_ascii=False).encode('utf-8')

def get_user_data(username: str):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    userdata = cursor.fetchone() # ("nautilus", "123", "Nautilus4K", 1732372092, None)
    # print(userdata)
    if (userdata == None):
        userdata = [None, None, None, None, None]
    else: userdata = list(userdata)
    if (userdata[2] == None): userdata[2] = userdata[0]

    json_data = {
        "username": userdata[0],
        # "password": userdata[1],  # Dangerous. Could be used to some degree of advantages
        "name": userdata[2],
        "date": userdata[3],
        # "phone": userdata[4]  # Uneeded. Probably just wasted some more bandwidths with this on.
                                # Also has to limit the amount of personal data could be accessed
                                # via API calls
    }

    return json.dumps(json_data, ensure_ascii=False).encode('utf-8')

def check_login_credentials(username: str, passwd: str):
    hashedpass = sha256(passwd.encode("utf-8")).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    userdata = cursor.fetchone() # ("nautilus", "123", "Nautilus4K", 1732372092, None)
    corr = True

    # If no user is found to be matched
    if (userdata == None):
        corr = False
    elif (userdata[1] != hashedpass):
        corr = False

    json_data = {
        "username": username,
        "correct": corr
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
                request_header = self.headers.get("Search")
                if request_header:
                    # ids = search_books(cursor, request_header)
                    # for i in range(len(ids[0])):
                    #     valid_id = ids[0][i]
                    #     bktype = ids[1][i][0]
                    #     rank = ids[1][i][1]
                    #     print(f"id: {valid_id} | type: {bktype} | confidence: {rank}%")
                    # try:
                    #     self.write_response(str(ids[0]).encode('utf-8'), content_type="text/plain; charset=utf-8")
                    # except ssl.SSLEOFError:
                    #     print("Some random error idk")
                    self.write_response(get_search_data(request_header), content_type="text/plain; charset=utf-8")
                else:
                    request_header = self.headers.get("Username")
                    if request_header:
                        self.write_response(get_user_data(request_header), content_type="text/plain; charset=utf-8")
        elif self.path == "/logincheck":
            username = self.headers.get("Username")
            passwd = self.headers.get("Password")
            if username and passwd:
                # If username and passwd are all supplied. Now check for matches
                self.write_response(check_login_credentials(username, passwd), content_type="text/plain; charset=utf-8")
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
                # self.send_error(404, "File not found")
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()

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
        print("-----------------------------------")
        print("Sent back content: ")
        print("     Content: "+str(content))
        print("     Content-Type: "+str(content_type))
        print("     Content-Length: "+str(len(content)))
        print("-----------------------------------")

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
