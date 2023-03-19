from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.httpobj import urlparse_cached
from .custom_robotparser import CustomRobotParser
from pprint import pprint


class CustomRobotMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Instantiate the middleware using the settings from the Scrapy project
        s = cls()
        s.robotstxt_user_agent = crawler.settings.get('ROBOTSTXT_USER_AGENT')
        s.robotstxt_obey = crawler.settings.getbool('ROBOTSTXT_OBEY')
        return s

    def __init__(self):
        self.robotstxt_user_agent = None
        self.robotstxt_obey = True
        self.parsers = {}

    def process_request(self, request, spider):
        if request.url.startswith("https"):
            request.meta['verify'] = False
        if self.robotstxt_obey:
            rp = self.get_robot_parser(request, spider)
            if rp and not rp.allow(request.url, self.robotstxt_user_agent):
                # Return a HTTP 403 Forbidden response if the URL is not allowed
                return response_forbidden('URL not allowed by robots.txt')

    def get_robot_parser(self, request, spider):
        # Get the base URL for the request and find the corresponding robots.txt URL
        url = urlparse_cached(request)
        pprint(url.scheme)
        rp_url = url.scheme + '://' + url.netloc + '/robots.txt'

        # Check if a robot parser already exists for the base URL
        if rp_url not in self.parsers:
            # Create a new robot parser and parse the robots.txt file
            rp = CustomRobotParser(rp_url)
            rp.read()
            self.parsers[rp_url] = rp

        return self.parsers[rp_url]
