import logging

logging.basicConfig(level=logging.INFO, format="")
LOG = logging.getLogger(__name__)


def display_iterable(iterable):
    return "\n".join(map(str, iterable))
