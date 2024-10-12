""" Supplier cost utils """
import logging

logger = logging.getLogger(__name__)

def cost_supplier( # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements, too-many-positional-arguments
        consumed_kwh, consumed_day_kwh, consumed_night_kwh,
        injected_kwh, injected_day_kwh, injected_night_kwh,
        peak_kw, # pylint: disable=unused-argument
        occurence,
        supplier_rates,
        days_in_year,
        days_in_month
    ):
    """
    Based on metered data, compute the cost of from the electricity suplier.

    Args:
    - consumed_kwh. Integer. Optional. Consumed kWh.
    - consumed_day_kwh. Integer. Optional. Consumed day kWh (off peak hours)
    - consumed_night_kwh. Integer. Optional. Consumed night kWh (peak hours)
    - injected_kwh. Integer. Optional. Injected kWh.
    - injected_day_kwh. Integer. Optional. Injected day kWh (off peak hours)
    - injected_night_kwh. Integer. Optional. Injected night kWh (peak hours)
    - peak_kw. Integer. Optional. Peak power in kW during the period.
    - occurence. Type of time frame. Enum of
        - daily
        - monthly
        - hourly
    - supplier_rates. List of distributor rates object to be considered.
    - days_in_year. Integer. Number of days in the year.
    - days_in_month. Integer. Number of days in the month.

    Returns:
    - cost_items. dict. Cost items.
        example:
        [
            {
                'source': 'supplier',
                'type': 'injection',
                'rate_occurrence': 'daily',
                'amount_eur': 0.345,
                'amount_eur_tincl': 0.42
            },
            {
                'source': 'supplier',
                'type': 'energy_contribution',
                'rate_occurrence': 'daily',
                'amount_eur': 1.05,
                'amount_eur_tincl': 1.15
            }
        ]
    - amount_eur_total. Float. Total amount in EUR.
    - amount_eur_tincl_total. Float. Total amount in EUR tax included.
    """

    # Init response
    cost_items = []
    amount_eur_total = 0
    amount_eur_tincl_total = 0

    for rate in supplier_rates:
        # Create new cost item
        cost_item = {
            'source': 'supplier',
            'type': f'{rate.rate_occurrence}_{rate.direction}_{rate.day_time_type}',
            'rate_occurrence': rate.rate_occurrence,
            'amount_eur': 0,
            'amount_eur_tincl': 0
        }

        if not rate.amount_eur:
            rate.amount_eur = 0
        rate.amount_eur = float(rate.amount_eur)
        rate.tax_pct = float(rate.tax_pct)

        if rate.rate_occurrence == 'per_kwh':
            if rate.day_time_type == 'simple':
                cost_item['amount_eur'] = rate.amount_eur * consumed_kwh
                #logger.debug(f'consumed_kwh: {consumed_kwh}')
            elif rate.day_time_type == 'day':
                cost_item['amount_eur'] = rate.amount_eur * consumed_day_kwh
                #logger.debug(f'consumed_day_kwh: {consumed_day_kwh}')
            elif rate.day_time_type in ['night']:
                cost_item['amount_eur'] = rate.amount_eur * consumed_night_kwh
                #logger.debug(f'consumed_night_kwh: {consumed_night_kwh}')
            elif rate.day_time_type == 'inject':
                cost_item['amount_eur'] = (
                    rate.amount_eur * (injected_kwh + injected_day_kwh + injected_night_kwh)
                )
            #logger.debug(f'rate.amount_eur: {rate.amount_eur}')
            #logger.debug(f'cost_item amount_eur: {cost_item["amount_eur"]}')


        elif rate.rate_occurrence == 'annual':
            if occurence == 'daily':
                cost_item['amount_eur'] = rate.amount_eur / days_in_year
            elif occurence == 'monthly':
                cost_item['amount_eur'] = rate.amount_eur / 12
            elif occurence == 'hourly':
                cost_item['amount_eur'] = rate.amount_eur / (days_in_year * 24)

        elif rate.rate_occurrence == 'monthly':
            if occurence == 'daily':
                cost_item['amount_eur'] = rate.amount_eur / days_in_month
            elif occurence == 'monthly':
                cost_item['amount_eur'] = rate.amount_eur
            elif occurence == 'hourly':
                cost_item['amount_eur'] = rate.amount_eur / (days_in_month * 24)

        cost_item['amount_eur_tincl'] = cost_item['amount_eur'] * (1 + rate.tax_pct / 100)

        # Round to 3 decimals
        cost_item['amount_eur'] = round(cost_item['amount_eur'], 3)
        cost_item['amount_eur_tincl'] = round(cost_item['amount_eur_tincl'], 3)

        # Add cost item to items list
        cost_items.append(cost_item)

        # Compute totals
        amount_eur_total += cost_item['amount_eur']
        amount_eur_tincl_total += cost_item['amount_eur_tincl']

    return cost_items, amount_eur_total, amount_eur_tincl_total


