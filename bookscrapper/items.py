# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass



class BookItem(scrapy.Item):
    
    title = scrapy.Field()
    product_type = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    tax = scrapy.Field()