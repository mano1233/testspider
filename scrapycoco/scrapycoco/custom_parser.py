import urllib.robotparser

class CustomRobotParser(urllib.robotparser.RobotFileParser):
    def __init__(self, url=''):
        super().__init__(url)
        self.allow_all = False
        self.disallow_all = False
        self.allowed_urls = []
        self.disallowed_urls = []

    def read(self):
        super().read()
        self.allowed_urls = []
        self.disallowed_urls = []
        for (user_agent, rules) in self.entries:
            if user_agent == '*' or user_agent == 'MyBot/1.0':
                for rule in rules:
                    if rule.allowance:
                        self.allowed_urls.append(rule.rule)
                    else:
                        self.disallowed_urls.append(rule.rule)

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
