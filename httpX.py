import asyncio
import platform
import sys
from datetime import datetime, timedelta

import httpx


class HttpError(Exception):
    pass


async def request(url: str):
    async with httpx.AsyncClient() as client:
        data = await client.get(url)
        if data.status_code == 200:
            result = data.json()
            return result
        else:
            raise HttpError(f"Error status: {data.status_code} for {url}")


async def main(index_day):
    d = datetime.now() - timedelta(days=int(index_day))
    shift = d.strftime("%d.%m.%Y")
    try:
        response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
        return response
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(sys.argv)
    data = asyncio.run(main(sys.argv[1]))
    for item in data['exchangeRate']:
        if item.get("currency") in sys.argv[2]:
            print(item)



