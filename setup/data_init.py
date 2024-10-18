""" Test models import """
import csv
import logging
import os
import glob

from datetime import datetime
from decimal import Decimal

from .models import (
    CostType, Distributor, DistributorRate, Supplier, SupplierContract,
    SupplierRate, Market, MarketRate
)

logger = logging.getLogger(__name__)

def data_init(): # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    """ data_init """

    cost_types = []
    distributors = []
    distributor_rates = []
    suppliers = []
    supplier_contracts = []
    supplier_rates = []
    markets = []
    market_rates = []

    # CostType
    with open('data/cost_type.csv', mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
        mappings = csv.DictReader(csv_file)
        for row in mappings:
            if row['slug'] != '':

                # Create CostType
                cost_type = CostType(
                    slug = row['slug'],
                    name = row['name_en'],
                    color = row['color']
                )
                cost_types.append(cost_type)

    # Market
    with open('data/be/markets.csv', mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
        mappings = csv.DictReader(csv_file)
        for row in mappings:
            #logger.debug(f'{index} - row:{row}')

            if row['slug'] != '':

                # Create Market
                market = Market(
                    slug = row['slug'],
                    market_type = row['market_type'],
                    country = row['country']
                )
                markets.append(market)

    # MarketRate
    with open('data/test/market_rate.csv', mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
        mappings = csv.DictReader(csv_file)
        for row in mappings:
            #logger.debug(f'{index} - row:{row}')

            if row['market'] != '':

                # Create Market
                market = None
                for market in markets:
                    if market.slug == row['market']:
                        break
                market = MarketRate(
                    market = market,
                    datetime_start = row['datetime_start'],
                    datetime_end = row['datetime_end'],
                    amount_eur = row['amount_eur']
                )
                market_rates.append(market)

    # Distributor
    with open('data/be/distributor/distributor.csv', mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
        mappings = csv.DictReader(csv_file)

        for row in mappings:
            if row['slug'] != '':

                file_types = []
                if row['file_types'] != '':
                    file_types = row['file_types'].split(',')

                # Create Distributor
                distributor = Distributor(
                    slug = row['slug'],
                    name = row['name'],
                    country = row['country'],
                    file_types = file_types
                )

                distributors.append(distributor)

    # Distributor rates
    path = 'data/be/distributor/rate/'
    for filename in glob.glob(os.path.join(path, '*.csv')):
        #logger.debug(f'filename:{filename}')
        with open(os.path.join(os.getcwd(), filename), mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
            mappings = csv.DictReader(csv_file)

            for row in mappings:
                #logger.debug(f'{index} - row:{row}')

                if row['distributor'] != '':
                    date_format = '%Y-%m-%d'

                    date_start = row['date_start'].lstrip().rstrip()
                    if date_start == '':
                        date_start = None
                    else:
                        date_start = datetime.strptime(date_start, date_format)

                    date_end = row['date_end'].lstrip().rstrip()
                    if date_end == '':
                        date_end = None
                    else:
                        date_end = datetime.strptime(date_end, date_format)

                    time_of_day_start = row['time_of_day_start'].lstrip().rstrip()
                    if time_of_day_start == '':
                        time_of_day_start = None
                    time_of_day_end = row['time_of_day_end'].lstrip().rstrip()
                    if time_of_day_end == '':
                        time_of_day_end = None
                    counter_type = row['counter_type']
                    if counter_type == '':
                        counter_type = None

                    for distributor in distributors:
                        if distributor.slug == row['distributor']:
                            break

                    for cost_type in cost_types:
                        if cost_type.slug == row['cost_type']:
                            break

                    # Create DistributorRate
                    distributor_rate = DistributorRate(
                        distributor = distributor,
                        cost_type = cost_type,
                        counter_type = counter_type,
                        peak_enabled = row['peak_enabled'],
                        day_time_type = row['day_time_type'],
                        rate_occurrence = row['rate_occurrence'],
                        amount_eur = row['amount_eur'],
                        tax_pct = row['tax_pct'],
                        time_of_day_start = time_of_day_start,
                        time_of_day_end = time_of_day_end,
                        date_start = date_start,
                        date_end = date_end,
                    )

                    distributor_rates.append(distributor_rate)

    # Supplier
    with open('data/be/supplier/supplier.csv', mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
        mappings = csv.DictReader(csv_file)
        for row in mappings:
            #logger.debug(f'{index} - row:{row}')

            if row['slug'] != '':

                # Create Supplier
                supplier = Supplier(
                    slug = row['slug'],
                    name = row['name'],
                    country = row['country']
                )
                suppliers.append(supplier)

    # SupplierContract
    path = 'data/be/supplier/contract/'
    for filename in glob.glob(os.path.join(path, '*.csv')):
        with open(os.path.join(os.getcwd(), filename), mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
            mappings = csv.DictReader(csv_file)
            for row in mappings:
                #logger.debug(f'{index} - row:{row}')

                if row['slug'] != '':

                    supplier = None
                    for supplier in suppliers:
                        if supplier.slug == row['supplier']:
                            break

                    # Create SupplierContract
                    supplier_contract = SupplierContract(
                        slug = row['slug'],
                        name_en = row['name_en'],
                        supplier = supplier,
                        contract_type = row['contract_type'],
                        valid_from = row['valid_from'],
                        valid_to = row['valid_to'],
                    )
                    supplier_contracts.append(supplier_contract)

    # SupplierRate
    path = 'data/be/supplier/rate/'
    for filename in glob.glob(os.path.join(path, '*.csv')):
        #logger.debug(f'filename:{filename}')
        with open(os.path.join(os.getcwd(), filename), mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
            mappings = csv.DictReader(csv_file)

            for row in mappings:
                #logger.debug(f'{index} - row:{row}')

                if row['supplier_contract'] != '':

                    date_start = row['date_start'].lstrip().rstrip()
                    if date_start == '':
                        date_start = None
                    date_end = row['date_end'].lstrip().rstrip()
                    if date_end == '':
                        date_end = None

                    day_time_type = row['day_time_type']
                    if day_time_type == '':
                        day_time_type = None

                    market = None
                    if row['dyn_market_source']:
                        for market in markets:
                            if market.slug == row['dyn_market_source']:
                                break

                    amount_eur = None
                    if row['amount_eur']:
                        amount_eur = Decimal(row['amount_eur'])

                    dyn_market_mult = None
                    if row['dyn_market_mult']:
                        dyn_market_mult = Decimal(row['dyn_market_mult'])

                    dyn_balance_eur_kwh = None
                    if row['dyn_balance_eur_kwh']:
                        dyn_balance_eur_kwh = Decimal(row['dyn_balance_eur_kwh'])

                    supplier_contract = None
                    for supplier_contract in supplier_contracts:
                        if supplier_contract.slug == row['supplier_contract']:
                            break

                    for cost_type in cost_types:
                        if cost_type.slug == row['cost_type']:
                            break

                    # Create or update SupplierRate
                    supplier_rate = SupplierRate(
                        supplier_contract = supplier_contract,
                        rate_occurrence = row['rate_occurrence'],
                        direction = row['direction'],
                        cost_type = cost_type,
                        day_time_type = day_time_type,
                        amount_eur = amount_eur,
                        tax_pct = row['tax_pct'],
                        dyn_market_source = market,
                        dyn_market_mult = dyn_market_mult,
                        dyn_balance_eur_kwh = dyn_balance_eur_kwh,
                        date_start = date_start,
                        date_end = date_end
                    )
                    supplier_rates.append(supplier_rate)

    return {
        'cost_types': cost_types,
        'distributors': distributors,
        'distributor_rates': distributor_rates,
        'suppliers': suppliers,
        'supplier_contracts': supplier_contracts,
        'supplier_rates': supplier_rates,
        'markets': markets,
        'market_rates': market_rates
    }
