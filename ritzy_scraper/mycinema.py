
# coding: utf-8

# In[2]:

import scrapy


class CinemaSpider(scrapy.Spider):
    name = "cinema"
    allowed_domains = ['picturehouses.com' ]
    start_urls = [
        'https://www.picturehouses.com/cinema/Ritzy_Picturehouse/Whats_On'
    ]

    def parse(self, response):
        movie_names = response.css('.row h2 ::text').extract()
        for movie_name in movie_names:
            yield {
                'name': movie_name
            }

