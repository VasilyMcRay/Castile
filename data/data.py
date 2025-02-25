from fake_useragent import FakeUserAgent

def get_headers() -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer null',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://castile.world',
        'priority': 'u=1, i',
        'referer': 'https://castile.world/?promote_code=DZKOXV5U61',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': FakeUserAgent().chrome,
        }
    return headers