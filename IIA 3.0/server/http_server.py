from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('0.0.0.0', 80), SimpleHTTPRequestHandler)
server.serve_forever()