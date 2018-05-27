import os
import signal
import subprocess
from abc import ABCMeta, abstractmethod
import logging


logger = logging.getLogger(__name__)

class AbstractProcess(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def _pre_run(self):
        pass

    @abstractmethod
    def _do_run(self):
        pass

    @abstractmethod
    def _post_run(self):
        pass


    def run(self):
        self._pre_run()
        self._do_run()
        self._post_run()

    @abstractmethod
    def _pre_kill(self):
        pass

    @abstractmethod
    def _do_kill(self):
        pass

    @abstractmethod
    def _post_kill(self):
        pass

    def suicide(self):
        self._pre_kill()
        self._do_kill()
        self._post_kill()



class GenericProcess(AbstractProcess):

    _command = None
    _pid = None
    _is_background = True

    def __init__(self, cmd, background=True):
        self._command = cmd
        self._is_background = background

    def _pre_run(self):
        logger.info("[Pre-Run][Generic]")

    def _do_run(self):
        logger.info("[Do-Run][Generic]")

        if self._is_background:
            process = subprocess.Popen(self._command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            self.pid = process.pid
        else:
            #Foreground
            process = subprocess.Popen(self._command, stdout=subprocess.PIPE, preexec_fn=os.setsid)
            self.pid = process.pid

    def _post_run(self):
        logger.info("[Post-Run][Generic]")

    def _pre_kill(self):
        logger.info("[Pre-Kill][Generic]")

    def _do_kill(self):
        logger.info("[Do-Kill][Generic]")

        if self._is_background:
            os.killpg(os.getpgid(self._pid), signal.SIGTERM)
        else:
            raise Exception("Process " + self._pid + " did not run in background!")

    def _post_kill(self):
        logger.info("[Post-Kill][Generic]")


class JavaProcess(GenericProcess):
    def _pre_run(self):
        logger.info("[Pre-Run][Java]")

    def _do_run(self):
        logger.info("[Do-Run][Java]")

    def _post_run(self):
        logger.info("[Post-Run][Java]")

    def _pre_kill(self):
        logger.info("[Pre-Kill][Java]")

    def _do_kill(self):
        logger.info("[Do-Kill][Java]")

    def _post_kill(self):
        logger.info("[Post-Kill][Java]")


class PerfProcess(GenericProcess):

    def _pre_run(self):
        logger.info("[Pre-Run][Perf]")

    def _do_run(self):
        logger.info("[Do-Run][Perf]")

    def _post_run(self):
        logger.info("[Post-Run][Perf]")

    def _pre_kill(self):
        logger.info("[Pre-Kill][Perf]")

    def _do_kill(self):
        logger.info("[Do-Kill][Perf]")

    def _post_kill(self):
        logger.info("[Post-Kill][Perf]")