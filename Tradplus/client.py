#默认服务端口

import requests 
import time
import implant

api = 'https://www.geek7.top:8000/api'
adsChannel = ['UnityAds']
region = '2' # 1: 中国  2: 其它地区


adsChannel.clear()
def log( msg ):
    print( msg )

def InitChannel():
    adsChannel.clear()
    with open('./bin/ads','r') as fp:
        for line in fp.readlines():
            adsChannel.append(line.replace('\n',''))


def Run( sdk_version = "10.2.0.1" ):
    InitChannel()
    data = {
        'token' : time.time(),
        'pipe':'tradplussdk',
        'code':829,
        'adchannels':','.join(adsChannel),
        'version':sdk_version,
        'region' : region
    }
    res = requests.get(api,data) 
    j = res.json()
    if 'data' not in j:
        log('erro: data not in depends')
        return
    appGradleCode = j['data']
    if None == appGradleCode:
        log('GetDependencies fail')
    else:
        print('input you "Assets\\Plugins\\Android" full path')
        print('example: D:\\Git\\2dtoilet\\2dtoilet-client\\Assets\\Plugins')
        print('Or you can try the Android folder to this window.')
        srcpath = input('input proj:\n')
        realpath = srcpath.replace('\\','/')
        implant.Run(realpath,appGradleCode)

if __name__ == "__main__":
    log('begin.')

    version = input('input you tradplus version: ')
    print(f'pulling the current version dependency of Tradplus: {version}')
    Run( version )

    log('end.')