from flask import Flask
from flask import request, jsonify
from tools.LockIP import IPStatus,check
import routes.route as route
 
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


@app.route('/api')
def callApi():
    ip = request.remote_addr

    status = check(ip)
    if status == IPStatus.Lock:
        return jsonify({
                "code": 202,
                "err": "你已在黑名单中"
            })
    
    if status == IPStatus.Suspicion:
        return jsonify({
                "code": 201,
                "err": "请稍后再尝试"
            })

    # 主逻辑
    data = request_parse(request)
    print('get req:')
    print(request.args)
    try:
        # 验证token
        return route.proc(data)
    
    # 异常反馈
    except Exception as e:
        print("异常========================")
        print(e)
        return jsonify({
            "code": 400,
            "err": str(e)
        })


def openserver():
    print('服务器启动中.....')
    app.run(host="0.0.0.0", port=8000, ssl_context=(
        './certificate/www.geek7.top.crt', './certificate/www.geek7.top.key'))

if __name__ == '__main__':
    openserver()
