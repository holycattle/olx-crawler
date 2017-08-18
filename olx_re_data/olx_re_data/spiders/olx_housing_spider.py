import scrapy
import sqlite3
import os

DEFAULT_MAX = 100

LOCATION = "Location:"
CONDITION = "Propertycondition:"
BEDS = "Bed:"
BATHS = "Bath:"
FLOOR_SIZE = "Floor:"
AD_ID = "Ad ID:"


class OLXHousingListSpider(scrapy.Spider):
    name = "olx_housing"
    root_url = 'https://www.olx.ph'
    start_urls = [
        'https://www.olx.ph/real-estate/real-estate-for-sale/apartment-condominium',
    ]

    def parse(self, response):
        page = response.url.split("?page=")
        page = 1 if len(page) != 2 else int(page[-1])

        # parse each listing on the page
        for href in response.css("div.item div.link a[itemprop='url']::attr(href)"):
            yield response.follow(self.root_url+href.extract(), self.parse_listing)

        # if there's another page or you haven't reached the max pages yet, crawl next
        max_page = getattr(self, 'max_page', None)
        max_page = int(max_page) if max_page else DEFAULT_MAX
        has_next = page < max_page
        next_url = response.css('li.pagination-next a::attr(href)').extract_first()
        if next_url and has_next:
            yield scrapy.Request(self.root_url+next_url, self.parse)

    def parse_listing(self, response):
        def extract_from_css(query):
            return response.css(query).extract_first().strip()
        detail_keys = response.xpath('//div[contains(@class, "details")]/\
div/ul/li/span[contains(@class, "key")]/text()')
        detail_vals = response.xpath('//div[contains(@class, "details")]/\
div/ul/li/span[contains(@class, "value")]/text()')

        details = {}
        for i, k in enumerate(detail_keys):
            details[k.extract().strip()] = detail_vals[i].extract().strip()

        listing = {
            'title': extract_from_css('h1.title-name::text'),
            'creator': extract_from_css('span.username a[rel="nofollow"]::text'),
            'creator_address': extract_from_css('span.title-meta\
[name="seller_location"]::text'),
            'price': int(extract_from_css('h2.price-value::text').replace(',', '').split(' ')[1]),
            # everything is for sale because of the URL
            'for_rent': True,
            'post_address': details.get(LOCATION),
            'condition': details.get(CONDITION),
            'beds': details.get(BEDS),
            'baths': details.get(BATHS),
            'floor_size': details.get(FLOOR_SIZE),
            'ad_id': details.get(AD_ID),
        }
        # HACK T_T
        conn = sqlite3.connect('sql/olx_re_data.db')
        c = conn.cursor()
        lv = list(listing.values())
        c.execute('''INSERT INTO listings
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', tuple(lv))
        conn.commit()
        conn.close()
        yield listing
