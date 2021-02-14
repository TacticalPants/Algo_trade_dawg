import sys, os, time
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
from arctic import Arctic

#initiate keys
ALPHA_VANTAGE_KEY=os.environ.get('ALPHA_VANTAGE_HIGHER_KEY')

# Connect to Local MONGODB
store = Arctic('localhost')

'''# Create the library - defaults to VersionStore
store.initialize_library('HISTORICAL_DATA')'''
# Access the library
library = store['HISTORICAL_DATA']

cx=CryptoCurrencies(key=ALPHA_VANTAGE_KEY, output_format='pandas')
cc=ForeignExchange(key=ALPHA_VANTAGE_KEY,output_format='pandas')
#step two
#download and update data
# this is probably better as a function
Crypto_list=['ETH','LTC','BTC']

for i in Crypto_list:
    print(i)
    data, meta_data = cx.get_digital_currency_daily(symbol=i, market='USD')
    library.write(i,data)


