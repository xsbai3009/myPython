# test_demo.py
import unittest
import requests

class TestApprove(unittest.TestCase):
    def test_ddt(self):
        print('开始执行')
        resp = requests.get("http://httpbin.org/get?id=2").json()
        assert resp["args"]["id"] == "2"
        print('执行结束')
		

if __name__ == "__main__":
    unittest.main()