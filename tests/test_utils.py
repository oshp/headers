import unittest
import os

from lib.utils.util import load_env_config
from lib.utils.util import get_dictsites


class TestUtils(unittest.TestCase):

    def test_default_env_settings(self):
        load_env_config()

        self.assertEqual("root", os.getenv("MYSQL_USERNAME"))
        self.assertEqual("password", os.getenv("MYSQL_PASSWORD"))
        self.assertEqual("localhost", os.getenv("MYSQL_HOST"))
        self.assertEqual("headers", os.getenv("MYSQL_DATABASE"))

    def test_custom_env_settings(self):
        os.environ['MYSQL_USERNAME'] = "custom_user"
        os.environ['MYSQL_PASSWORD'] = "custom_password"
        os.environ['MYSQL_HOST'] = "custom_host"
        os.environ['MYSQL_DATABASE'] = "custom_db"

        load_env_config()

        self.assertEqual("custom_user", os.getenv("MYSQL_USERNAME"))
        self.assertEqual("custom_password", os.getenv("MYSQL_PASSWORD"))
        self.assertEqual("custom_host", os.getenv("MYSQL_HOST"))
        self.assertEqual("custom_db", os.getenv("MYSQL_DATABASE"))

    @classmethod
    def tearDown(self):
        del os.environ["MYSQL_USERNAME"]
        del os.environ["MYSQL_PASSWORD"]
        del os.environ["MYSQL_HOST"]
        del os.environ["MYSQL_DATABASE"]


if __name__ == '__main__':
    unittest.main()
