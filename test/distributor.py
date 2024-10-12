""" DistributorRate object"""
import datetime

from dataclasses import dataclass
from typing import List

@dataclass
class Distributor:

    slug = str
    name = str
    country = str
    file_types = List[str]

@dataclass
class DistributorRate:

    distributor = Distributor
    rate_occurrence = str
    cost_type = str
    counter_type = str
    day_time_type = str
    amount_eur = float
    tax_pct = float
    time_of_day_start = datetime.datetime
    time_of_day_end = datetime.datetime
    date_start = datetime.date
    date_end = datetime.date
    date_created = datetime.date
