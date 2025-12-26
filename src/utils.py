import locale


def parse_currency(value):
    return float(value.replace('.', '').replace(',', '.').replace('R$', ''))


def format_currency(value):
    return locale.currency(value, grouping=True)


def format_float_number(value):
    return locale.format_string('%.2f', value)
