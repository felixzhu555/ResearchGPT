import urllib, urllib.request
from bs4 import BeautifulSoup
import requests

def search_arxiv(query, max_results):
    url = 'http://export.arxiv.org/api/query?search_query=cat:cs.LG%20AND%20' + query + "&max_results=" + str(max_results)
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def html_to_string(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text

def download_file(download_url):
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(f'/Users/felix_3gpdyfd/ai hackathon/cs189/{download_url.split("/")[-1]}', 'wb') as f:
            f.write(response.content)

def num(i):
    if i < 10:
        return f"0{i}"
    else:
        return str(i)

for i in range(1, 26):
    download_file(f"https://people.eecs.berkeley.edu/~jrs/189/lec/{num(i)}.pdf")