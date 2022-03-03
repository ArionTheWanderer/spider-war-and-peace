import scrapy
import w3lib.html


class WarAndPeaceSpider(scrapy.Spider):
    name = "war_and_peace"
    start_urls = [
        'https://ilibrary.ru/text/11/p.1/index.html',
    ]
    
    def __init__(self):
        with open("index.txt", "w+") as f:
            f.write("")
        self.__current_page_number = 1

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'выкачка-{self.__current_page_number}.txt'
        output= w3lib.html.remove_tags(response.body, encoding="cp1251")
        
        with open(filename, 'w') as f:
            f.write(output)
        
        with open("index.txt", "a") as f:
            f.write(str(self.__current_page_number) + " " + response.url + "\n")
        
        navs_buttons = response.css('div.bnvin a::attr(href)').getall()
        
        if (self.__current_page_number == 1):
            next_page = navs_buttons[0]
        else:
            next_page = navs_buttons[1]
        number_of_next_page = next_page.split("/")[-2]
        
        if number_of_next_page != "p.101":
            next_page = response.urljoin(next_page)
            self.__current_page_number = self.__current_page_number + 1
            yield scrapy.Request(next_page, callback=self.parse)
