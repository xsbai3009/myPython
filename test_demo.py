# test_demo.py
import unittest
import requests

class TestApprove(unittest.TestCase):
    def test_ddt(self):
        print('开始执行')
        resp = requests.get("http://httpbin.org/get?id=2").json()
        assert resp["args"]["id"] == "2"
        print('执行结束')
		print('收队')
	
	def test01_login(self):
		print('登陆成功')
		

if __name__ == "__main__":
    unittest.main()
	print('执行结束')