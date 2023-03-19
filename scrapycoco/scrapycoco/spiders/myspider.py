import scrapy
import ssl
import cryptography
import scrapy.core.downloader.contextfactory
class MySpider(scrapy.Spider):
    name = 'myspider'

    start_urls = [
        'https://twitter.com/robots.txt',
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'ROBOTSTXT_USER_AGENT': 'MyBot/1.0',
        'TLS_VERSION': ssl.PROTOCOL_TLSv1_2,
        'DOWNLOADER_CLIENTCONTEXTFACTORY': 'scrapy.core.downloader.contextfactory.BrowserLikeContextFactory',
        'CIPHERS': "DEFAULT:@SECLEVEL=1",
        'scrapy.core.downloader.contextfactory.SSL_VERSION': 'TLSv1',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapycoco.middlewares.CustomRobotMiddleware': 100
        }
    }

    def parse(self, response):
        self.logger.info(f'Response URL: {response.url}')
        yield {
            'url': response.url,
            'text': response.text
        }
