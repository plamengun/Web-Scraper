from bs4 import BeautifulSoup
import requests


resp_url = requests.get('https://www.upwork.com/ab/feed/jobs/rss?q=python&contractor_tier=2%2C3&proposals=0-4&sort=recency&paging=0%3B10&api_params=1&securityToken=f2de7592ae0640de30c3908545fdc8d53c89e8d1aabe736eac8074a2c18280dd2cee848455935a36dafa06163c4407dfe3b8936cb2699be7023843af15b0995b&userUid=703923235574398976&orgUid=703923235633119233')

soup = BeautifulSoup(resp_url.content, 'xml')
entries = soup.find_all('item')

for entry in entries:
    title = entry.title.text
    url = entry.link.text
    print(f"Job post: {title}\nLink: {url}\n\n")




