import os
import json
import mitmproxy.http
from mitmproxy import ctx
import time
from datetime import datetime
import xlwt


 
class Counter:
    def __init__(self):
        self.num = 0
        self.requestNum = 0
        self.responseOrErrorNum = 0
        self.aa = 0
        now = datetime.now()
        now = now.strftime("%Y-%m-%d_%H_%M_%S")
        self.save_to = '../url/'+now+'.xls'
        if not os.path.exists(self.save_to):
            os.system('touch '+self.save_to)
        # self.all_arr = [['请求路径','请求域名','请求path','cookies','请求大小(b)','响应大小','响应类型','请求响应时间差(s)','请求开始时间','请求响应结束时间']]
        self.all_arr = [['请求路径', 'cookies']]
 
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        flow.customField = []
 
    
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'login' in flow.request.url:
            time.sleep(1.3)
            os.system('adb -s 10.249.243.227:5555 shell input keyevent 4')
            time.sleep(0.8)
            os.system('adb -s 10.249.243.227:5555 shell input keyevent 4')
            # time.sleep(1)
            # os.system('adb -s 10.249.243.227:5555 shell input keyevent 4')
        if not 'comment' in flow.request.url:
            return
        
        self.num = self.num + 1
        self.requestNum = self.requestNum+1
        flow.start_time = time.time()
        flow.customField = [flow.request.url, json.dumps(dict(flow.request.cookies))]
        self.all_arr.append(flow.customField)
 
 
    def response(self, flow):
        self.aa = self.aa + 1
        self.responseOrErrorNum = self.responseOrErrorNum+1
        flow.end_time = time.time()
        
        # if self.num % 400 == 0:
        #     self.save_to = 'url_'+str(self.num)+'.xls'
                
        self.save_excel(self.all_arr,self.save_to)
 
 
    def save_excel(self,array,filename):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('test')
        for x in range(len(array)):
            for y in range(len(array[x])):
                worksheet.write(x, y, array[x][y])
        workbook.save(filename)
 

addons = [
    Counter()
]