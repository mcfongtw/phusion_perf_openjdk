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

    _parser = None

    _args = None

    def __init__(self):
        self._parser = argparse.ArgumentParser()

        # either system wide or process wide profiling is accepted
        system_or_process_group = self._parser.add_mutually_exclusive_group(required=True)
        system_or_process_group.add_argument("-a", "--all", help="system wide profiling")
        system_or_process_group.add_argument("-p", "--p", help="process <pid> profiling", type=int, action='store_const')

        # input jar path
        self._parser.add_argument("-i", "--input", help="input executable path", required=True)

        # measuring frequency rate
        self._parser.add_argument("-f", "--frequency", help="Profile at this frequency", required=False, type=int, default=199, const=199)

        # measuring duration
        self._parser.add_argument("-s", "--sleep", help="Profile for this duration", required=True, type=int, default=60, const=60)

        # measuring event type
        self._parser.add_argument("-e", "--event", help="Select the PMU event", required=True, default='cycles', const='cycles')

        self._parser.add_argument("-c", "--count", help="Event period to sample", required=False)

        # enable call graph
        self._parser.add_argument("-g", "--call-graph", help="Enables call-graph (stack chain/backtrace) recording", required=False)


    def parse(self, command=""):
       self._args=self._parser.parse_args(command.split())

    #TODO: builder pattern
    def build_perf_command:
        return "perf record "

    def get_args(self):
        return self._args