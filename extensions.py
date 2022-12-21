import json
import requests
from config import *

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base: str, sym: str, amount: str):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount.replace (",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}')
        #resp = json.loads(r.content)
        new_price = json.loads(r.content)[keys[sym.lower()]]
        #new_price = resp['rates'][sym_key] * float(amount)
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {sym} : {new_price}"
        return message
