""" Test cost_distributor """
import csv
import glob
import logging
import os

from datetime import datetime

from compute.cost_distributor import cost_distributor
from setup.data_init import data_init

logger = logging.getLogger(__name__)

class TestCostDistributor(): # pylint: disable=too-few-public-methods
    """ TestCostDistributor """

    def test_cost_distributor(self):
        """ Test cost_distributor """

        # Init data
        data = data_init()

        # Get test data
        path = 'data/test/be/distributor/rate/'
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

                    # Fetch common test data
                    elif row['description'] == 'days_in_month':
                        days_in_month = int(row['unit'])
                    elif row['description'] == 'days_in_year':
                        days_in_year = int(row['unit'])
                    elif row['description'] == 'prosumer_kw':
                        prosumer_kw = int(row['unit'])
                    elif row['description'] == 'peak':
                        peak_kw = int(row['unit'])
                    elif row['description'] == 'peak_monthly_avrg':
                        peak_monthly_avrg_kw = int(row['unit'])

                    # Fetch particular test data
                    elif row['total_occurence'] != '':
                        distributor_slug = row['description']
                        counter_type = row['counter_type']
                        peak_enabled = row['peak_enabled']

                        date_format = '%Y-%m-%d'
                        date_start = row['date_start'].strip()
                        date_end = row['date_end'].strip()
                        logger.debug(f'date_start:{date_start}')
                        logger.debug(f'date_end:{date_end}')
                        date_start = datetime.strptime(date_start, date_format)
                        date_end = datetime.strptime(date_end, date_format)
                        expected_amount_eur = float(row['amount_eur'])

                        distributor_rates = [x for x in data['distributor_rates']
                            if (x.distributor.slug == distributor_slug
                                and x.date_start >= date_start
                                and x.date_end <= date_end)]

                        #logger.debug(f'distributor_rates:{distributor_rates}')

                        # Compute cost
                        cost_items, amount_eur_total, amount_eur_tincl_total = cost_distributor(
                            consumed_kwh,
                            consumed_day_kwh,
                            consumed_night_kwh,
                            injected_kwh,
                            injected_day_kwh,
                            injected_night_kwh,
                            peak_kw,
                            peak_monthly_avrg_kw,
                            prosumer_kw,
                            row['total_occurence'],
                            distributor_rates,
                            counter_type,
                            peak_enabled,
                            days_in_year,
                            days_in_month
                        )

                        logger.debug(f'expected_amount_eur:{expected_amount_eur}')
                        logger.debug(f'amount_eur_total:{amount_eur_total}')
                        assert round(expected_amount_eur, 1) == round(amount_eur_total, 1)
