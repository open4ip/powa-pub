# distributor rate CSV files

**distributor**

Slug of the related distributor.

**counter_type**

Type of counter. Rate is specific to this counter type.

Enum of
- smart. Communicative meter. Typically can also measure quarter hour granularity.
- simple. Analog meter. Needs manual indexing for data gathering.
- none. Not specificied.

**day_time_type**

Time of day type. Rate is specific to a particular time of day.

Enum of
- simple. No time of day. For counters that have no day/night.
- day. Day time rate.
- night. Night time rate.
- night_excl. Night exclusive rate.
- none. Not specificied.

**rate_occurrence**

Rate occurrence. To what period of data does a rate refer to.

Enum of
- per_kwh. Rate per kWh.
- annual_per_kw. Rate per year, per kW installed.
- annual. Rate per year.
- monthly. Rate per month.

**cost_type**

Cost type. Slug of the cost_type table. Refer back to it.

**amount_eur**

Amount in EUR.

**tax_pct**

Tax percentage.

**time_of_day_start**

For day_time_type day, night, night_excl. Time start of this day_time_type.

**time_of_day_end**

For day_time_type day, night, night_excl. Time end of this day_time_type.

**date_start**

Validity start datetime of this rate.

**date_end**

Validity end datetime of this rate.