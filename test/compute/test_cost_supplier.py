""" Test cost_distributor """
import logging

from setup.data_init import data_init

logger = logging.getLogger(__name__)

class TestCostSupplier(): # pylint: disable=too-few-public-methods
    """ TestCostSupplier """

    def test_cost_supplier(self):
        """ Test cost_distributor """

        # Init data
        data = data_init()

        # Get subset of rates
        rates = [x for x in data['distributor_rates']
                 if (x.distributor.slug == 'tecteo_resa'
                     and x.date_start >= '2024-01-01'
                     and x.date_end <= '2024-12-31')]

        #logger.debug(f'rates:{rates}')
        assert len(rates) > 0
