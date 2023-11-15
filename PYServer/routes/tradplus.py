from flask import jsonify
import tools.log as log
import requests

tradplusSDKListUrl = 'https://docs.tradplusad.com/api/sdk/list'
tradplusConfigUrl = 'https://docs.tradplusad.com/api/sdk/config'
tradplusDependsUrl = 'https://docs.tradplusad.com/api/sdk/package'

sdkmapping = {}
adsmapping = {}
addCrossAndAdx = []
# 289: 叁一
valid_code = [  '829'  ]
eromsg = ''

def logInfo( msg ):
    global eromsg
    log.debug(msg)
    eromsg += msg

def InitSDKMapping():
    data = {
        'os': '0'
    }
    r = requests.post(tradplusSDKListUrl, data=data)
    j = r.json()

    data = j['data']
    if None == data:
        logInfo("数据解析异常 未知data")
        return

    androidXSDKlist = data['androidVersions']
    if None == androidXSDKlist:
        logInfo("AndroidX SDK获取失败")
        return

    for sdk in androidXSDKlist:
        sdkmapping[sdk['version']] = sdk['sdkId']

def InitConfig( sdk_version = "10.2.0.1", region = '2'):
    if sdk_version not in sdkmapping.keys():
        logInfo(f"unknow version: {sdk_version}")
        return
    
    data = {
        'os': '1',
        'sdkId':sdkmapping[sdk_version]
    }
    r = requests.post(tradplusConfigUrl, data=data)
    j = r.json()
    if 'data' not in j:
        logInfo('Get config fail')
        return
    d = j['data']
    if 'networks' not in d:
        logInfo('Get networks fail')
        return
    networks = d['networks']
    for network in networks:
        adsmapping[network['nameEn']]=network['networkId']

        if network['isAddCrossAndAdx'] == '1' and network['region'] == region:
            addCrossAndAdx.append(network['networkId'])

def GetDependencies( adsChannel,sdk_version = "10.2.0.1" ):
    if len(adsChannel) == 0:
        logInfo('ads platform count must greater than 0')
        return
    
    if sdk_version not in sdkmapping.keys():
        logInfo(f"unknow version: {sdk_version}")
        return
    
    if len(adsmapping.keys()) == 0:
        logInfo(f"adsmapping init fail")
        return

    ads = []
    print('渠道信息-----------------')
    print(adsChannel)
    print('渠道信息-----------------')
    for c in adsChannel:
        if c in adsmapping.keys():
            ads.append(adsmapping[c])
        else:
            print(f'找不到渠道: {c}')
   
    ads.extend(addCrossAndAdx)
    data = {
        'os': '1',
        'sdkId':sdkmapping[sdk_version],
        'isUnity':'0',
        'isNogradle':'0',
    }
    ads = list(set(ads))
    for i in range( len(ads) ):
        data[f'networkIds[{i}]'] = ads[i]

    print("请求的数据")
    print(data)
    r = requests.post(tradplusDependsUrl, data=data)
    j = r.json()
    print('返回的json')
    print(j)

    if 'data' not in j:
        print('找不到data')
        print(j)
        return
    t = j['data']
    if 'appGradleCode' not in t:
        print('找不到appGradleCode')
        print(t)
        return None
    return t['appGradleCode']


def Run(  sdk_version = "10.2.0.1" ,adsChannel = None ,region = ""):
    print('初始化SDK隐射表')
    InitSDKMapping()
    print('初始化Config')
    InitConfig(sdk_version,region)
    print('拉取依赖')
    appGradleCode = GetDependencies(adsChannel,sdk_version)
    if None == appGradleCode:
        return jsonify({
        "code": 205,
        "err": eromsg
        } )
    
    return jsonify({
        "code": 200,
        "data": appGradleCode,
        'version':','.join(sdkmapping.keys())
        } )

def proc(msg: dict):
    global eromsg
    eromsg = ''
    print('处理Tradplus数据')
    if 'adchannels' in msg.keys():
        req_code = msg['code']
        if req_code not in valid_code:
            return jsonify({
                "code": 204,
                "err": "tradplus has been updated."
            })
        
        adsChannel = msg['adchannels']
        if None != adsChannel:
            adsChannel = adsChannel.split(',')
        else:
            print("adsChannel错误")
            print(adsChannel)

        sdk_version = msg['version']
        region = msg['region']

        print('当前数据信息')
        print(adsChannel)
        print(sdk_version)
        print(region)
        return Run(sdk_version,adsChannel,region)

    return jsonify({
        "code": 404,
        "err": "channels ero."
    })






