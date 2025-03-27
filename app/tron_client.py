from tronpy import Tron
from tronpy.providers import HTTPProvider

class TronClient:
    """Класс для взаимодействия с Tron сетью через TronPy."""
    def __init__(self):
        self.client = Tron(provider=HTTPProvider("https://api.trongrid.io"))

    def get_balance(self, address: str) -> float:
        try:
            balance = self.client.get_account_balance(address)
            return balance if balance else 0.0
        except Exception as e:
            raise Exception(f"Ошибка при получении баланса: {str(e)}")

    def get_resources(self, address: str) -> dict:
        try:
            resources = self.client.get_account_resource(address) 
            print(f"Resources from TronPy: {resources}") 
            return resources if resources else {}
        except Exception as e:
            raise Exception(f"Ошибка при получении ресурсов: {str(e)}")