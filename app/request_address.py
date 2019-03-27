import re
import json
import time

import requests
from flask import g

from app import settings
from structlog import get_logger

logger = get_logger()


def query_address_index(search_value):
    """
    Postcode definition Regex taken from:
    https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/488478/
        Bulk_Data_Transfer_-_additional_validation_valid_from_12_November_2015.pdf
    """
    if re.match(r'([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})'
                r'|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])'
                r'|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})', search_value):
        # Postcode search
        request_string = "/".join((settings.LOOKUP_URL, 'addresses', 'postcode', search_value))
    else:
        request_string = "/".join(
            (settings.LOOKUP_URL, 'addresses', 'partial?input=' + search_value + '&limit=' + settings.RESULT_LIMIT))

    logger.info("Request data from address index", url=request_string)

    address_index_request_start = time.time()
    resp = requests.get(request_string,
                        timeout=(settings.REQUEST_CONNECTION_TIMEOUT,
                                 settings.REQUEST_READ_TIMEOUT),
                        auth=(settings.AUTH_KEY, ''))
    g.address_index_response_time = time.time() - address_index_request_start
    logger.bind(address_index_response_time=g.address_index_response_time)

    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception("ERROR IN ADDRESS INDEX API (try refresh). Reason: {}. Response: {}".format(resp.reason,
                                                                                                    resp.text))

    return get_addresses(resp)


def get_addresses(resp):
    addresses = []
    result = json.loads(resp.text)
    for address in result['response']['addresses']:
        addresses.append(address['formattedAddress'])
    return addresses
