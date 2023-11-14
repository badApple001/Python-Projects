import time
from enum import Enum

request_history = {}  #请求历史信息 包含ip 最后一次请求时间戳 频繁请求计数 违规次数
blacklist = [] #黑名单 通知一次玩家已经是在黑名单了
locklist = []  #锁定列表 返回空字符串


class IPStatus(Enum):
     General = 1    
     Lock = 2
     Suspicion = 3


def check( ip ):
    # 锁定ip列表
    if ip in locklist:
        return IPStatus.Lock

    # 黑名端 会通知一次客户端
    if ip in blacklist:
        locklist.append(ip)
        return IPStatus.Suspicion

    # 1秒内请求限制5次
    if ip not in request_history.keys():
        request_history[ip] = [time.time(), 1, 0 ]  # 最近call的时间, 短时间内调用的次数, 频繁计数
    else:
        if time.time() - request_history[ip][0] < 1:
            request_history[ip][1] += 1
            # 频繁请求 违规处理
            if request_history[ip][1] >= 5:
                #违规次数统计
                request_history[ip][2] += 1
                if request_history[ip][2] >= 5:
                    blacklist.append(ip) #加入黑名端
                return IPStatus.Suspicion
        else:
            request_history[ip][1] = 1
        request_history[ip][0] = time.time()
    return IPStatus.General