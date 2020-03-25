import json
import requests
import random
import time
import re
from outils import *
from bs4 import BeautifulSoup as bs

jsonfolder = 'vacancies/'

def build_url(url, text, page):
        url += '&text='+text
        url += '&page='+page
        return url

class HeadhunterParser(object):
    def __init__(self, base_url, headers):
        self.session = requests.Session()
        self.base_url = base_url
        self.headers = headers

    def hh_get_page_links(self, url, checkex):
        local_vacancies = list()
        request = self.session.get(url, headers = self.headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
            divs.extend(soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}))
            for div in divs:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
                if title:
                    title = title.text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
                if href:
                    href = href['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                if company:
                    company = company.text
                if company and href and title:
                    page_data = {'title':title, 'href':href, 'company':company}
                    #print(href, jsonfolder+href.split('?')[0].split('/')[-1])
                    #responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    #requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    #local_vacancies.append((title, href, company, responsibility, requirement))
                    if href:
                        if not checkex or not file_exists(jsonfolder+href.split('?')[0].split('/')[-1]+'.json'):
                            #print('Reading:', jsonfolder+href.split('?')[0].split('/')[-1]+'.json')
                            #time.sleep(random.uniform(0.0, 0.1))
                            vacancy_data = self.hh_get_vacancy(href)
                            if vacancy_data:
                                page_data.update(vacancy_data)
                            local_vacancies.append(page_data)
                            #break;
                        else:
                            print('Exists:', jsonfolder+href.split('?')[0].split('/')[-1]+'.json')
        else:
            print('Get page error')
        return local_vacancies

    def hh_get_vacancy(self, url):
        pagedata = ''
        skills = list()
        request = self.session.get(url, headers = self.headers)
        if request.status_code == 200 or request.status_code == 204:
            soup = bs(request.content, 'html.parser')
            divs = soup.find_all('div', attrs={'data-qa':'vacancy-description'})
            #print(divs)
            for data in divs:
                pagedata = data.text#.find('p').text
                re.sub('<[^>]+>', '', pagedata)
            skillstext = soup.find_all('div', attrs={'data-qa': 'bloko-tag bloko-tag_inline'})
            #skills = list(set([item for item in skills]))
            for item in skillstext:
                skills.append(re.sub('<[^>]+>','', item.text).lower())
        else:
            print('Error vacancy get', request.status_code)
        return {'content':pagedata, 'skills':skills}
    
    def hh_grab_data(self, querytexts, pagenumber):
        vacancies = list()
        for pagenum in range(pagenumber):
            for text in querytexts:
                vacancy_datas = self.hh_get_page_links(build_url(self.base_url, text, str(pagenum)), True)
                #print(len(vacancy_datas))
                for vacancy in vacancy_datas:
                    if text.lower() not in vacancy['skills']:
                        vacancy['skills'].append(text.lower())
                    save_json_vacancy(vacancy)
        for item in vacancies:
            print(item)

    def hh_get_vacancies(self, text, numbervac):
        vacancies = list()
        i = 0
        while (len(vacancies) < numbervac):
            vacancy_datas = self.hh_get_page_links(build_url(self.base_url, text, str(i)), False)
            i+=1
            vacancies.extend(vacancy_datas[:numbervac - len(vacancies)])
        return vacancies
            
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78'}

url_init = 'https://hh.ru/search/vacancy?area=1&search_period=50&st=searchVacancy'


querytexts = ['java', 'python', 'go', 'sql', 'javascript', 'html', 'ruby', 'php', 'matlab', 'keras', 'swift', 'android',
              '.net', 'web']
pages = 71

def main():
    p = HeadhunterParser(url_init, headers)
    p.hh_grab_data(querytexts, pages)

#vacs = HeadhunterParser(url_init, headers).hh_get_vacancies('java', 30)
#for vac in vacs:
#    print(vac, '\n')
#print(len(vacs))


