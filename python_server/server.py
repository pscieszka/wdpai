import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


class SimpleRequestHandler(BaseHTTPRequestHandler):
    user_list = [{'id': 0, 'first_name': 'Michal', 'last_name': 'Mucha', 'role': 'instructor'}]
    id = 1 

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(SimpleRequestHandler.user_list).encode())

    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        new_user: dict = json.loads(post_data.decode())

        new_user['id'] = SimpleRequestHandler.id
        SimpleRequestHandler.id += 1
        SimpleRequestHandler.user_list.append(new_user)

        response: dict = {
            "Message": "Successfull - user add",
            "updated_list:": SimpleRequestHandler.user_list
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(new_user).encode())

    def do_DELETE(self) -> None:
        path = self.path.strip("/")
        try:
            id = int(path)

            user_to_delete = None
            for user in SimpleRequestHandler.user_list:
                if user['id'] == id:
                    user_to_delete = user
                    break

            if user_to_delete is None:
                self.send_response(404) 
            else:
                SimpleRequestHandler.user_list.remove(user_to_delete)  
                self.send_response(200)

            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        except ValueError:
            self.send_response(400)
            self.end_headers()
        except Exception as e:
            self.send_response(500) 
            self.end_headers()

def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()



if __name__ == '__main__':
    run()