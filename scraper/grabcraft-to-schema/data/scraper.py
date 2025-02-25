import requests
from bs4 import BeautifulSoup
"""
get urls from grabcraft and save to file

Edit 2/25/25: Thanks Xiuyuan!
"""
HDR = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

def read_page(url):
    r = requests.get(url=url, headers=HDR)
    soup = BeautifulSoup(r.content,  "html.parser") 
    n_table = soup.findAll('h3', attrs = {'class':'name'}) 

    urls = []
    for row in n_table:
        urls.append(row.find('a')['href'])
    return urls

pg = 1
prev_result = True
cumulative = []
while prev_result:
    urls = read_page(f"https://www.grabcraft.com/minecraft/houses/sort/date1/pg/{pg}")
    prev_result = urls
    cumulative += urls
    print(f"\rpage: {pg}, {len(urls)} urls found, {len(cumulative)} total")
    pg += 1

with open('houses.txt', 'w') as f:
    for line in cumulative:
        f.write(f"https://www.grabcraft.com{line}\n")