from urllib.parse import urlparse, parse_qs, urldefrag, urljoin
import tldextract
import urllib.request, urllib.error
import re

class URLHelper(object):

    def __init__(self):
        pass

    def convert(self, url):
        if not url.startswith('http'):
            return 'http://{url}'.format(url=url)
        return url


    def parse(self, url):
        url = self.convert(url)
        url = self.replace(url)
        parsed_url = urlparse(url)
        self.parsed_url = {
            "scheme": parsed_url.scheme,
            "domain": parsed_url.netloc,
            "paths": parsed_url.path,
            "params": parsed_url.params,
            "queries": parsed_url.query,
            "fragments": parsed_url.fragment,
            "link_hash": self.get_link_hash(url)
        }
        self.__parse_qs()
        self.__parse_domain()
        self.__parse_path()

    def __parse_qs(self):
        self.parsed_url["queries"] = parse_qs(self.parsed_url["queries"])

    def __parse_domain(self):
        splitted_domain = tldextract.extract(self.parsed_url["domain"])
        self.parsed_url["subdomain"] = None if splitted_domain.subdomain == '' else splitted_domain.subdomain
        self.parsed_url["domain"] = splitted_domain.registered_domain



    def __parse_path(self):
        if self.parsed_url["paths"].endswith('/'):
            self.parsed_url["paths"] = self.parsed_url["paths"][:-1]
        elif self.parsed_url["paths"].startswith('/'):
            self.parsed_url["paths"] = self.parsed_url["paths"][1:]

        self.parsed_url["paths"]= self.parsed_url["paths"].split('/')


    def replace(self, url):
        return url.replace('\r', '').replace('\t', '').replace('\n', '').strip()
    
    def check_permission(self, forbidden):
        """
        TODO: To check a url has a permission to be crawled depends on query paramater or a text.
        """

    def match(self):
        """
        TODO: Match websites and url depends on path
        """

    def validate(self, url):
        valid = False
        if url.startswith('http'):
            url = url.strip()
            if not ' ' in url:
                valid = True
        return valid

    def urldefrag(self, url):
        return urldefrag(url).url

    def get_status_code(self, url):
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            return e.code
        except urllib.error.URLError as e:
            return 400
        else:
            return 200

    def is_url(self, cand):
        if re.match('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', cand):
            return True
        return False

    
    def urlify(self, cand, domain):
        if not self.is_url(cand):
            return urljoin(domain, cand)
        return cand

    
    def modify_domain(self, origin, canon):
        parsed_canon = urllib.parse.urlparse(canon)
        parsed_origin = urllib.parse.urlparse(origin)
        return parsed_canon._replace(netloc=parsed_origin.netloc).geturl()

    def get_link_hash(self, link):
        if link is not None:
            link = link.replace("'","").replace('"', '')
            return hashlib.md5(link.encode("utf-8")).hexdigest()
        else:
            return None




