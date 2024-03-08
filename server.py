from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json

# Your API key and Username
API_KEY = "YOURAPIKEY"
USERNAME = "YOURUSERNAME"


class LastFMServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  
        self.end_headers()

        if self.path == '/currently_playing':
            try:
                response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USERNAME}&api_key={API_KEY}&format=json')
                data = response.json()
                currently_playing = {
                    "artist": data['recenttracks']['track'][0]['artist']['#text'],
                    "track": data['recenttracks']['track'][0]['name']
                }
                self.wfile.write(json.dumps(currently_playing).encode())
            except Exception as e:
                print("Error:", e)
                self.wfile.write(json.dumps({"error": "Unable to fetch currently playing song"}).encode())
        else:
            self.wfile.write(b'404 Not Found')

def run_server():
    server_address = ('YOURIPADDRESS', 8000)  # Replace with your IP address and Port
    httpd = HTTPServer(server_address, LastFMServerHandler)
    print(f'Server running on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
