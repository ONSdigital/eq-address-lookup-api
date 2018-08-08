import os
from decimal import Decimal


def get_env_or_fail(key):
    value = os.getenv(key)
    if value is None:
        raise Exception("Setting '{}' Missing".format(key))

    return value

LOOKUP_URL = get_env_or_fail('LOOKUP_URL')
RESULT_LIMIT = os.getenv('RESULT_LIMIT', '100')
REQUEST_CONNECTION_TIMEOUT = Decimal(os.getenv('REQUEST_CONNECTION_TIMEOUT', '2'))
REQUEST_READ_TIMEOUT = int(os.getenv('REQUEST_READ_TIMEOUT', '5'))
AUTH_KEY = get_env_or_fail('AUTH_KEY')
