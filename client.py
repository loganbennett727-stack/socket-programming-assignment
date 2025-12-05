import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432

def main():
    host = input(f"Enter server host [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST

    port_input = input(f"Enter server port [{DEFAULT_PORT}]: ").strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print("[ERROR] Invalid port number. Using default.")
            port = DEFAULT_PORT
    else:
        port = DEFAULT_PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)

        try:
            print(f"[CLIENT] Connecting to {host}:{port} ...")
            sock.connect((host, port))
            print("[CLIENT] Connected! Type messages. 'quit' to exit.\n")
        except Exception as exc:
            print(f"[ERROR] {exc}")
            return

        try:
            while True:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                sock.sendall(user_input.encode("utf-8"))

                try:
                    data = sock.recv(1024)
                except socket.timeout:
                    print("[CLIENT] No response (timeout).")
                    continue

                if not data:
                    print("[CLIENT] Server closed connection.")
                    break

                response = data.decode("utf-8").strip()
                print(f"Server: {response}")

                if user_input.lower() == "quit":
                    print("[CLIENT] Exiting.")
                    break
        finally:
            print("[CLIENT] Disconnected.")

if __name__ == "__main__":
    main()
