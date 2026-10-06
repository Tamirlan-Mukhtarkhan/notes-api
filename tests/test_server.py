import sys, os, threading, unittest, json
import urllib.request, urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from server import make_server


class TestNotesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = make_server(0)
        cls.port = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def get(self, path):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    def post(self, path, data):
        body = json.dumps(data).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    def delete(self, path):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    def test_healthz_is_ok(self):
        status, body = self.get("/healthz")
        self.assertEqual(status, 201)
        self.assertTrue(body.strip())

    def test_root_answers(self):
        status, _ = self.get("/")
        self.assertEqual(status, 200)

    def test_notes_returns_list(self):
        status, body = self.get("/notes")
        self.assertEqual(status, 200)
        notes = json.loads(body)
        self.assertIsInstance(notes, list)
        self.assertGreater(len(notes), 0)

    def test_post_note_adds_it(self):
        before = json.loads(self.get("/notes")[1])
        status, body = self.post("/notes", {"text": "new test note"})
        self.assertEqual(status, 201)
        after = json.loads(body)
        self.assertEqual(len(after), len(before) + 1)
        self.assertIn("new test note", after)

    def test_delete_note_removes_it(self):
        self.post("/notes", {"text": "to be deleted"})
        before = json.loads(self.get("/notes")[1])
        idx = before.index("to be deleted")
        status, body = self.delete(f"/notes/{idx}")
        self.assertEqual(status, 200)
        after = json.loads(body)
        self.assertNotIn("to be deleted", after)

    def test_post_empty_text_is_rejected(self):
        status, _ = self.post("/notes", {"text": "   "})
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
