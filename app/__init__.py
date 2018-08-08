import requests
from flask import request, redirect, url_for, json
from flask_api import FlaskAPI
from . request_address import query_address_index

app = FlaskAPI(__name__)

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('address_search'))

@app.route('/status')
def status():
    data = {
        'status': 'OK'
    }
    return json.dumps(data)

@app.route('/address_api/', methods=['GET'])
def address_search():
    query = request.args.get('q')
    if query:
        try:
            addresses = query_address_index(query)
            return dict(addresses=addresses, count=len(addresses))
        except requests.exceptions.ConnectionError:
            return 'ADDRESS INDEX API CONNECTION ERROR', 503
        except requests.exceptions.ConnectTimeout:
            return "ADDRESS INDEX API CONNECTION TIMED OUT", 503
        except requests.exceptions.ReadTimeout:
            return "ADDRESS INDEX API READ TIMED OUT", 408
    else:
        return "Enter address_api/?q=Address"

if __name__ == '__main__':
    app.run(debug=True)