import logging
from logging.config import dictConfig


def setup_logging(is_test = False) :

    if is_test:
        default_log_lvl = logging.DEBUG
    else:
        default_log_lvl = logging.INFO

    logging_config = dict(
        version = 1,
        formatters =
        {
            'default':
                {
                    'format' : '%(asctime)s %(name)-35s %(levelname)-8s %(message)s'
                }
        },
        handlers =
        {
            'default':
                {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'level': default_log_lvl
                }
        },
        root =
        {
            'handlers': ['default'],
            'level': default_log_lvl,
            'propagate': True
        },
    )

    dictConfig(logging_config)


JVM_EXPERIMENTAL_OPTS = " -XX:-Inline "

JVM_PERF_OPTS = " -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints"

JVM_OPTS = ""

JVM_OPTS = ''.join([JVM_OPTS, JVM_EXPERIMENTAL_OPTS])

DEFAULT_PERF_RECORD_FREQ="299"

DEFAULT_PERF_RECORD_TIME_IN_SEC="60"

PERF_MAP_AGENT_DIR="/workspace/perf-map-agent"

FLAME_GRAPH_DIR="/workspace/FlameGraph"

PERF_OUTPUT_DATA_PATH="/workspace/perf.data"