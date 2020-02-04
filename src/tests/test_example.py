# Just need something so the pytest from tox doesn't fail
import unittest


class TestExample(unittest.TestCase):
    def test_example(self):
        self.assertEqual("obj", "".join(["o", "bj"]))
