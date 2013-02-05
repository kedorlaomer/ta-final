# encoding=utf-8

import unittest

from helpers import getHamContent, getSpamContent


class TestHelpersFunktions(unittest.TestCase):

    def setUp(self):
        pass

    def testGetHamContent(self):
        content = getHamContent()
        self.assertEqual(len(content), 1171)
        self.assertTrue(content[0])

    def testGetSpamContent(self):
        content = getSpamContent()
        self.assertEqual(len(content), 1732)
        self.assertTrue(content[234])


if __name__ == '__main__':
    unittest.main()
