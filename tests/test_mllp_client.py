import threading
import socket
import time

from app.mllp.client import send_message, SB, EB, CR


def start_server(port_holder, received):
    srv = socket.socket()
    srv.bind(("localhost", 0))
    port_holder.append(srv.getsockname()[1])
    srv.listen(1)
    conn, _ = srv.accept()
    data = b""
    while not data.endswith(EB + CR):
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
    received.append(data)
    conn.sendall(SB + b"AA" + EB + CR)
    conn.close()
    srv.close()


def test_send_message():
    port_holder = []
    received = []
    t = threading.Thread(target=start_server, args=(port_holder, received))
    t.start()
    while not port_holder:
        time.sleep(0.05)
    ack = send_message("localhost", port_holder[0], "MSH|^~\\&|S|F|R|F|2020||ADT^A01|1|P|2.5\rPID|1||1")
    t.join()
    assert ack == "AA"
    assert received
    assert received[0].startswith(SB)

