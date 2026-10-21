import unittest
from main import extract_links

class TestLinkChecker(unittest.TestCase):
    def test_extract_links(self):
        md_content = 'Here is a [Google](https://google.com) and an invalid [Local](http://localhost/test).'
        links = extract_links(md_content)
        self.assertEqual(len(links), 2)
        self.assertIn('https://google.com', links)
        self.assertIn('http://localhost/test', links)

if __name__ == '__main__':
    unittest.main()
