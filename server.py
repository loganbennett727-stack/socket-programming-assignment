import socket
from contextlib import closing

HOST = "127.0.0.1"
PORT = 65432

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[-] Client {addr} disconnected.")
                break

            message = data.decode("utf-8").strip()
            print(f"[>] Received from {addr}: {message}")

            if message.lower() == "quit":
                response = "Goodbye! Closing connection."
                conn.sendall(response.encode("utf-8"))
                print(f"[!] Closing connection with {addr}.")
                break

            response = f"Server received: {message.upper()}"
            conn.sendall(response.encode("utf-8"))
            print(f"[<] Sent to {addr}: {response}")
    finally:
        conn.close()
        print(f"[x] Connection with {addr} closed.")

def main():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((HOST, PORT))
        except OSError as exc:
            print(f"[ERROR] Could not bind: {exc}")
            return

        server_socket.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")

        try:
            while True:
                print("[SERVER] Waiting for connection...")
                conn, addr = server_socket.accept()
                handle_client(conn, addr)
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down.")
        finally:
            print("[SERVER] Server socket closed.")

if __name__ == "__main__":
    main()
