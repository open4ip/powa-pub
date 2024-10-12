""" Models """
import datetime

from dataclasses import dataclass
from typing import List

@dataclass
class CostType:
    """ CostType """
    slug: str
    name: str
    color: str

@dataclass
class Distributor:
    """ Distributor """
    slug: str
    name: str
    country: str
    file_types: List[str]

@dataclass
class DistributorRate: # pylint: disable=too-many-instance-attributes
    """ DistributorRate """
    distributor: Distributor
    rate_occurrence: str
    cost_type: str
    counter_type: str
    day_time_type: str
    amount_eur: float
    tax_pct: float
    time_of_day_start: datetime.datetime
    time_of_day_end: datetime.datetime
    date_start: datetime.date
    date_end: datetime.date

@dataclass
class Supplier:
    """ Supplier """
    slug: str
    name: str
    country: str

@dataclass
class SupplierContract:
    """ SupplierContract """
    slug: str
    name_en: str
    supplier: Supplier
    contract_type: str
    valid_from: datetime.date
    valid_to: datetime.date

@dataclass
class SupplierRate: # pylint: disable=too-many-instance-attributes
    """ SupplierRate """
    supplier_contract: SupplierContract
    rate_occurrence: str
    direction: str
    day_time_type: str
    amount_eur: float
    tax_pct: float
    dyn_market_source: str
    dyn_market_mult: float
    dyn_balance_eur_kwh: float
    date_start: datetime.date
    date_end: datetime.date

@dataclass
class Market:
    """ Market """
    slug: str
    country: str
    market_type: str

@dataclass
class MarketRate:
    """ MarketRate """
    market: Market
    amount_eur: float
    datetime_start: datetime.datetime
    datetime_end: datetime.datetime
