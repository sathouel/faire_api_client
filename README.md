Sample usage:

import faire_api_client as fc

faire = fc.Client(access_token = "your_faire_api_token_here")
args = {'limit':50,'excluded_states':'CANCELED'}
orders = faire.orders.fetch_list(args).json()['orders']
