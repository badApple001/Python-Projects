import requests 
#引入requests库
res = requests.get('https://www.geek7.top:8091/login') 
#发送请求，并把响应结果赋值在变量res上
print(res)
#用print输出返回的响应

