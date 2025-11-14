import struct
from .serialization import to_json, from_json

HEADER_STRUCT = struct.Struct("!I")

def send_message(sock, data):
    body = to_json(data)
    header = HEADER_STRUCT.pack(len(body))
    sock.sendall(header + body)

def recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket cerrado")
        buf += chunk
    return buf

def receive_message(sock):
    header = recv_exact(sock, HEADER_STRUCT.size)
    (length,) = HEADER_STRUCT.unpack(header)
    body = recv_exact(sock, length)
    return from_json(body)
