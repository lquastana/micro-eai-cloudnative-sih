"""Basic MLLP server implementation using asyncio."""
import asyncio

from ..hl7.parser import parse_hl7_message
from ..jobs.tasks import process_message

SB = b"\x0b"
EB = b"\x1c"
CR = b"\x0d"


class MLLPProtocol(asyncio.Protocol):
    def __init__(self):
        self.buffer = b""

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        self.buffer += data
        if self.buffer.endswith(EB + CR):
            payload = self.buffer.strip(SB + EB + CR)
            message = payload.decode()
            parse_hl7_message(message)
            process_message.delay(message)
            ack = SB + b"AA" + EB + CR
            self.transport.write(ack)
            self.buffer = b""


def serve(host: str = "0.0.0.0", port: int = 2575):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MLLPProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
