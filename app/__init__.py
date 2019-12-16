import time

import requests
from flask import request, redirect, url_for, json, g
from flask_api import FlaskAPI
from flask_cors import CORS
from structlog import get_logger

from app.request_address import query_address_index
from app.request_address import query_address_index_by_uprn

logger = get_logger()


app = FlaskAPI(__name__)
CORS(app)


@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.after_request
def after_request(response):
    if g.get('request_start_time') and g.get('address_index_response_time'):
        lookup_api_response_time = time.time() - g.request_start_time
        logger.info('Request Complete',
                    lookup_api_response_time=lookup_api_response_time,
                    lookup_api_processing_time=lookup_api_response_time - g.address_index_response_time)
    return response


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('address_search'))


@app.route('/status')
def status():
    data = {
        'status': 'OK'
    }
    return json.dumps(data)


@app.route('/address_api/', methods=['GET', 'POST'])
def address_search():

    if request.method == 'POST':
        query = request.form['q']
    else:
        query = request.args.get('q')

    if query:
        try:
            resp = query_address_index(query)
            return dict(addresses=resp['addresses'], count=len(resp['addresses']), time=resp['time'])
        except requests.exceptions.ConnectionError:
            return 'ADDRESS INDEX API CONNECTION ERROR', 503
        except requests.exceptions.ConnectTimeout:
            return 'ADDRESS INDEX API CONNECTION TIMED OUT', 503
        except requests.exceptions.ReadTimeout:
            return 'ADDRESS INDEX API READ TIMED OUT', 408
        except Exception as exception:
            return str(exception), 500
    else:
        return 'Enter address_api/?q=Address'

@app.route('/uprn/', methods=['GET', 'POST'])
def address_search_by_uprn():

    if request.method == 'POST':
        query = request.form['q']
    else:
        query = request.args.get('q')

    if query:
        try:
            resp = query_address_index_by_uprn(query)
            return dict(address=resp['address'], count=len(resp['address']), time=resp['time'])
        except requests.exceptions.ConnectionError:
            return 'ADDRESS INDEX API CONNECTION ERROR', 503
        except requests.exceptions.ConnectTimeout:
            return 'ADDRESS INDEX API CONNECTION TIMED OUT', 503
        except requests.exceptions.ReadTimeout:
            return 'ADDRESS INDEX API READ TIMED OUT', 408
        except Exception as exception:
            return str(exception), 500
    else:
        return 'Enter uprn/?q=uprn'


if __name__ == '__main__':
    app.run()
