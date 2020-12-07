from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import datetime

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!
    def do_POST(self):
        global con
        cur = con.cursor()
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode("utf-8")
        cur.execute('INSERT INTO \"table_name\" (timestamp, data) VALUES (\'' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  + '\', \'' + str(body) + '\');')
        cur.close()
        self._set_headers()
        self.wfile.write(self._html("POST!"))

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

con = psycopg2.connect(
    host="postgrya",
    database="fbk",
    user="postgres"
    )
con.set_session(autocommit=True)
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS public.\"table_name\" ("timestamp" timestamp without time zone NOT NULL, data character(256) COLLATE pg_catalog."default" NOT NULL);')
cur.close()

if __name__ == "__main__":
  run(addr="0.0.0.0", port=5000)
