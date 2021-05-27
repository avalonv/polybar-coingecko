#!/usr/bin/env python3

import configparser
import sys
from os import path
from decimal import Decimal
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
config = configparser.ConfigParser()

# File must be opened with utf-8 explicitly
with open(f'{path.dirname(__file__)}/crypto-config', 'r', encoding='utf-8') as f:
    config.read_file(f)

# Everything except the general section
currencies = [x.lower() for x in config.sections() if x != 'general']
base_currency = config['general']['base_currency'].lower()
params = {'convert': base_currency}


for currency in currencies:
    try:
        coin_dict = cg.get_price(ids=f'{currency}', include_24hr_change='true',
            vs_currencies=f'{base_currency}')
    except:
        # Print nothign if no connection
        sys.stdout.write('')
        sys.exit()

    icon = config[currency]['icon']
    local_price = round(Decimal(coin_dict[f'{currency}'][f'{base_currency}']), 2)
    change_24 = round(Decimal(coin_dict[f'{currency}']['usd_24h_change']), 1)

    display_opt = config['general']['display']
    if display_opt == 'both' or display_opt == None:
        sys.stdout.write(f'{icon} {local_price}/{change_24:+}%  ')
    elif display_opt == 'percentage':
        sys.stdout.write(f'{icon} {change_24:+}%  ')
    elif display_opt == 'price':
        sys.stdout.write(f'{icon} {local_price}  ')
