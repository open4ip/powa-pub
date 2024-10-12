""" Test cost_distributor """
import json
import logging

from compute.cost_supplier import cost_supplier
from setup.data_init import data_init

logger = logging.getLogger(__name__)

class TestCostSupplier():
    """ TestCostSupplier """

    def test_cost_supplier(self):
        """ Test cost_distributor """

        # Init data
        cost_types, distributors, distributor_rates = data_init()

        # Get subset of rates
        rates = [x for x in distributor_rates 
                 if (x.distributor.slug == 'tecteo_resa'
                     and x.date_start >= '2024-01-01'
                     and x.date_end <= '2024-12-31')]

        #logger.debug(f'rates:{rates}')

        cost_items, amount_eur_total, amount_eur_tincl_total = cost_distributor(
            consumed_kwh=1000,
            consumed_day_kwh=1000,
            consumed_night_kwh=1000,
            injected_kwh=100,
            injected_day_kwh=100,
            injected_night_kwh=100,
            peak_kw=10,
            occurence='daily',
            distributor_rates=rates,
            days_in_year=365,
            days_in_month=30
        )

        logger.debug(f'cost_items:{json.dumps(cost_items, indent=4)}')
        logger.debug(f'amount_eur_total:{amount_eur_total}')
        logger.debug(f'amount_eur_tincl_total:{amount_eur_tincl_total}')
        