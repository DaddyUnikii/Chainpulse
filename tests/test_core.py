import json
import os
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from chainpulse.cli import render_table
from chainpulse.core import check, check_all


os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")


class FakeRpc(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        result = {"eth_blockNumber": "0x10", "eth_chainId": "0x38"}[body["method"]]
        data = json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class ChainPulseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), FakeRpc)
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_healthy_endpoint(self):
        r = check("fake", self.url)
        self.assertTrue(r.ok)
        self.assertEqual(r.block, 16)
        self.assertEqual(r.chain_id, 56)

    def test_dead_endpoint(self):
        r = check("dead", "http://127.0.0.1:1", timeout=1)
        self.assertFalse(r.ok)
        self.assertIsNotNone(r.error)

    def test_failures_sorted_last(self):
        results = check_all({"dead": "http://127.0.0.1:1", "fake": self.url}, timeout=1)
        self.assertEqual([r.name for r in results], ["fake", "dead"])

    def test_table_renders(self):
        table = render_table([check("fake", self.url)], color=False)
        self.assertIn("1/1 endpoints healthy", table)


if __name__ == "__main__":
    unittest.main()
