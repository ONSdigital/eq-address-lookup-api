def sort_address_results(addresses, postcode):
    '''
    # Not to be used. Address Index API should sort for us.
    If required address object should include the following fields:

    paoStartNumber = address['nag']['pao']['paoStartNumber']
    saoStartNumber = address['nag']['sao']['saoStartNumber']
    street_number = paoStartNumber or saoStartNumber or 999999

    addresses.append({
        'number': int(street_number),
        'address': address['formattedAddress'],
        'confidenceScore': address['confidenceScore'],
        'underlyingScore': address['underlyingScore']
    })


    '''
    number_of_results = len(addresses)
    if postcode or number_of_results < 40:
        sorted_addresses = sorted(addresses, key=lambda k: k['number'])
    else:
        sorted_addresses = sorted(addresses, key=lambda k: k['confidenceScore'])

    return sorted_addresses