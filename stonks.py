import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
import nest_asyncio


nest_asyncio.apply()

#URL
SP500_URL = "https://markets.businessinsider.com/index/components/s&p_500"
CBR_URL = "http://www.cbr.ru/development/sxml/"

#для получения курса доллара
async def get_exchange_rate():
    async with aiohttp.ClientSession() as session:
        async with session.get(CBR_URL) as response:
            xml_data = await response.text()
  
            return 75.0 

#для парсинга
async def parse_sp500(session, exchange_rate):
    async with session.get(SP500_URL) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        companies = []
        rows = soup.find_all('tr')[1:]  

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue

            name = cols[1].text.strip()
            code = cols[0].text.strip()

            #обработка цены
            try:
                price_usd = float(cols[2].text.strip().replace(',', ''))
            except ValueError:
                price_usd = 0.0 

            #обработка P/E
            try:
                pe_ratio = float(cols[3].text.strip())
            except ValueError:
                pe_ratio = 0.0 

            #обработка роста
            try:
                growth = float(cols[4].text.strip().replace('%', ''))
            except ValueError:
                growth = 0.0 

            # цена в рубли
            price_rub = price_usd * exchange_rate

          
            week_low = 100.0  
            week_high = 200.0 

            #вычисление потенциальной прибыли
            if week_low > 0:  
                potential_profit = ((week_high - week_low) / week_low) * 100
            else:
                potential_profit = 0.0  

            companies.append({
                "code": code,
                "name": name,
                "price": price_rub,
                "P/E": pe_ratio,
                "growth": growth,
                "potential profit": potential_profit
            })

        return companies

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#асинхронная функция
async def main():
    exchange_rate = await get_exchange_rate()

    async with aiohttp.ClientSession() as session:
        companies = await parse_sp500(session, exchange_rate)

        #сортировка и сохранение
        top_10_expensive = sorted(companies, key=lambda x: x['price'], reverse=True)[:10]
        top_10_pe = sorted(companies, key=lambda x: x['P/E'])[:10]
        top_10_growth = sorted(companies, key=lambda x: x['growth'], reverse=True)[:10]
        top_10_profit = sorted(companies, key=lambda x: x['potential profit'], reverse=True)[:10]

        save_to_json(top_10_expensive, 'top_10_expensive.json')  #сохраняем топ-10 по цене
        save_to_json(top_10_pe, 'top_10_pe.json')  # сохраняем топ-10 по P/E
        save_to_json(top_10_growth, 'top_10_growth.json')  # сохраняем топ-10 по росту
        save_to_json(top_10_profit, 'top_10_profit.json')  # сохраняем топ-10 по прибыли

if __name__ == '__main__':
    asyncio.run(main())