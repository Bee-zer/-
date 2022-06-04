import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/resume/search_resume.html?keywords%5B0%5D%5Bkeys%5D=Python&keywords%5B0%5D%5Bskwc%5D=and&keywords%5B0%5D%5Bsrws%5D=1']

    def parse(self, response: HtmlResponse):
        # response.status
        next_page = response.xpath('//a[contains(@class,"f-test-button-dalshe")]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="f-test-search-result-item"]//div/div/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("h1::text").get()
        salary = response.xpath('//span[@class = "-gENC _1TcZY mO3i1 dAWx1"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)

