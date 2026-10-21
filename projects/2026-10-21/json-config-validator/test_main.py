import unittest
from main import validate_config

class TestConfigValidator(unittest.TestCase):
    def test_valid_config(self):
        config = {
            'host': '127.0.0.1',
            'port': 8080,
            'debug': False,
            'allowed_hosts': ['*']
        }
        errors = validate_config(config)
        self.assertEqual(len(errors), 0)

    def test_invalid_config(self):
        config = {
            'host': '127.0.0.1',
            'port': '8080',
            'debug': 'not-a-bool'
        }
        errors = validate_config(config)
        self.assertTrue(len(errors) > 0)

if __name__ == '__main__':
    unittest.main()
