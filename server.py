import socket
import threading
import utils

from routerEngine import REngine
from responser import HttpResponseBuilder
from resourceReader import ResourceReader

HOST = "127.0.0.1"
PORT = 8180


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.listen()

    def start_server(self):
        print("[Server started]....")
        self._listen_for_connection()
        pass

    def stop_server(self):
        self.server_socket.close()
        print("[Server stopped]....")

    def _listen_for_connection(self):
        print("[Server listening for connections].... ")
        while True:
            conn, addr = self.server_socket.accept()
            print("[New connection established]....")
            conn_thread = threading.Thread(target=self._handle_connection, args=(conn, addr))
            conn_thread.start()
            print("Running threads: {}".format(threading.active_count()))

    def _handle_connection(self, conn, addr):
        while True:
            received_data = conn.recv(1024).decode()
            if not received_data or received_data.find("keep-alive") != -1:
                break

        router = REngine()
        reader = ResourceReader()
        requested_path = utils.extract_path_from_request(received_data)
        path_to_file = router.process_path(requested_path)
        body = reader.read_resource_file(path_to_file)

        resp = HttpResponseBuilder().build(
            body.get("status"),
            headers("Content-Type", body.get("resource_type")),
            body.get("body")
        )
        print(resp)
        conn.send(resp)
        conn.close()


def headers(key: str, value) -> dict:
    header = dict()
    header["Server"] = "Simple server"
    header[key] = value
    return header


if __name__ == '__main__':
    server = Server()
    server.start_server()
