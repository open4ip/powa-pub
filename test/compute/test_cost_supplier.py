""" Test cost_distributor """
import csv
import glob
import logging
import os

from decimal import Decimal

from setup.data_init import data_init
from compute.cost_supplier import cost_supplier

logger = logging.getLogger(__name__)

class TestCostSupplier(): # pylint: disable=too-few-public-methods
    """ TestCostSupplier """

    def test_cost_supplier(self):
        """ Test cost_distributor """

        # Init data
        data = data_init()

        #logger.debug(f'rates:{rates}')
        assert len(data['supplier_rates']) > 0

        # Get test data

        path = 'data/test/be/supplier/rate/'
        for filename in glob.glob(os.path.join(path, '*_test.csv')):
            logger.debug(f'filename:{filename}')
            with open(os.path.join(os.getcwd(), filename), mode='r') as csv_file: #pylint: disable=[unspecified-encoding]
                mappings = csv.DictReader(csv_file)
                for row in mappings:
                    #logger.debug(f'row:{row}')

                    # Fetch meter data
                    if row['description'] == 'meter_data':

                        consumed_kwh = float(row['consumed_kwh'])
                        consumed_day_kwh = float(row['consumed_day_kwh'])
                        consumed_night_kwh = float(row['consumed_night_kwh'])
                        injected_kwh = float(row['injected_kwh'])
                        injected_day_kwh = float(row['injected_day_kwh'])
                        injected_night_kwh = float(row['injected_night_kwh'])
                        peak_kw = 0
                        if row['peak_kw'] != '':
                            peak_kw = float(row['peak_kw'])

                    elif row['description'] == 'days_in_month':
                        days_in_month = int(row['unit'])

                    elif row['description'] == 'days_in_year':
                        days_in_year = int(row['unit'])

                    elif row['occurence'] != '':
                        supplier_contract_slug = row['description']
                        expected_amount_eur = float(row['amount_eur'])

                        supplier_rates = [x for x in data['supplier_rates']
                                          if x.supplier_contract.slug == supplier_contract_slug]

                        # Compute cost
                        cost_items, amount_eur_total, amount_eur_tincl_total = cost_supplier( # pylint: disable=unused-variable
                            consumed_kwh,
                            consumed_day_kwh,
                            consumed_night_kwh,
                            injected_kwh,
                            injected_day_kwh,
                            injected_night_kwh,
                            peak_kw,
                            row['occurence'],
                            supplier_rates,
                            days_in_year,
                            days_in_month
                        )

                        # logger.debug(f'expected_amount_eur:{expected_amount_eur}')
                        # logger.debug(f'amount_eur_total:{amount_eur_total}')
                        assert round(expected_amount_eur, 1) == round(amount_eur_total, 1)
