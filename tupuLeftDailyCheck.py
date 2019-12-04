# -*- coding:utf-8 -*-

import urllib2
import urllib
import re
import datetime
import random
import time
import smtplib
import email
from email.mime.text import MIMEText
from email.header import Header

time_start=datetime.datetime.now()
postfix=bytes(time_start.year)+bytes(time_start.month)+bytes(time_start.day)
def sendReq(queryString):
        value={
                'queryString':'刘德华的年龄',
                'forceQuery':'1',
                'queryFrom':'web'#字典中的内容随意，不影响#
        }
        words=open(queryString,'r')
	word_type={}
	old_pvtype_num={}
	new_pvtype_num={}
	for word in words:
                #data3 = word.decode('gbk',errors="ignore")
                #print(data3)
		w_t=word.split('\t',1)
		w_t[0]=w_t[0].strip('\n')
		w_t[1]=w_t[1].strip('\n')
		word_type[w_t[0]]=w_t[1]
		#print(word_type)
		if w_t[1] in old_pvtype_num.keys():
			old_pvtype_num[w_t[1]] += 1
			new_pvtype_num[w_t[1]] += 1
		else:
			old_pvtype_num[w_t[1]] = 1
			new_pvtype_num[w_t[1]] = 1
	#new_pvtype_num = old_pvtype_num
	#print old_pvtype_num.keys()
	#print new_pvtype_num.keys()
	noTupuLeft=open("noTupuLeft"+'_'+postfix,'w+')
	diffPvtype=open("diffPvtype"+'_'+postfix,'w+')
	numOfPvtype=open("numOfPvtype"+'_'+postfix,'w+')
	diffPvtype.writelines("query".ljust(30)+'\t'+"ori_pvtype".ljust(10)+'\t'+"now_pvtype".ljust(10)+'\r\n')
        numOfPvtype.writelines("pvtype".ljust(20)+'\t'+"ori_num".ljust(10)+'\t'+"now_num".ljust(10)+'\r\n')
        #p1=r"pvtype=\"[^_\"]+_[^_\"]+_[^\"]+\""
        p1=r"(?<=pvtype=\")[^_\"]+_[^_\"]+_[^\"]+"
        pattern=re.compile(p1)
        #time=datetime.datetime.now()
        #print word_type.keys()
        for line in word_type.keys():
                #print word_type[line].strip('\n')
                #url="http://cache0"+bytes(random.randint(1, 8))+".tupu.djt.ted:5555"
                url="http://10.134.30.37:5555"
                #print url
                value["queryString"]=line
                data=urllib.urlencode(value)#对value进行编码，转换为标准编码#
                req=urllib2.Request(url,data)#向url发送请求，并传送表单data#
                response=urllib2.urlopen(req)#获取响应#
                the_page=response.read()#解析#
                the_page = the_page.decode("utf16").encode("gb18030")
                #print the_page
		status=pattern.findall(the_page)
                #print line
		print status
		if status:
                        now_pvtype=status[0].decode("gbk").encode("gb18030")
			#now_pvtype=now_pvtype+'\n'
			#print now_pvtype
			ori_pvtype=word_type[line]
			if now_pvtype != ori_pvtype:
				new_pvtype_num[ori_pvtype] -= 1
				if now_pvtype in new_pvtype_num.keys():
					#print "In"
					new_pvtype_num[now_pvtype] +=1
				else:
					#print "NotIn"
					new_pvtype_num[now_pvtype] =1
				diffPvtype.writelines(line.ljust(30)+'\t'+ori_pvtype.ljust(10)+'\t'+now_pvtype.ljust(10)+'\r\n')
                else:
			new_pvtype_num[word_type[line]] -= 1
                        noTupuLeft.writelines(line.ljust(30)+'\t'+word_type[line].ljust(10)+'\r\n')
                time.sleep(0.1)
                #print line
	for key in new_pvtype_num.keys():
		if new_pvtype_num[key]>=0:
			new_num=str(new_pvtype_num[key])
		else:
			new_num='0'
		if key in old_pvtype_num.keys() and old_pvtype_num[key] >=0:
			numOfPvtype.writelines(key.strip().ljust(20)+'\t'+str(old_pvtype_num[key]).ljust(10)+'\t'+new_num.ljust(10)+'\r\n')
		else :
			numOfPvtype.writelines(key.ljust(20)+'\t'+'0'.ljust(10)+'\t'+new_num.ljust(10)+'\r\n')
        
	#print new_pvtype_num
	words.close()
        noTupuLeft.close()
	diffPvtype.close()
	numOfPvtype.close()

def sendMail(_user,_pwd,_to):
	msg = email.MIMEMultipart.MIMEMultipart()
	body = MIMEText("未出图谱左侧结果的query见附件noTupuLeft"+'<br>'+"pvtype有变化的query见附件diffPvtype"+'<br>'+"pvtype个数变化见附件numOfPvtype", 'HTML', 'gbk')#邮件内容
	msg['Subject'] = "图谱左侧结果检测"#邮件的标题
	#msg['Subject'] = sub
	msg['From'] = _user
	msg['To'] = ','.join(_to)
	msg.attach(body)
	#添加附件
	att=MIMEText(open("noTupuLeft"+'_'+postfix,"rb").read(),"base64","utf-8")#打开附件地址
	att["Content-Type"] = "application/octet-stream"
	att["Content-Disposition"] ='attachment; filename="noTupuLeft"'
	att2=MIMEText(open("diffPvtype"+'_'+postfix,"rb").read(),"base64","utf-8")#打开附件地址
        att2["Content-Type"] = "application/octet-stream"
        att2["Content-Disposition"] ='attachment; filename="diffPvtype"'
	att3=MIMEText(open("numOfPvtype"+'_'+postfix,"rb").read(),"base64","utf-8")#打开附件地址
        att3["Content-Type"] = "application/octet-stream"
        att3["Content-Disposition"] ='attachment; filename="numOfPvtype"'
	msg.attach(att)
	msg.attach(att2)
	msg.attach(att3)
	#发送邮件
	s = smtplib.SMTP()
	s.connect("mail.sogou-inc.com")
	s.login(_user,_pwd)  # 登录邮箱的账户和密码
	s.sendmail(_user,_to, msg.as_string())#发送邮件
	s.quit()
	


if __name__ == "__main__":
	_usr="qa_svnreader@sogou-inc.com"
	_pwd="New$oGou4U!"
	#_to=['liuwei213289@sogou-inc.com','malu@sogou-inc.com','yinjingjing@sogou-inc.com']
	_to=['liuyangsi2810@sogou-inc.com']
	queryString="pressQuery"
	sendReq(queryString)
	#sendMail(_usr,_pwd,_to)
