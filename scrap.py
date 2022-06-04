import requests
import scrapy

for page_number in range(1,46):
    payload = {'api_key': '6eb6717a2187640a5b334543fda39b36',
               'url': f'https://it.pracuj.pl/?tt=Python&jobBoardVersion=2&pn={page_number}', 'render': 'true'}
    r = requests.get('http://api.scraperapi.com', params=payload)
    html_file = open(f'pracujPYTHON{page_number}.html', 'w')
    html_file.write(r.text)
    html_file.close()