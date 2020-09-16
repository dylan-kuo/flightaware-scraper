import scrapy


class FlightSpider(scrapy.Spider):
    name = "flights"

    custom_settings = {
        'ROBOTSTXT_OBEY': False  
    }

    def start_requests(self):
        urls = [
            'https://flightaware.com/live/aircrafttype/PC12', # Pilatus PC-12 
            'https://flightaware.com/live/aircrafttype/C208', # Cessna Caravan 
            'https://flightaware.com/live/aircrafttype/BE20', # Beechcraft Super King Air 200 
            'https://flightaware.com/live/aircrafttype/C560', # Cessna Citation Excel/XLS
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//*[@class="prettyTable fullWidth"]//tr'):
            yield {
                'ident': row.xpath('td[1]//a//text()').extract_first(),
                'type': row.xpath('td[2]//text()').extract_first(),
                'origin': row.xpath('td[3]//text()').extract_first(),
                'destination': row.xpath('td[4]//text()').extract_first(),
                'departure': row.xpath('td[5]//text()').extract_first(),
                'est_arrive_time': row.xpath('td[6]//text()').extract_first(),
                'est_time_enroute': row.xpath('td[7]//text()').extract_first(),
            }
        next_page_url = response.xpath('//a[contains(text(), "Next")]/@href').extract_first()

        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
