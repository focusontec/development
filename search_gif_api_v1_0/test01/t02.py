import requests
import time
import threadpool
i = 1
while 1:
    requests.head('http://47.91.216.106:5000/api/v1.0/gif/searchByQuery/baidu?query=%E6%90%9E%E7%AC%91')
    # time.sleep(0.1)
    print '%d'%i
    i+=1