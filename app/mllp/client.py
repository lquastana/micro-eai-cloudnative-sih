import socket
from pathlib import Path

SB = b"\x0b"
EB = b"\x1c"
CR = b"\x0d"

def send_message(host: str, port: int, message: str, timeout: float = 5.0) -> str:
    """Send a single HL7 message via MLLP and return the ACK code."""
    if "\n" in message and "\r" not in message:
        message = message.replace("\n", "\r")
    payload = SB + message.encode() + EB + CR
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall(payload)
        data = b""
        while not data.endswith(EB + CR):
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
    ack = data[len(SB):-len(EB + CR)].decode()
    return ack


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Send an HL7 message via MLLP")
    parser.add_argument("file", help="Path to HL7 message file")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=2575)
    args = parser.parse_args()

    text = Path(args.file).read_text()
    ack = send_message(args.host, args.port, text)
    print(f"ACK: {ack}")


if __name__ == "__main__":
    main()
