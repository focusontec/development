# coding=utf-8
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisMixin
from scrapy_redis.utils import bytes_to_str
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from tools import handel_re
import logging as log


class MyRedisMixin(RedisMixin):
    redis_key = None
    redis_batch_size = None
    redis_encoding = None
    server = None
    logger = log
    base_api = None
    base_re = None
    http_save_id_re = None
    http_error_save = False

    # 重写 setup_redis 方法
    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if crawler is None:
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        # 注册结束信号，这样，就能够在结束时调用
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

        if self.server is not None:
            return

    # 重写 next_requests 方法
    def next_requests(self):
        """Returns a request to be scheduled or none."""
        if self.server is None:
            self.logger.error("ERROR server know")
            return
        else:
            pass

        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = self.server.get()
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    # 处理 HTTP 错误
    def err_back_http_bin(self, failure):
        response = failure.value.response
        spider = failure.tb.tb_frame.f_locals.get('spider')
        try:
            url = response.meta['item']['url']
        except Exception as e:
            self.logger.info("Not response item url : {}".format(e.message))
            url = response.url

        status = response.status
        spider_name = None
        try:
            spider_name = unicode(spider.name).split(":")[2]
        except Exception as e:
            self.logger.error(e.message)

        if failure.check(DNSLookupError):
            self.logger.error('status {},DNSLookupError on {}'.format(status, url))
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('status {},TimeoutError on {}'.format(status, url))
        elif failure.check(HttpError):
            self.logger.error('status {},HttpError on {}'.format(status, url))
        else:
            self.logger.error('status {},OtherError on {}'.format(status, url))

        game_id = handel_re(self.http_save_id_re, url)
        if game_id:
            game_id = ''.join(game_id)

        # 更改插入值为对应的 http error code
        if (spider_name and game_id) is not None:
            status_code = 9999
            try:
                status_code = int(status)
            except Exception as e:
                self.logger.error(e.message)

            self.server.change_column_num(
                column=spider_name, value=status_code, game_id=game_id
            )

    def make_request_from_data(self, data):
        """
        重写 make_requests_from_url
        在里面重写 Requests 的调用方法
        """
        item = dict()
        item['url'] = data
        url = bytes_to_str(data, self.redis_encoding)
        return Request(url, dont_filter=True, meta={'item': item}, errback=self.err_back_http_bin)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        try:
            self.schedule_next_requests()
        except Exception as e:
            self.logger.error(e.message)

        raise DontCloseSpider


class MySpider(MyRedisMixin, Spider):
    """
    Spider that reads urls from redis queue when idle.
    """

    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(MySpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis()
        return obj


class CycleSpider(Spider):
    """
    这个程序是一个自运行的程序，注册一个下一步的获取函数
    """
    keep_next_requests = True

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        # spider_idle spider 空闲
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.open, signal=signals.spider_opened)

    def spider_idle(self):
        if self.keep_next_requests:
            try:
                self.schedule_next_requests()
            except Exception as e:
                self.logger.error(e.message)
                raise DontCloseSpider
        else:
            pass

    def open(self, spider):
        """ 开启spider """
        pass

    def schedule_next_requests(self):
        """Schedules a request if available"""
        # TODO: While there is capacity, schedule a batch of redis requests.
        for req in self.next_requests(crawler=self.crawler):
            self.crawler.engine.crawl(req, spider=self)

    def next_requests(self, crawler):
        return []

    # 处理 HTTP 错误
    def err_back_http_bin(self, failure):
        response = failure.value.response
        spider = failure.tb.tb_frame.f_locals.get('spider')
        try:
            url = response.meta['item']['url']
        except Exception as e:
            self.logger.info("Not response item url : {}".format(e.message))
            url = response.url

        status = response.status
        spider_name = None
        try:
            spider_name = unicode(spider.name).split(":")[2]
        except Exception as e:
            self.logger.error(e.message)

        if failure.check(DNSLookupError):
            self.logger.error('status {},DNSLookupError on {}'.format(status, url))
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('status {},TimeoutError on {}'.format(status, url))
        elif failure.check(HttpError):
            self.logger.error('status {},HttpError on {}'.format(status, url))
        else:
            self.logger.error('status {},OtherError on {}'.format(status, url))
