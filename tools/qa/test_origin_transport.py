import unittest
from http.server import BaseHTTPRequestHandler
from urllib.request import urlopen
from origin_transport import OriginTransport

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"known-online")
    def log_message(self,*args):
        pass

class OriginTransportTests(unittest.TestCase):
    def test_actual_cut_and_same_origin_restore(self):
        t=OriginTransport(Handler)
        self.addCleanup(t.stop)
        t.start()
        origin=t.origin
        with urlopen(origin,timeout=2) as r:
            self.assertEqual(r.read(),b"known-online")
        t.stop()
        t.assert_closed()
        t.start()
        self.assertEqual(t.origin,origin)
        with urlopen(origin,timeout=2) as r:
            self.assertEqual(r.read(),b"known-online")

    def test_live_origin_cannot_be_declared_closed(self):
        t=OriginTransport(Handler)
        self.addCleanup(t.stop)
        t.start()
        with self.assertRaises(AssertionError):
            t.assert_closed()
