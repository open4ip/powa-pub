# supplier contract CSV files

**supplier_contract**

Related contract slug

**rate_occurrence**

Rate occurence that the amount relates to.

Enum of
- monthly. Per month.
- annual. Per year.
- per_kwh. Per kWh.

**direction**

Energy flow direction.

Enum of
- consumer. Customer buys energy.
- producer. Customer produces energy.

**day_time_type**

Time of day type. Rate is specific to a particular time of day.

Enum of
- simple. No time of day. For counters that have no day/night.
- day. Day time rate.
- night. Night time rate.
- night_excl. Night exclusive rate.
- none. Not specificied.

**amount_eur**

Amount in EUR.

**tax_pct**

Tax percentage.