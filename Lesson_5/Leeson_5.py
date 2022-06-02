# Вариант I
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


def write_to_database(mail):

    client = MongoClient('127.0.0.1', 27017)
    db = client['mail_db']
    mail_data = db.mail
    if mail_data.find_one({'link': mail['link']}):
        print(f'Duplicated mail {mail["link"]}')
    else:
        mail_data.insert_one(mail)
        print(f'Success insert the link {mail["link"]}')


url = 'https://e.mail.ru'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
options = Options()
options.add_argument('start-maximized')

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

driver.get('https://account.mail.ru/login')
button = driver.find_element(By.XPATH, '//div[contains(@class, "box-0-2-119")]')
button.click()

elem = driver.find_element(By.XPATH, '//input[@name="username"]')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
time.sleep(2)
elem = driver.find_element(By.XPATH, '//input[@name="password"]')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 30)
elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "llc ")]')))
links_set = set()
last_link = ''
while True:
    links = driver.find_elements(By.XPATH, '//a[contains(@class, "llc ")]')
    if last_link == links[-1].get_attribute('href'):
        break
    else:
        last_link = links[-1].get_attribute('href')
    actions = ActionChains(driver)
    for el in links:
        links_set.add(el.get_attribute('href'))
    actions.move_to_element(links[-1])
    actions.perform()
    time.sleep(4)

mail_list = []
for link in list(links_set):
    mail_data = {}
    driver.get(link)
    time.sleep(3)
    driver.implicitly_wait(35)
    title = driver.find_element(By.TAG_NAME, 'h2').text
    sender_info = driver.find_element(By.XPATH, '//div[@class="letter__author"]')
    author_name = sender_info.find_element(By.XPATH, './span[@class="letter-contact"]').text
    author_email = sender_info.find_element(By.XPATH, './span[@class="letter-contact"]').get_attribute('title')
    date = sender_info.find_element(By.XPATH, './div[@class="letter__date"]').text
    body = driver.find_element(By.XPATH, "//div[@class='letter-body']").text
    mail_data['link'] = link
    mail_data['author_name'] = author_name
    mail_data['author_email'] = author_email
    mail_data['title'] = title
    mail_data['letter_date'] = date
    mail_data['letter_body'] = body
    print(mail_data['title'])
    write_to_database(mail_data)
    mail_list.append(mail_data)

pprint(mail_list)