import http.client
import re
import time
import datetime
import urllib.parse
import urllib.request
import urlhandle
import getopt
import sys
import requests
import request_fix
import json
import os 
from xml.etree import ElementTree as ET

#query_mode:
#0:仅对比pvtype、vrid
#1:对比pvtype、vrid、标题、答案
#2:对比pvtype、vrid、标题、答案、摘要


# =========================code============================

#time_start=datetime.datetime.now()
localtime = time.localtime(time.time())
postfix=str(localtime.tm_year)+str(localtime.tm_mon)+str(localtime.tm_mday)
#print(postfix)
def send_seq(result_file, query_file, req_config, host, port, query_mode,version):
    value={
        'queryString':'刘德华的年龄',
        'forceQuery':'1',
        'queryFrom':'web'#字典中的内容随意，不影响#
    }
    words=open(query_file,'r', encoding='utf8', errors='ignore')
    i = 0
    result_obj = open(result_file, 'w+', encoding='gbk', errors='ignore')
    result_obj.write('查询词'+'\t'+ 'pvtype' +'\t'+ 'vrid' +'\t'+ '标题' +'\t' +'答案' +'\t'+'摘要')
    for word in words:
        time.sleep(0.2)
        data3 = word.encode('utf8',errors="ignore")
        data2 = data3.decode('utf8',errors="ignore")
        w_t=data2.split('\t',1)

        w_t[0]=w_t[0].strip('\n')
        w_t[1]=w_t[1].strip('\n')
        value["queryString"]=w_t[0]
          
        #url="http://cache0"+bytes(random.randint(1, 8))+".tupu.djt.ted:5555"
        url="http://"+host+":"+str(port)
        #print(url)
        data=urlhandle.urlencode(value, 'utf_16_le', 'ignore')
        #data=urllib.parse.urlencode(value)#对value进行编码，转换为标准编码#
        ua_headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-16LE",
            "Connection": "keep-alive",
        }
        data1 = str.encode(data)
        req=urllib.request.Request(url,data1,headers = ua_headers)#向url发送请求，并传送表单data#
        response=urllib.request.urlopen(req)#获取响应#
        the_page=response.read()#解析#
        the_page = the_page.decode("utf16").encode("utf8")
        #print(the_page)
        
        i_str = str(i)
        filename = i_str + '.txt'
        print(filename)
        result1_obj = open("result."+version+'/'+filename, 'wb')
        #data3 = data1.decode('utf_16_le',errors="ignore")
        #print(type(data1))
        result1_obj.write(the_page)
        result1_obj.close()
        i = i + 1
    if i % 1000 == 0:
        print(i)
    result_obj.close()



