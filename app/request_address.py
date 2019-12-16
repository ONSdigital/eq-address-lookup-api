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
                r'|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})',
                search_value):
        # Postcode search
        request_string = f'{settings.LOOKUP_URL}/addresses/postcode/{search_value}'
    else:
        request_string = f'{settings.LOOKUP_URL}/addresses/partial'\
            f'?input={search_value}'\
            f'&limit={settings.RESULT_LIMIT}'

    logger.info('Request data from address index', url=request_string)

    address_index_request_start = time.time()
    headers = {'content-type': 'application/json'}
    resp = requests.get(request_string,
                        timeout=(settings.REQUEST_CONNECTION_TIMEOUT,
                                 settings.REQUEST_READ_TIMEOUT),
                        auth=(settings.AUTH_KEY, ''),
                        headers=headers)
    g.address_index_response_time = time.time() - address_index_request_start
    logger.bind(address_index_response_time=g.address_index_response_time)

    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('ERROR IN ADDRESS INDEX API (try refresh).'
                        f' Reason: {resp.reason}. Response: {resp.text}')

    return dict(addresses=build_addresses(resp), time=g.address_index_response_time)


def query_address_index_by_uprn(search_value):

    request_string = f'{settings.LOOKUP_URL}/addresses/uprn/{search_value}?verbose=true'

    logger.info('UPRN Request data from address index', url=request_string)

    address_index_request_start = time.time()
    headers = {'content-type': 'application/json'}
    resp = requests.get(request_string,
                        timeout=(settings.REQUEST_CONNECTION_TIMEOUT,
                                 settings.REQUEST_READ_TIMEOUT),
                        auth=(settings.AUTH_KEY, ''),
                        headers=headers)
    g.address_index_response_time = time.time() - address_index_request_start
    logger.bind(address_index_response_time=g.address_index_response_time)

    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('ERROR IN ADDRESS INDEX API (try refresh).'
                        f' Reason: {resp.reason}. Response: {resp.text}')

    return dict(address=build_address(resp), time=g.address_index_response_time)


def get_addresses(resp):
    addresses = []
    result = json.loads(resp.text)
    logger.info('Address Index API response data', data=result)
    for address in result['response']['addresses']:
        addresses.append(address['formattedAddress'])
    logger.info('eQ Address Lookup API response data', data=addresses)
    return addresses


def build_address(resp):
    result = json.loads(resp.text)
    logger.info('UPRN Building address from Address Index response data', data=result)
    address_response = result['response']['address']
    address_fields = address_response['formattedAddress'].split(", ")
    i = 0
    address = {}
    for value in address_fields:
        i = i + 1
        key = 'field' + str(i)
        address[key] = value
    address["uprn"] = address_response['uprn']
    address["formattedAddress"] = address_response['formattedAddress']
    address["welshFormattedAddressNag"] = address_response['welshFormattedAddressNag']
    # There will be 0 or 1 paf
    address["paf"] = address_response['paf']
    # There will be >= 1 nag
    address["nag"] = address_response['paf']
    logger.info('UPRN Formatted data from eQ API', data=address)
    return address


def build_addresses(resp):
    addresses = []
    result = json.loads(resp.text)
    logger.info('Building addresses from Address Index response data', data=result)
    for address_line in result['response']['addresses']:
        address = {}
        address["uprn"] = address_line['uprn']
        address["text"] = address_line['formattedAddress']
        addresses.append(address)
    logger.info('Formatted data from eQ API', data=addresses)
    return addresses
