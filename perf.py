#!/usr/bin/env python
#

import sys

from cli.env import setup_logging
setup_logging(True)

from cli.process import JavaProcess, PerfProcess
import logging

logger = logging.getLogger(__name__)




if __name__ == '__main__':
    assert sys.version_info >= (3, 5)


    java_process = JavaProcess('')

    java_process.run()

    perf_process = PerfProcess('')

    perf_process.run()