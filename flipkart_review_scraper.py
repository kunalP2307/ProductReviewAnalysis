from pathlib import Path
import scrapy


class FlipkartProdReview(scrapy.Spider):
    name = "product_review"
    url_a = 'https://www.flipkart.com/apple-iphone-14-starlight-128-gb/product-reviews/itm3485a56f6e676?pid=MOBGHWFHABH3G73H&lid=LSTMOBGHWFHABH3G73HVXY5AV&marketplace=FLIPKART'
    count = 0
    custom_settings = {
        'FEEDS': { 'data.csv': { 'format': 'csv', 'overwrite': True}}
        }

    def start_requests(self):
        url = 'https://www.flipkart.com/apple-iphone-14-starlight-128-gb/product-reviews/itm3485a56f6e676?pid=MOBGHWFHABH3G73H&lid=LSTMOBGHWFHABH3G73HVXY5AV&marketplace=FLIPKART'
        yield scrapy.Request(url=url, callback=self.parse)

    # def parse_resulting(self, response):
    #     element = response.css('._1LKTO3')[-1]
    #     if element.css('span::text').get() == 'Next':
    #         url = element.css('::attr(href)').get() 
    #         print(url)
    #         yield scrapy.Request(url= 'https://www.flipkart.com' + url, callback=self.parse)
    
    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        #
        location = []
        rating = response.css('._3LWZlK::text').getall()[1:]
        review_title = response.css('._2-N8zT::text').getall()
        review_description = response.css('.t-ZTKy div > div::text').getall()
        # date = response.css('._2sc7ZR::text').getall()
        date = []
        votes = response.css('._3c3Px5::text').getall()
        
        for row in response.css('._3n8db9'):
            date.append(row.css('p::text').getall()[1])
            location.append(row.css('p span::text').getall()[1])
          
        for i in range(len(rating)):
            yield{
                'rating' : rating[i],
                'review_title' : review_title[i],
                'review_description':review_description[i],
                'date' : date[i],
                'location': location[i],
                'up_votes' : votes[i*2],
                'down_votes': votes[(i*2) +1]
            }
        
        # element = response.css('._1LKTO3')[-1]
        # if element.css('span::text').get() == 'Next':
        #     url = element.css('::attr(href)').get() 
        #     if count < 10:
        #         url_new = 'https://www.flipkart.com'+url 
        #         yield response.follow(url_new, callback=self.parse)
    
        for i in range(2,100):
            url = 'https://www.flipkart.com/apple-iphone-14-starlight-128-gb/product-reviews/itm3485a56f6e676?pid=MOBGHWFHABH3G73H&lid=LSTMOBGHWFHABH3G73HVXY5AV&marketplace=FLIPKART&page='+str(i)
            yield response.follow(url, callback=self.parse)
    
            # yield {'Text': title,
            #        'Author': author,
            #        "Tags": tags
            #     }   
            
