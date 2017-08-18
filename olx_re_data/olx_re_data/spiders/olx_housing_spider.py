import scrapy

DEFAULT_MAX = 100

class OLXHousingListSpider(scrapy.Spider):
    name = "olx_housing"
    root_url = 'https://www.olx.ph'
    start_urls = [
        'https://www.olx.ph/real-estate/real-estate-for-sale/apartment-condominium',
    ]

    def parse(self, response):
        page = response.url.split("?page=")
        if len(page) != 2:
            page = 1
        else:
            page = int(page[-1])
        print(response.url.split("?page="))
        filename = 'test-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        # if there's another page or you haven't reached the max pages yet, crawl next
        max_page = getattr(self, 'max_page', None)
        max_page = int(max_page) if max_page else DEFAULT_MAX
        has_next = page < max_page
        next_url = response.css('li.pagination-next a::attr(href)').extract_first()
        if next_url and has_next:
            print(next_url)
            yield scrapy.Request(self.root_url+next_url, self.parse)

    def parse_listing(self, response):
        pass