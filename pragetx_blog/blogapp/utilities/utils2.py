import phonenumbers
import pycountry
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from phonenumbers.phonenumberutil import region_code_for_number
from decimal import Decimal

def get_country_code(phone_number):
    pass
    if phone_number:
        pn = phonenumbers.parse(phone_number)
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
        return country.alpha_3
    return "IND"


def get_country_currency_code(phone_number):
    pass
    if not phone_number:
        return "INR"
    pn = phonenumbers.parse(phone_number)
    country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
    if country.alpha_2 == "IN":
        return "INR"
    elif country.alpha_2 in [
        "AT",
        "BE",
        "BG",
        "HR",
        "CY",
        "CZ",
        "DK",
        "EE",
        "FI",
        "FR",
        "DE",
        "GR",
        "HU",
        "IE",
        "IT",
        "LV",
        "LT",
        "LU",
        "MT",
        "NL",
        "PL",
        "PT",
        "RO",
        "SK",
        "SI",
        "ES",
        "SE",
    ]:
        return "EUR"
    elif country.alpha_2 == "GB":
        return "GBP"
    else:
        return "USD"

        
# def currency_conversion(from_currency, to_currency, amount):
#     return convert_money(Money(amount, from_currency), to_currency)


