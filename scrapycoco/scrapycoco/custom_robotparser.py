import urllib.robotparser
from pprint import pprint
from urllib import request
from urllib.robotparser import RobotFileParser
import unicodedata


class CustomRobotParser(urllib.robotparser.RobotFileParser):
    def __init__(self, url='', verify_ssl=True):
        super().__init__(url)
        self.verify_ssl = verify_ssl
        self.allowed_urls = []
        self.disallowed_urls = []

    def read(self):
        if self.url:
            req = request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with request.urlopen(req, timeout=10, context=None if self.verify_ssl else ssl._create_unverified_context()) as response:
                if response.status == 200 or response.status == 404:
                    pprint(str(response.readlines()[0],encoding='ascii'))
                    self.parse(response.readlines())
                else:
                    raise ValueError('Invalid URL or non-200 response: %s' % response.status)
        else:
            raise ValueError('URL must be set')

    def parse(self, lines):
        """Parse the input lines from a robots.txt file."""
        self.disallow_all = False
        self.allow_all = False
        self.set_url(None)
        self.last_modified = None
        self.expires = None
        self.crawl_delay = None
        self.sitemaps = []
        #pprint(lines)
        lines = [line.replace('\n','') for line in lines]
        # Handle non-ASCII characters
        lines = [str(line, encoding='ascii') for line in lines]

        # Now parse the lines
        for line in lines:
            # Remove comments
            if "#" in line:
                i = line.find("#")
                line = line[:i]
            # Remove leading and trailing whitespace
            line = line.strip()
            # Skip blank lines
            if not line:
                continue

            # Split the line into fields
            try:
                field, value = line.split(":", 1)
            except ValueError:
                continue
            # Remove leading and trailing whitespace from the field and value
            field = field.strip().lower()
            value = value.strip()

            # Parse the field
            if field == "user-agent":
                if value == "*" or value == self.agent:
                    self.last_checked = None
                else:
                    continue
            elif field == "disallow":
                if self.allow_all:
                    continue
                self.disallow_all = False
                self.add_disallow(value)
            elif field == "allow":
                if self.disallow_all:
                    continue
                self.allow_all = False
                self.add_allow(value)
            elif field == "crawl-delay":
                self.crawl_delay = float(value)
                self.allow_all = True
                self.disallow_all = True
            elif field == "sitemap":
                self.sitemaps.append(value)
            elif field == "last-modified":
                self.last_modified = value
            elif field == "expires":
                self.expires = value
            elif field == "host":
                self.host = value
                self.allow_all = True
                self.disallow_all = True
    def allow(self, url, user_agent='*'):
        if self.allow_all:
            return True
        elif self.disallow_all:
            return False
        else:
            if url in self.allowed_urls:
                return True
            elif url in self.disallowed_urls:
                return False
            else:
                return True
