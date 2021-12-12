import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    #url = f'https://www.indeed.co.uk/jobs?q=python+developer&l=London,+Greater+London&start={page}'
    url = f'https://pk.indeed.com/jobs?q=data+science&l=Pakistan&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

joblist = []
def transform(soup):
    divs = soup.find_all('div', class_ = 'slider_container')
    for item in divs:
        title = item.find('div', class_ = 'heading4').text.strip()
        #title = item.find('span').text.strip()
        company = item.find('div', class_ = 'heading6').text.strip()
        companyLocation = item.find('div', class_ = 'companyLocation').text.strip()
        try:
            date = item.find('span', class_ = 'date').text.strip()
            salary = item.find('div', class_ = 'salary-snippet').text.strip()
        except:
            date = ''
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
        #summary = item.find('div', {'class' : 'summary'}).text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'date' : date,
            'companyLocation': companyLocation,
            'salary': salary,
            'summary': summary
        }
        
        joblist.append(job)

    return    

for i in range(0,70,10):
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
df.to_csv('ds-1.csv')