def cost_supplier_dynamic( # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements, too-many-positional-arguments
        consumed_kwh_total,
        injected_kwh_total,
        supplier_rates,
        market_rates,
        time_start,
        time_end,
        days_in_year,
        days_in_month
    ):
    """
    Args:
    - consumed_kwh_total. Integer. Optional. Consumed kWh.
    - injected_kwh_total. Integer. Optional. Injected kWh.
    - supplier_rates. List of supplier rate object to be considered.
    - market_rates. List of market rate objects to be considered.
    - time_start. Datetime. Start of the period.
    - time_end. Datetime. End of the period.
    - days_in_year. Integer. Number of days in the year.
    - days_in_month. Integer. Number of days in the month.

    Returns:
        response
    """

    cost_items = []
    amount_eur_total = 0
    amount_eur_tincl_total = 0

    for rate in supplier_rates:
        # Create new cost item
        cost_item = {
            'source': 'supplier',
            'type': f'{rate.rate_occurrence}_{rate.direction}_{rate.day_time_type}',
            'rate_occurrence': rate.rate_occurrence,
            'amount_eur': 0,
            'amount_eur_tincl': 0
        }

        if rate.amount_eur:
            rate.amount_eur = float(rate.amount_eur)
        else:
            rate.amount_eur = 0
        rate.tax_pct = float(rate.tax_pct)

        if rate.rate_occurrence == 'per_kwh':
            rate.dyn_market_mult = float(rate.dyn_market_mult)
            rate.dyn_balance_eur_kwh = float(rate.dyn_balance_eur_kwh)
            # logger.debug(f'consumed_kwh_total: {consumed_kwh_total}')
            # logger.debug(f'rate.dyn_market_mult: {rate.dyn_market_mult}')
            # logger.debug(f'rate.dyn_balance_eur_kwh: {rate.dyn_balance_eur_kwh}')

            # Fetch dynamic market rate
            # logger.debug(f'time_start:{time_start.strftime("%s")} {time_start}')
            # logger.debug(f'time_end:{time_end.strftime("%s")} {time_end}')
            # resp = MarketRate.objects.filter(
            #     market=rate.dyn_market_source,
            #     datetime_start=time_start,
            #     datetime_end=time_end
            # )
            rates = [x for x in market_rates
                           if (x.datetime_start == time_start
                               and x.datetime_end == time_end)]
            market_rate_eur = 0
            if rates:
                market_rate_eur = float(rates[0].amount_eur)
            # logger.debug(f'market_rate_eur: {market_rate_eur}')

            if rate.direction == 'consumer':
                cost_item['amount_eur'] = (
                    (market_rate_eur * rate.dyn_market_mult + rate.dyn_balance_eur_kwh)
                    * consumed_kwh_total
                )

            elif rate.direction == 'producer':
                cost_item['amount_eur'] = (
                    (market_rate_eur * rate.dyn_market_mult + rate.dyn_balance_eur_kwh)
                    * injected_kwh_total
                )

            # logger.debug(f'000 rate.amount_eur: {rate.amount_eur}')
            # logger.debug(f'000 cost_item amount_eur: {cost_item["amount_eur"]}')

        elif rate.rate_occurrence == 'annual':
            cost_item['amount_eur'] = rate.amount_eur / (days_in_year * 24)

        elif rate.rate_occurrence == 'monthly':
            #logger.debug(f'rate: {rate}')
            cost_item['amount_eur'] = rate.amount_eur / (days_in_month * 24)

        cost_item['amount_eur_tincl'] = cost_item['amount_eur'] * (1 + rate.tax_pct / 100)

        # Round to 3 decimals
        cost_item['amount_eur'] = round(cost_item['amount_eur'], 3)
        cost_item['amount_eur_tincl'] = round(cost_item['amount_eur_tincl'], 3)

        # Add cost item to items list
        cost_items.append(cost_item)

        # Compute totals
        amount_eur_total += cost_item['amount_eur']
        amount_eur_tincl_total += cost_item['amount_eur_tincl']

    # logger.debug(f'amount_eur_total: {amount_eur_total}')
    # logger.debug(f'amount_eur_tincl_total: {amount_eur_tincl_total}')

    return cost_items, amount_eur_total, amount_eur_tincl_total
