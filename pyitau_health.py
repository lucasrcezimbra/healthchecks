from datetime import date
import requests
from decouple import config
from pyitau import Itau


def check(id, method, *args, **kwargs):
    method(*args, **kwargs)
    response = requests.get(f"https://betteruptime.com/api/v1/heartbeat/{id}")
    return response.status_code


def run():
    today = date.today()
    itau = Itau(
        agency=config("ITAU_AGENCY"),
        account=config("ITAU_ACCOUNT"),
        account_digit=config("ITAU_ACCOUNT_DIGIT"),
        password=config("ITAU_PASSWORD"),
        holder_name=config("ITAU_HOLDER_NAME", default=None),
    )

    check(config("PYITAU_AUTHENTICATE"), itau.authenticate)

    try:
        check(config("PYITAU_GET_STATEMENTS"), itau.get_statements)
    except Exception:
        pass

    try:
        check(
            config("PYITAU_GET_STATEMENTS_FROM_MONTH"),
            itau.get_statements_from_month,
            year=today.year,
            month=today.month,
        )
    except Exception:
        pass

    try:
        check(config("PYITAU_GET_CREDIT_CARD_INVOICE"), itau.get_credit_card_invoice)
    except Exception:
        pass


if __name__ == "__main__":
    run()
