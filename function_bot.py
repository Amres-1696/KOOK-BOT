import time
import json
import random
import requests
from urllib.parse import urlencode


def count_down(lotto_time,config,number):
    """计时"""
    lotto_time = lotto_time*3600
    while lotto_time > 0:
        time.sleep(1)
        lotto_time -= 1
    return get_user_id(config,number)


def get_user_id(config,number):
    """获取抽奖信息下的✋回应的用户id"""
    params = {
        'msg_id': config['msg_id'],
        'emoji': config['emoji'],
        'sort': 'id',
    }
    headers = {
        'Authorization': f'Bot {config["bot_token"]}',
    }
    url = 'https://www.kookapp.cn/api/v3/message/reaction-list'  # kook的api 

    req = requests.get(url=url, headers=headers,params=urlencode(params))
    reques = json.loads(req.text)
    return winner(reques['data'],number)

def winner(users : list,number):
    """随机抽取中奖用户"""
    users_id = [users[u]['id'] for u in range(len(users))]
    if number == 1:
        winner_index = random.randint(0,len(users_id)-1)
        return [users_id[winner_index]]
    else:
        winner_indices = random.sample(list(range(0, len(users_id) - 1)), number)
        return [users_id[n] for n in winner_indices]



