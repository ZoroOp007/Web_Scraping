# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip all whitespaces

        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value[0].strip()

        ## Category and productype --> Switch to lowercase
            
        lowercase_keys = ['category','product_type']

        for lowercase_key in lowercase_keys:
            value = adapter[lowercase_key]
            adapter[lowercase_key] = value.lower()

        ## Price --> convert to float
            
        price_keys = ['tax','price']

        for price_key in price_keys:
            value = adapter[price_key]
            value = value.replace('£','')
            adapter[price_key] = float(value)

        ## Availiabilty --> Extract number of books in Stock
            
        availability_string = adapter.get('availability')

        split_string_array = availability_string.split('(')

        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split()
            adapter['availability'] = int(availability_array[0])


        ## Reviews --> to integer
            
        value = adapter['num_reviews']

        adapter['num_reviews'] = int(value)

        ## Star-rating --> to integer

        rating_string = adapter['stars']
        rating_array = rating_string.split(" ")
        star_text_value = rating_array[1].lower()
        
        if star_text_value == 'one':
            adapter['stars'] = 1
        elif star_text_value == 'two':
            adapter['stars'] = 2
        elif star_text_value == 'three':
            adapter['stars'] = 3
        elif star_text_value == 'four':
            adapter['stars'] = 4
        elif star_text_value == 'five':
            adapter['stars'] = 5
        else:
            pass
        
        return item
    

# Saving Data Directly to Database
    

import mysql.connector

class SaveToMySQL_Pipeline:

    ## connecting to mysql database
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'books')
        
    ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()  

    ## Create books table if none exists
        self.cur.execute ( """
        CREATE TABLE IF NOT EXISTS books(
                         id int NOT NULL auto_increment,
                         title text,
                         product_type VARCHAR(255),
                         availability INTEGER,
                         num_reviews INTEGER,
                         stars INTEGER,
                         category VARCHAR(255),
                         price DECIMAL,
                         tax DECIMAL,
                         PRIMARY KEY (id)
                         )
        """)
    
    def process_item (self,item,spider):
        self.cur.execute("""
        INSERT INTO books 
                         (title,product_type,availability,num_reviews,stars,category,price,tax)
                         values(%s,%s,%s,%s,%s,%s,%s,%s)""",
                         (item["title"],item["product_type"],item["availability"],item["num_reviews"],item["stars"],item["category"],item["price"],item["tax"]))
        
        ## Execute insert of data in database

        self.conn.commit()
        return item
    
    ## Close cursor and Database Connection

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()

                         
