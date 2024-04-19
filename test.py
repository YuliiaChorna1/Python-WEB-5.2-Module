import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class CurrencyRateAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_currency_rate(self, currency, date):
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.base_url}?json&exchange&coursid=5&date={date.strftime('%d.%m.%Y')}"
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    for item in data:
                        if item['ccy'] == currency:
                            return item['sale'], item['buy']
            except aiohttp.ClientError as e:
                print(f"An error occurred: {e}")
                return None, None

class CurrencyRateConsoleUtility:
    def __init__(self, api):
        self.api = api

    async def show_rates(self, days):
        if days > 10:
            print("Ви можете перевірити курси лише за останні 10 днів.")
            return
        today = datetime.now()
        for i in range(days):
            date = today - timedelta(days=i)
            usd_sale, usd_buy = await self.api.get_currency_rate('USD', date)
            eur_sale, eur_buy = await self.api.get_currency_rate('EUR', date)
            print(f"Дата: {date.strftime('%Y-%m-%d')}")
            print(f"USD: Купівля {usd_buy}, Продаж {usd_sale}")
            print(f"EUR: Купівля {eur_buy}, Продаж {eur_sale}")

class Request:
    def __init__(self, days):
        self.days = days

class Response:
    def __init__(self, date, usd_sale, usd_buy, eur_sale, eur_buy):
        self.date = date
        self.usd_sale = usd_sale
        self.usd_buy = usd_buy
        self.eur_sale = eur_sale
        self.eur_buy = eur_buy

async def main():
    # Отримайте кількість днів з аргументів командного рядка
    days = int(sys.argv[1])
    api = CurrencyRateAPI("https://api.privatbank.ua/p24api/pubinfo")
    utility = CurrencyRateConsoleUtility(api)
    await utility.show_rates(days)

if __name__ == "__main__":
    # Перевірте, чи сценарій виконується безпосередньо, а не імпортується
    if asyncio.get_event_loop().is_running():
        # Створіть новий цикл подій, якщо вже працює один
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    # Виконайте основну функцію
    loop.run_until_complete(main())