def result_diff(query_file,result_file,version,query_mode):
    value={
        'queryString':'刘德华的年龄',
        'forceQuery':'1',
        'queryFrom':'web'#字典中的内容随意，不影响#
    }
    words=open(query_file,'r', encoding='utf8', errors='ignore')
    vrid=[]
    attribute_name=[]
    answer_text_new=[]
    pvtype=[]
    desc_new=[]
    i = 0
    result_obj = open(result_file, 'w+', encoding='gbk', errors='ignore')
    result_obj.write('查询词'+'\t'+ 'pvtype' +'\t'+ 'vrid' +'\t'+ '标题' +'\t' +'答案' +'\t'+'摘要'+'\n')
    for word in words:
        #print(word)
        data3 = word.encode('utf8',errors="ignore")
        data2 = data3.decode('utf8',errors="ignore")
        w_t=data2.split('\t',1)

        w_t[0]=w_t[0].strip('\n')
        w_t[1]=w_t[1].strip('\n')
        value["queryString"]=w_t[0]
        i_str = str(i)
        filename = i_str + '.txt'
        
        with open("result."+version+'/'+filename, 'r', encoding="utf8", errors="ignore") as data_obj:
            lines = data_obj.readlines()
            #print(lines)
            for line in lines:
                #print(line.count('<doc>'))
                if line.count('<doc>') > 0:
                    kmap_left=line.split('<doc>')[1]
                    #print(kmap_left)
                    #pvtype= re.findall(r"pvtype=\"(4_33_[6,10])\"",line)
                    pvtype=re.findall(r"pvtype=\"([^_,]+_[^_,]+_[^_,])\"",kmap_left)
                    #pattern1=re.compile(p1)
                    #pvtype=pattern1.findall(line)
                    if pvtype:
                        #print(line1)
                        #print(pvtype)
                        vrid = re.findall(r'vrid="(\d+)"',kmap_left)
                        #print(vrid)
                        if  '4_33_10'  in pvtype:
                            attribute_name = re.findall(r"<attribute name=\"(\D+?)??\"",kmap_left)
                            #print(attribute_name)
                            desc = re.findall(r"<desc>.+?</desc>",kmap_left)
                            desc_new = "".join(desc).replace("\n", "")
                            #print(desc)
                            answer_text = re.findall(r"<answer text=\"(\D+?)??\"",kmap_left)
                            answer_text_new = "".join(answer_text).replace(" ", "")
                            #print(answer_text_new)
                        elif '4_33_6'  in pvtype:
                            attribute_name = re.findall(r"em=\"(\D+?)??\"",kmap_left)
                            #print(attribute_name)
                            desc = re.findall(r"<content\ fl=.+?>(\D+)</content><baikeurl>",line)
                            desc = re.findall(r"<content\ fl.+?>(.+?)</content>",kmap_left)
                            desc_new = "".join(desc).replace("\n", "")
                            #print(desc_new)
                            answer_text = re.findall(r"answer=\"(\D+?)??\"",kmap_left)
                            answer_text_new = "".join(answer_text).replace(" ", "")
                            #print(answer_text_new)
                        else:
                            #print("no pvtype")
                            attribute_name = re.findall(r"<attribute name=\"(\D+)\"\ ",kmap_left)
                            #print(attribute_name)
                            desc = re.findall(r"<desc><!\[CDATA\[(.+?)\]\]></desc>",kmap_left)
                            desc_new = "".join(desc).replace("\n", "")
                            #print(desc)
                            answer_text = re.findall(r"<answer text=\"(\D+)\"\ ",kmap_left)
                            answer_text_new = "".join(answer_text).replace(" ", "")
                            #print(answer_text_new)
                    else:
                        print("no tupu result")

        if query_mode == '0':
            result_obj.write(w_t[0] + '\t' + "".join(pvtype) +'\t' + "".join(vrid))
            result_obj.write("\n")
            pass
        elif query_mode == '1':
            result_obj.write(w_t[0] + '\t' + "".join(pvtype) +'\t' + "".join(vrid)  +'\t' + "".join(attribute_name) +'\t' + "".join(answer_text_new))
            result_obj.write("\n")
            pass
        elif query_mode == '2':
            result_obj.write(w_t[0] + '\t' + "".join(pvtype) +'\t' + "".join(vrid)  +'\t' + "".join(attribute_name) +'\t' + "".join(answer_text_new)+'\t' + "".join(desc_new))
            result_obj.write("\n")
            pass
        else:
            print("No mode")
        i = i + 1
    result_obj.close()



if __name__ == '__main__':
    argv = sys.argv[1:]
    print(argv)
    _query_file = ''
    _result_file = ''
    _req_config = {}
    _host = ''
    _port = 0
    _query_mode = 0
    _version = ''
    try:
        opts, args = getopt.getopt(argv, "", ["queryfile=", "resultfile=","result1file=", "req_config=", "host=", "port=", "mode=", "version="])
    except getopt.GetoptError:
        print('xxx')
        sys.exit(2)
    for opt, arg in opts:
        print(opt)
        if opt == "--queryfile":
            _query_file = arg
        #elif opt == "--resultfile":
        #    _result_file = arg
        elif opt == "--resultfile":
            _result_file = arg
        elif opt == "--req_config":
            config_list = arg.split('&')
            for config in config_list:
                _req_config.update({config.split('=')[0]: config.split('=')[1]})
        elif opt == "--host":
            _host = arg
        elif opt == "--port":
            _port = int(arg)
        elif opt == "--mode":
            _query_mode = arg
        elif opt == "--version":
            _version = arg
    if 'userArea' in _req_config.keys():
        _req_config['userArea'] = urlhandle.value_decode(_req_config['userArea'], 'utf8', 'ignore')
#    print(_query_file)
#    print(_result_file)
#    print(_req_config)
#    print(_host)
#    print(_port)
#    print(_query_mode)
#    print(_version)
    send_seq(query_file=_query_file,
         result_file=_result_file,
         req_config=_req_config,
         host=_host,
         port=_port,
         query_mode=_query_mode,
         version=_version,
         )
    result_diff(query_file=_query_file,result_file=_result_file,version=_version,query_mode=_query_mode)
