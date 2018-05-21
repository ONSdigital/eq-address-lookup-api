from flask import request, redirect, url_for
from flask_api import FlaskAPI
from . request_address import query_address_index

app = FlaskAPI(__name__)

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('address_search'))

@app.route('/address_api/', methods=['GET'])
def address_search():
    query = request.args.get('q')
    if query:
        addresses = query_address_index(query)
        return dict(addresses=addresses, count=len(addresses))
    else:
        return "Enter address_api/?q=Address"

if __name__ == '__main__':
    app.run(debug=True)