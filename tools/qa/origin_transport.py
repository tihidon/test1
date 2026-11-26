"""QA-only origin transport. One server owner, same port across restarts."""
import errno
from http.server import ThreadingHTTPServer
import socket
import threading

class OriginTransport:
    def __init__(self, handler):
        self.handler=handler
        self.port=0
        self.server=None
        self.thread=None

    def start(self):
        if self.server is not None:
            raise RuntimeError("origin already running")
        server=ThreadingHTTPServer(("127.0.0.1",self.port),self.handler)
        self.port=server.server_port
        self.server=server
        self.thread=threading.Thread(target=server.serve_forever,daemon=True)
        self.thread.start()

    def stop(self):
        if self.server is None:
            return
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        if self.thread.is_alive():
            raise RuntimeError("origin server thread still running")
        self.server=None
        self.thread=None

    @property
    def origin(self):
        if not self.port:
            raise RuntimeError("origin not initialized")
        return f"http://127.0.0.1:{self.port}"

    def assert_closed(self):
        if self.server is not None:
            raise AssertionError("origin server not stopped")
        try:
            with socket.create_connection(("127.0.0.1",self.port),timeout=2):
                pass
        except OSError as exc:
            if exc.errno==errno.ECONNREFUSED:
                return
            raise
        raise AssertionError("origin port still accepts connections")
