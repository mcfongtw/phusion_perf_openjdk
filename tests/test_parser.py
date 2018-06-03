from cli import parser
from cli.env import setup_logging
import logging
setup_logging(True)

logger = logging.getLogger(__name__)

import unittest


class TestParserFunctions(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

    def test_1(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()