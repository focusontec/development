
import Queue

user_list = [{'18864932834':'ZHao1990625'},{"15600728162":"0p-0p-0op"}]

def getUlistQueue(user_dict):
    secret_que = Queue.Queue()
    for user_dict in user_list:
        secret_que.put(user_dict)

    return secret_que



