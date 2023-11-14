from flask import request, jsonify
import routes.tradplus as tradplus

def proc( data ):

    pipe = data.get('pipe')
    if pipe == 'tradplussdk':
        print('tradplussdk proc')
        return tradplus.proc( data )
    return jsonify({
                "code": 203,
                "err": "未找到pipe"
            })