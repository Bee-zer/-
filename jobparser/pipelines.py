# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

#    def __init__(self):
#        client = MongoClient('localhost', 27017)
#        self.mongobase = client.vacancy1204'''

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary1(item['salary'])
            del item['salary']
            pass
        else:
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary2(item['salary'])
            del item['salary']
            pass
        return item

    def process_salary1(self, salary):
        if salary is None:
            min_salary = None
            max_salary = None
            currency = None
        elif 'з/п не указана' in salary:
            min_salary = None
            max_salary = None
            currency = None
        elif 'от ' in salary[0] and 'до ' in salary[2]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = int(salary[3].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[5]
        elif 'от ' in salary[0]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = None
            currency = salary[3]
        elif 'до ' in salary[0]:
            min_salary = None
            max_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[3]

        return min_salary, max_salary, currency



    def process_salary2(self, salary):
        global currency
        if salary is None:
            min_salary = None
            max_salary = None
            currency = None
        elif 'з/п не указана' in salary:
            min_salary = None
            max_salary = None
            currency = None
        elif 'от ' in salary[0] and 'до ' in salary[2]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = int(salary[3].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[5]
        elif 'от ' in salary[0]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = None
            currency = salary[3]
        elif 'до ' in salary[0]:
            min_salary = None
            max_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[3]


        return min_salary, max_salary, currency

