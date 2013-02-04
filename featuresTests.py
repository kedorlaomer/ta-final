# encoding=utf-8

import unittest

from features import PROMILLE
from features import linkCounter, citationLineCounter


class TestFeaturesFunktions(unittest.TestCase):

    def setUp(self):
        pass

    def testLinkCounter(self):
        tokens = [
            'asdasd',
            'http://asdasdasdas',
            'http://a.com',
            'http://b.a.com',
            'http://www.site_name.com',
        ]
        self.assertEqual(
            linkCounter(tokens).values()[0],
            3 * PROMILLE / len(tokens)
        )

    def testCitationCounter(self):
        filepath = "./eval/00009.13c349859b09264fa131872ed4fb6e4e"

        with open(filepath) as f:
            text = f.readlines()
        text = ''.join(text)

        self.assertEqual(
            citationLineCounter(text).values()[0],
            24 * PROMILLE / text.count("\n")
        )


if __name__ == '__main__':
    unittest.main()
