import requests
import implant

tradplusSDKListUrl = 'https://docs.tradplusad.com/api/sdk/list'
tradplusConfigUrl = 'https://docs.tradplusad.com/api/sdk/config'
tradplusDependsUrl = 'https://docs.tradplusad.com/api/sdk/package'
adsChannel = ['UnityAds']

sdkmapping = {}
adsmapping = {}
addCrossAndAdx = []
region = '2' # 1: 中国  2: 其它地区

def log( msg ):
    print( msg )

def InitSDKMapping():
    data = {
        'os': '0'
    }
    r = requests.post(tradplusSDKListUrl, data=data)
    j = r.json()

    data = j['data']
    if None == data:
        log("数据解析异常 未知data")
        return

    androidXSDKlist = data['androidVersions']
    if None == androidXSDKlist:
        log("AndroidX SDK获取失败")
        return

    for sdk in androidXSDKlist:
        sdkmapping[sdk['version']] = sdk['sdkId']

def InitConfig( sdk_version = "10.2.0.1"):
    if sdk_version not in sdkmapping.keys():
        log(f"unknow version: {sdk_version}")
        return
    
    data = {
        'os': '1',
        'sdkId':sdkmapping[sdk_version]
    }
    r = requests.post(tradplusConfigUrl, data=data)
    j = r.json()
    if 'data' not in j:
        log('Get config fail')
        return
    d = j['data']
    if 'networks' not in d:
        log('Get networks fail')
        return
    networks = d['networks']
    for network in networks:
        adsmapping[network['nameEn']]=network['networkId']

        if network['isAddCrossAndAdx'] == '1' and network['region'] == region:
            addCrossAndAdx.append(network['networkId'])

def GetDependencies( sdk_version = "10.2.0.1" ):
    if len(adsChannel) == 0:
        log('ads platform count must greater than 0')
        return
    
    if sdk_version not in sdkmapping.keys():
        log(f"unknow version: {sdk_version}")
        return
    
    ads = []
    for channel in adsChannel:
        if channel in adsmapping.keys():
            ads.append(adsmapping[channel])
        else:
            log(f'channel absence: {channel}')
    ads.extend(addCrossAndAdx)
    data = {
        'os': '1',
        'sdkId':sdkmapping[sdk_version],
        'isUnity':'0',
        'isNogradle':'0',
    }
    for i in range( len(ads) ):
        data[f'networkIds[{i}]'] = ads[i]

    r = requests.post(tradplusDependsUrl, data=data)
    j = r.json()
    if 'data' not in j:
        log('fail dependen')
        return
    data = j['data']
    if 'appGradleCode' not in data:
        log('not found apps build.gradle')
        return
    return data['appGradleCode']

def InitChannel():
    adsChannel.clear()
    with open('./bin/ads','r') as fp:
        for line in fp.readlines():
            adsChannel.append(line.replace('\n',''))

def Run(  sdk_version = "10.2.0.1" ):
    InitChannel()
    InitSDKMapping()
    InitConfig(sdk_version)
    appGradleCode = GetDependencies(sdk_version)
    if None == appGradleCode:
        log('GetDependencies fail')
        return
    srcpath = input('input proj:\n')
    realpath = srcpath.replace('\\','/')
    implant.Run(realpath,appGradleCode)

Run()



## 输出当前 Tradplus 广告渠道key
# with open('./tradplus sdk key list.txt','w+') as fp:
#     fp.write('\n'.join(adsmapping.keys()))


## 输出当前 Tradplus 广告渠道ID
# with open('./tradplus sdk ID list.txt','w+') as fp:
#     fp.write('\n'.join(adsmapping.values()))