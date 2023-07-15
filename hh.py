import requests
import bs4
import fake_headers
from pprint import pprint
import json
headers = fake_headers.Headers().generate()
params = {'no_magic':'true',
          'L_save_area':'true',
          'text':'Python',
          'area':['1','2'],
          'experience':'doesNotMatter',
          'currency_code':'USD',
          'order_by':'relevance',
          'search_period':'0',
          "items_on_page":'50'
          }
hh_html = requests.get("https://spb.hh.ru/search/vacancy", headers=headers, params=params).content
soup = bs4.BeautifulSoup(hh_html, 'lxml')

job_name_tag_list = soup.find_all('a', class_='serp-item__title')
job_name_list = []
for name in job_name_tag_list:
    job_name_list.append(name.text)

span_com_name_tag_list = soup.find_all('a', class_='bloko-link bloko-link_kind-tertiary')
com_name_list = []
for com_name in span_com_name_tag_list:
    com_name_list.append(com_name.text)

salary_a_tag_list = soup.find_all('span', class_='bloko-header-section-3')
list_salary = []
for salary in salary_a_tag_list:
    list_salary.append(salary.text)

work_list = []
article_link_list = soup.find_all('a', class_='serp-item__title')
for article_number in range(len(article_link_list)):
    vacancy_content = requests.get((article_link_list[article_number])['href'], headers=headers).content.decode(encoding='utf_8')
    soup_for_vacancy = bs4.BeautifulSoup(vacancy_content, 'lxml')
    vac_description = soup_for_vacancy.find('div', class_='vacancy-section')
    if 'Django' and 'Flask' in str(vac_description) or 'django' and 'flask' in str(vac_description):
        work_list.append({'Job title':job_name_list[article_number],
                          'Company name':com_name_list[article_number],
                          'Average salary':list_salary[article_number],
                          'Link':article_link_list[article_number]['href']})
with open('work_list.json', 'w', encoding='utf-8') as file:
    json.dump(work_list, file, indent=4, ensure_ascii=False)