# -*- coding: utf-8 -*-

# Scrapy settings for Curling project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from urllib import quote_plus as urlquote
BOT_NAME = 'Curling'

SPIDER_MODULES = ['Curling.spiders']
NEWSPIDER_MODULE = 'Curling.spiders'

LOG_LEVEL = "DEBUG"
# LOG_FILE = 'play_by_play.logs'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Curling (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Curling.middlewares.CurlingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "Curling.middlewares.RotateUserAgentMiddleware": 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Curling.pipelines.PGStorePipeline': 300,
    'Curling.pipelines.JsonFilePipeline':500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#数据库配置
PG_HOST = 'rm-2zen988pb49xf833mo.pg.rds.aliyuncs.com'
PG_PORT = 3432
PG_DB = 'winter_olympics'
PG_USR = 'cdy038'
PG_PWD = 'wf25shjcrzali$Mix%tMt@'
PG_SCHEMA = 'www_worldcurling_org'
PG_CONN = 'postgresql://{}:{}@{}:{}/{}'.format(PG_USR, urlquote(PG_PWD), PG_HOST, PG_PORT, PG_DB)
PG_KWARGS = {'database': PG_DB, 'user': PG_USR, 'password': PG_PWD, 'host': PG_HOST, 'port': PG_PORT}

