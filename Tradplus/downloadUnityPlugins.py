import requests
import zipfile
import tempfile
import os

def get_data( url ):
    response = requests.get(url)
    return url, response.content

def dowanlodZip( url , dest = "./zip"):
    url, data = get_data( url )  # data为byte字节
    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
    print(_tmp_file)
 
    _tmp_file.write(data)  # byte字节数据写入临时文件
    # _tmp_file.seek(0)
    
    print(f'extract to: {os.path.join(os.getcwd(),dest)}')
    zf = zipfile.ZipFile(_tmp_file, mode='r')
    for names in zf.namelist():
        f = zf.extract(names, dest)  # 解压到zip目录文件下
        print(f)
    zf.close()
    print('extract completed')

 
