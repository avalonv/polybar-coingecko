#!/usr/bin/env python3

import configparser
import sys
from os import path
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
config = configparser.ConfigParser()

# File must be opened with utf-8 explicitly
with open(f'{path.dirname(__file__)}/crypto-config', 'r', encoding='utf-8') as f:
    config.read_file(f)

# Everything except the general section
currencies = [x.lower() for x in config.sections() if x != 'general']
base_currency = config['general']['base_currency'].lower()


for currency in currencies:
    try:
        price_data = cg.get_price(ids=currency, include_24hr_change='true',
            vs_currencies=base_currency)
    except:
        # Print nothing if no connection
        sys.stdout.write('')
        sys.exit(2)

    try:
        icon = config[currency]['icon']
    except:
        icon = cg.get_coin_by_id(currency)['symbol']

    try:
        digits = int(config[currency]['digits'])
    except:
        digits = int(config['general']['digits'])


    local_price = format(price_data[currency][base_currency], f'.{digits}f')
    change_24 = round(price_data[currency]['usd_24h_change'], 1)

    display_opt = config['general']['display']
    if display_opt == 'both':
        sys.stdout.write(f'{icon} {local_price}/{change_24:+}%  ')
    elif display_opt == 'percentage':
        sys.stdout.write(f'{icon} {change_24:+}%  ')
    else:
        sys.stdout.write(f'{icon} {local_price}  ')
