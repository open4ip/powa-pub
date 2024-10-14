""" Test setup """
import logging

from setup.data_init import data_init

logger = logging.getLogger(__name__)


class TestSetup(): # pylint: disable=too-few-public-methods
    """ Test setup """

    def test_data_init(self):
        """ Test data_init """

        (cost_types,
         distributors,
         distributor_rates,
         suppliers,
         supplier_contracts,
         supplier_rates,
         markets,
         market_rates) = data_init()

        # logger.debug(f'cost_types:{len(cost_types)}')
        # logger.debug(f'distributors:{len(distributors)}')
        # logger.debug(f'distributor_rates:{len(distributor_rates)}')
        # logger.debug(f'suppliers:{len(suppliers)}')
        # logger.debug(f'supplier_contracts:{len(supplier_contracts)}')
        # logger.debug(f'supplier_rates:{len(supplier_rates)}')
        # logger.debug(f'markets:{len(markets)}')
        # logger.debug(f'market_rates:{len(market_rates)}')

        assert len(cost_types) > 0
        assert len(distributors) > 0
        assert len(distributor_rates) > 0
        assert len(suppliers) > 0
        assert len(supplier_contracts) > 0
        assert len(supplier_rates) > 0
        assert len(markets) > 0
        assert len(market_rates) > 0
