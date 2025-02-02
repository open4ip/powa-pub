""" Distributor cost utils """
import logging

logger = logging.getLogger(__name__)


def cost_distributor( # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements, too-many-positional-arguments
        consumed_kwh, consumed_day_kwh, consumed_night_kwh,
        injected_kwh, injected_day_kwh, injected_night_kwh, # pylint: disable=unused-argument
        peak_kw,
        peak_monthly_avrg_kw,
        prosumer_kw,
        occurence,
        distributor_rates,
        meter_type,
        peak_enabled,
        days_in_year,
        days_in_month
    ):
    """
    Based on metered data, compute the cost of from the electricity distributor.

    Args:
    - consumed_kwh. Integer. Optional. Consumed kWh.
    - consumed_day_kwh. Integer. Optional. Consumed day kWh (off peak hours)
    - consumed_night_kwh. Integer. Optional. Consumed night kWh (peak hours)
    - injected_kwh. Integer. Optional. Injected kWh.
    - injected_day_kwh. Integer. Optional. Injected day kWh (off peak hours)
    - injected_night_kwh. Integer. Optional. Injected night kWh (peak hours)
    - peak_kw. Integer. Optional. Peak power in kW during the period.
    - peak_monthly_avrg_kw. Integer. Optional. Peak power in kW during the month.
    - prosumer_kw. Integer. Optional. Prosumer installk power in kW.
    - occurence. Type of time frame. Enum of
        - daily
        - monthly
        - hourly
    - distributor_rates. List of distributor rates object to be considered.
    - meter_type. String. Type of meter. Enum of
        - simple
        - smart
    - peak_enabled. Boolean. True if peak power is enabled.
    - days_in_year. Integer. Number of days in the year.
    - days_in_month. Integer. Number of days in the month.

    Returns:
    - cost_items. dict. Cost items.
        example:
        [
            {
                'source': 'distributor',
                'type': 'injection',
                'rate_occurrence': 'daily',
                'amount_eur': 0.345,
                'amount_eur_tincl': 0.42
            },
            {
                'source': 'distributor',
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

    for rate in distributor_rates:

        #logger.debug(f'rate:{rate}')

        # Init cost item
        cost_item = {
            'source': 'distributor',
            'type': rate.cost_type.slug,
            'rate_occurrence': rate.rate_occurrence,
            'amount_eur': 0,
            'amount_eur_tincl': 0
        }

        rate.amount_eur = float(rate.amount_eur)
        rate.tax_pct = float(rate.tax_pct)

        if rate.rate_occurrence == 'per_kwh':

            # For simple and smart meter rates only
            if meter_type == rate.counter_type:
                if (meter_type == 'simple'
                    or (meter_type == 'smart' and peak_enabled == rate.peak_enabled)):
                    if rate.cost_type.slug == 'distribution_simple':
                        cost_item['amount_eur'] = rate.amount_eur * consumed_kwh

                    elif rate.cost_type.slug == 'distribution_day':
                        cost_item['amount_eur'] = rate.amount_eur * consumed_day_kwh

                    elif rate.cost_type.slug == 'distribution_night':
                        cost_item['amount_eur'] = rate.amount_eur * consumed_night_kwh

            # Non dependent on meter type - Injection
            elif rate.cost_type.slug == 'injection':
                # Total kwh injected
                total_kwh_injected = (injected_kwh
                                      + injected_day_kwh
                                      + injected_night_kwh)
                cost_item['amount_eur'] = rate.amount_eur * total_kwh_injected

            # Non dependent on meter type - Other
            elif rate.cost_type.slug not in ['distribution_simple',
                                             'distribution_day',
                                             'distribution_night',
                                             'distribution_night_excl']:
                # Total kwh consummed
                total_kwh_consumed = (consumed_kwh
                                      + consumed_day_kwh
                                      + consumed_night_kwh)

                # Use all consumed kWh
                cost_item['amount_eur'] = rate.amount_eur * total_kwh_consumed

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

        elif rate.rate_occurrence == 'annual_per_kw':
            if rate.cost_type.slug == 'prosumer':
                cost_item['amount_eur'] = rate.amount_eur * prosumer_kw

            elif (meter_type == 'smart'
                  and peak_enabled == rate.peak_enabled
                  and peak_enabled):

                if rate.cost_type.slug == 'peak_monthly_avrg':
                    cost_item['amount_eur'] = rate.amount_eur * peak_monthly_avrg_kw

                elif rate.cost_type.slug == 'peak':
                    cost_item['amount_eur'] = rate.amount_eur * peak_kw

            if occurence == 'monthly':
                cost_item['amount_eur'] = cost_item['amount_eur'] / 12
            elif occurence == 'daily':
                cost_item['amount_eur'] = cost_item['amount_eur'] / days_in_year
            elif occurence == 'hourly':
                cost_item['amount_eur'] = cost_item['amount_eur'] / (days_in_year * 24)

            # elif rate.cost_type.slug == 'capacity':
            #     if rate.counter_type == 'smart':
            #         pass
            #     elif rate.counter_type == 'classic':
            #         pass
            #     else:
            #         pass

        logger.debug(f'cost_item amount_eur: {cost_item["amount_eur"]} type: {cost_item["type"]}')

        cost_item['amount_eur_tincl'] = cost_item['amount_eur'] * (1 + rate.tax_pct / 100)

        # Round to 3 decimals
        cost_item['amount_eur'] = round(cost_item['amount_eur'], 3)
        cost_item['amount_eur_tincl'] = round(cost_item['amount_eur_tincl'], 3)

        # Add cost item to items list
        cost_items.append(cost_item)

        # Compute totals
        amount_eur_total += cost_item['amount_eur']
        amount_eur_tincl_total += cost_item['amount_eur_tincl']

    amount_eur_total = round(amount_eur_total, 3)
    amount_eur_tincl_total = round(amount_eur_tincl_total, 3)

    return cost_items, amount_eur_total, amount_eur_tincl_total
