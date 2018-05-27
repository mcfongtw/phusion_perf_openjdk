import argparse
from abc import ABCMeta
from enum import Enum


class AbstractPerfParser(object):
    __metaclass__ = ABCMeta

    _root_parser=None

    def __init__(self):
        self._root_parser=argparse.ArgumentParser()


class PerfEventType(Enum):
    ON_CPU = ('cycles', 1)
    L1_CACHE_MISSES = ('L1-dcache-load-misses', 2)
    LAST_LEVEL_CACHE_MISSES = ('LLC-load-misses', 3)
    BLOCK_REQ_ISSUE = ('block:block_rq_issue', 4)

    def __init__(self, instruction, value):
        self._instruction = instruction
        self._value = value


    def get_instruction(self):
        return self._instruction

    def get_value(self):
        return self._value



class PerfProfileParser(AbstractPerfParser):

    def __init__(self, is_process = True, frequency = 99, sleep_duration=60, enable_call_graph=True):
        parser = argparse.ArgumentParser()

        # input jar path
        parser.add_argument("-i", "--input", help="input jar path", required=True)
        # measuring metric type
        parser.add_argument("-m", "--metric", help="measuring metric type", required=True)

        parser.add_argument("-t", "--type", help="process or system wide profiling", required=False)