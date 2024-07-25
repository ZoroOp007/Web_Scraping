import scrapy

from bookscrapper.items import BookItem

class Bookspider3Spider(scrapy.Spider):
    name = "bookspider3"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    custom_settings = {
        'FEEDS' : {
            'booksdata.json' : {'format' : 'json', 'overwrite':True},
            'booksdata.csv' : {'format' : 'csv', 'overwrite' : True}
        }
    }

    def parse(self, response):
        books = response.css(".product_pod")

        for book in books:
             book_url = book.css("h3 a::attr(href)").get()

             full_book_url = "https://books.toscrape.com/catalogue/" + book_url

             yield response.follow(full_book_url , callback = self.display)

        next_page = response.css(".next a::attr(href)").get()

        if next_page is not None:

            if '/catalogue' not in next_page:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/" + next_page
            
            yield response.follow(next_page_url , self.parse)


    def display(self, response):

        rows = response.css("table tr")

        book_item = BookItem()


        book_item['title'] =  response.css(".product_main h1::text").get(),
        book_item['category'] = response.xpath("//ul [@class = 'breadcrumb']/ li [@class = 'active']/preceding-sibling:: li[1]/a/text()").get(),
        book_item['price'] = response.css(".product_main .price_color::text").get(),
        book_item['stars'] = response.css(".star-rating::attr(class)").get(),
        book_item['availability'] = rows[5].css("td::text").get(),
        book_item['num_reviews'] = rows[6].css("td::text").get(),
        book_item['product_type'] = rows[1].css("td::text").get(),
        book_item['tax'] = rows[4].css("td::text").get(),
 
        yield book_item