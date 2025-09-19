import socket

def test_bolt_port(host='127.0.0.1', port=7687):
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            print(f"Successfully connected to {host} on port {port}")
    except (socket.timeout, ConnectionRefusedError) as e:
        print(f"Connection to {host} on port {port} failed: {e}")

if __name__ == "__main__":
    test_bolt_port()