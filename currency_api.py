# currency_api.py
import requests
from datetime import datetime, timezone


class CurrencyAPI:
    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.last_update = None
        self.currency_data = None

    def get_currency_rates(self):
        """Получение и кеширование данных о валютах"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()

            self.currency_data = data['Valute']
            self.last_update = datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%S%z')
            return True
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return False

    def get_currency_info(self, currency_code):
        """Получение данных по конкретной валюте"""
        if not self.currency_data:
            if not self.get_currency_rates():
                return None

        currency = self.currency_data.get(currency_code)
        if not currency:
            return None

        return {
            'name': currency['Name'],
            'current': round(currency['Value'], 2),  # Округление до 2 знаков
            'previous': round(currency['Previous'], 2),  # Округление предыдущего значения
            'change_abs': round(currency['Value'] - currency['Previous'], 2),
            'change_pct': round(
                (currency['Value'] - currency['Previous']) / currency['Previous'] * 100,
                2
            )
        }


class ExchangeRateAPI :
    def __init__(self, api_key) :
        self.api_key = api_key
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/USD/RUB"
        self.usd_rate = None
        self.last_update = None

    def get_rates(self) :
        """Получаем курс USD/RUB и обновляем время"""
        try :
            response = requests.get(f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD")
            response.raise_for_status()
            data = response.json()

            if data['result'] != 'success' :
                return False

            self.usd_rate = data['conversion_rates']['RUB']
            self.last_update = datetime.strptime(data['time_last_update_utc'], '%a, %d %b %Y %H:%M:%S +0000')
            return True

        except Exception as e :
            print(f"ExchangeRate-API error: {e}")
            return False

    def convert_via_usd(self, target_currency) :
        """Конвертируем через USD курс для других валют"""
        try :
            response = requests.get(f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{target_currency}/USD")
            response.raise_for_status()
            data = response.json()

            if data['result'] != 'success' :
                return None

            rate = self.usd_rate * data['conversion_rate']
            return round(rate, 2)

        except Exception as e :
            print(f"Conversion error for {target_currency}: {e}")
            return None


# currency_api.py (добавляем новый класс)
class BinanceAPI:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
        self.p2p_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        self.last_update = None

    # Добавьте этот метод в класс
    def get_binance_data(self, symbol):
        """Получение данных по криптопаре с Binance"""
        try:
            # Получаем текущую цену
            price_url = f"{self.base_url}/ticker/price?symbol={symbol}"
            price_response = requests.get(price_url)
            price_response.raise_for_status()
            price_data = price_response.json()

            # Получаем 24h изменение
            change_url = f"{self.base_url}/ticker/24hr?symbol={symbol}"
            change_response = requests.get(change_url)
            change_response.raise_for_status()
            change_data = change_response.json()

            return {
                'price': float(price_data['price']),
                'change_abs': round(float(change_data['priceChange']), 2),
                'change_pct': round(float(change_data['priceChangePercent']), 2),
                'time': datetime.now(timezone.utc)
            }
        except Exception as e:
            print(f"Binance API error: {e}")
            return None

    def get_p2p_rate(self, asset="USDT", fiat="RUB", trade_type="BUY") :
        try :
            headers = {
                "Content-Type" : "application/json",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            data = {
                "asset" : asset,
                "fiat" : fiat,
                "tradeType" : trade_type,
                "page" : 1,
                "rows" : 1
            }

            response = requests.post(self.p2p_url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()

            if not result['data'] :
                return None

            advertiser = result['data'][0]['adv']
            return {
                'price' : float(advertiser['price']),
                'time' : datetime.fromtimestamp(result['data'][0]['adv']['updateTime'] / 1000, timezone.utc)
            }
        except Exception as e :
            print(f"Binance P2P error: {e}")
            return None