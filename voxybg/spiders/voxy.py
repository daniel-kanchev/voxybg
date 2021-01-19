import scrapy
from scrapy.loader import ItemLoader
from voxybg.items import Article
from datetime import datetime


def format_content(text, title):
    # removes data which was already extracted from the article body

    if not text.strip():  # removes whitespace
        return False

    elif text == title:  # removes the title
        return False

    elif text.endswith("Comments"):  # removes the number of comments
        return False

    else:
        return True


class VoxySpider(scrapy.Spider):
    name = 'voxy'
    allowed_domains = ['voxybg.com']
    start_urls = ['http://voxybg.com/']

    def parse(self, response):
        articles = response.xpath("//div[@class='article_content']")
        for article in articles:
            link = article.xpath(".//div[@class='read-btn']/a/@href").get()
            yield response.follow(link, self.parse_article)

        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(item=Article(), response=response)

        title = response.xpath("//h3/text()").get()

        date = response.xpath("//span[@class='entry-date']/descendant-or-self::*/text()").getall()
        date = date[0]

        author = response.xpath("//span[@class='entry-author']/descendant-or-self::*/text()").getall()
        author = author[0]

        content = response.xpath("//div[@class='article_content']/descendant-or-self::*/text()").getall()
        content = [text.strip() for text in content if format_content(text, title)]
        content = " ".join(content[2:])  # the slice removes the author and date from the article body

        # reformat date
        date_time_obj = datetime.strptime(date, '%B %d, %Y')  # July 15,2020
        date = date_time_obj.strftime("%y/%m/%d")

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('author', author)

        return item.load_item()
