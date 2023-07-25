import datetime
from flask import Flask
from flask import request, jsonify
from channel import channel_manager
from apscheduler.schedulers.blocking import BlockingScheduler
import hot_update

app = Flask(__name__)

def request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/callApi')
def callApi():
    data = request_parse(request)
    try:
        # 验证token
        token = data.get('token')

        # 验证不通过 返回错误代码
        if not token:
            return jsonify({
                "code": 401,
                "err": "error token."
            })

        # 获取处理的管线
        channel = data.get('channel')
        if not channel:
            return jsonify({
                "code": 401,
                "err": "not contains channel."
            })

        # 派遣任务
        res = channel_manager.dispatch(data)
        if None != res:
            return res

        # 未找到对应的管线
        return jsonify({
            "code": 404,
            "err": "channel not found."
        })

    # 异常反馈
    except Exception as e:
        return jsonify({
            "code": 412,
            "err": str(e)
        })


def openserver():
    print('服务器启动中.....')
    app.run(host="0.0.0.0", port=8091, ssl_context=('./certificate/www.geek7.top.crt', './certificate/www.geek7.top.key'))

def dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,1分钟更新15次
    scheduler.add_job(channel_manager.update, 'interval', seconds=60/15, id='main_thread_tick')
    # 延时一秒执行一次
    scheduler.add_job(openserver,'date', run_date=datetime.datetime.now()+datetime.timedelta(seconds=1))
    scheduler.start()

if __name__ == '__main__':
    hot_update.start()
    dojob()
    