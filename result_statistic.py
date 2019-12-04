import sys
import getopt
import pymysql  
import types  
import mydifflib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

#只有线上版本测试版本都出图谱时才对比标题等字段

def get_result(online_result,test_result,query_file,desc_file,add_file,diff_file):
    #result_on=open(online_result,'r', encoding='gbk', errors='ignore')
    #result_test=open(test_result,'r', encoding='gbk', errors='ignore')
    #words=open(query_file,'r', encoding='utf8', errors='ignore')
    word_type={}
    same_line = 0
    desc_line = 0
    add_line = 0
    diff_line = 0
    title_diff_num = 0
    answer_diff_num = 0
    desc_diff_num = 0
    pvtype_num = 0
    vrid_num  = 0
    num = 0
    online_list = [0 for x in range(0,6)]
    test_list = []
    j = 0
    list1 = []
    list2 = []
    tab = ['query:','pvtype:','vrid:','title:','answer:','abstract:']
    file01=open(online_result,'r', encoding='gbk', errors='ignore')
    for line in file01:
        num = num + 1
    num = num-1
    result_desc_obj = open(desc_file, 'w+', encoding='utf8', errors='ignore')
    result_add_obj = open(add_file, 'w+', encoding='utf8', errors='ignore')
    result_diff_obj = open(diff_file, 'w+', encoding='utf8', errors='ignore')
    result_desc_obj.write('<html><head><meta http-equiv="Content-Type"content="text/html; charset=utf-8" /></head><body><table border=1><tr><th>查询词</th></tr><indent>测试版本减少的图谱结果:') #使用write写入字符串内容到file.html
    result_add_obj.write('<html><head><meta http-equiv="Content-Type"content="text/html; charset=utf-8" /></head><body><table border=1><tr><th>查询词</th></tr><indent>测试版本增加的图谱结果:') #使用write写入字符串内容到file.html
    with open(online_result, 'r', encoding='gbk', errors='ignore') as x , open(test_result, 'r', encoding='gbk', errors='ignore') as y:
        line1 = x.readlines()
        line2 = y.readlines()
        for i in range(num):
            va1 = line1[i].rstrip()
            #print(va1)
            va2 = line2[i].rstrip()
            #print(va2)
            if va1 == va2:
                same_line += 1
                #print("本行相同")
            else:
                online_list = va1.split("\t")
                test_list = va2.split("\t")
                if len(online_list) > len(test_list):
                    desc_line += 1
                    list1 = va1.split()
                    #result_desc_obj.write('<tr><td>{}'+str(1)+'</td><td>{}'+str(2)+'</td></tr>') #使用write写入字符串内容到file.html
                    result_desc_obj.write('<tr><td>'+list1[0]+'</td></tr>') #使用write写入字符串内容到file.html

                    #result_desc_obj.write(message)
                    #result_desc_obj.write("\n")
                elif len(online_list) < len(test_list):
                    add_line += 1
                    list2 = va2.split()
                    #print(list2[0])
                    #result_add_obj.write(list2[0])
                    result_add_obj.write('<tr><td>'+list2[0]+'</td></tr>') #使用write写入字符串内容到file.html
                    #result_add_obj.write("\n")
                elif len(online_list) < 6:
                    for k in range(0,len(online_list)):
                        online_list[k] = tab[k] + online_list[k]
                        
                else:
                    diff = mydifflib.HtmlDiff(wrapcolumn=100)
                    diff_result = []
                    online_list[0] = tab[0] + online_list[0]
                    online_list[1] = tab[1] + online_list[1]
                    online_list[2] = tab[2] + online_list[2]
                    online_list[3] = tab[3] + online_list[3]
                    online_list[4] = tab[4] + online_list[4]
                    online_list[5] = tab[5] + online_list[5]
                    test_list[0] = 'query:' + test_list[0]
                    test_list[1] = 'pvtype:' + test_list[1]
                    test_list[2] = 'vrid:' + test_list[2]
                    test_list[3] = 'title:' + test_list[3]
                    test_list[4] = 'answer:' + test_list[4]
                    test_list[5] = 'abstract:' + test_list[5]

                    diff_data = diff.make_file(online_list,test_list).replace('nowrap="nowrap"', '')
                    
                    result_diff_obj.write(diff_data)
                    #print(diff_data)
                    for j in range(len(test_list)):
                        if online_list[j] == test_list[j]:
                           j += 1
                        else:
                            if j == 1:
                                pvtype_num += 1
                                vrid_num += 1
                                break
                            elif j == 3:
                                title_diff_num += 1
                            elif j == 4:
                                answer_diff_num += 1
                            else:
                                desc_diff_num += 1
                #var = str(i + 1)
                #print("第" + var + "行不同。")
        result_desc_obj.write('</indent></table></body></html>') #使用write写入字符串内容到file.html
        result_add_obj.write('</indent></table></body></html>') #使用write写入字符串内容到file.html
        
        line_diff_ratio=round((num-same_line)/num*100,1)
        desc_ratio=round(desc_line/num*100,1)
        add_ratio=round(add_line/num*100,1)
        diff_ratio=round(line_diff_ratio-desc_ratio-add_ratio,1)
        diff_pvtype_ratio=round(pvtype_num/num*100,1)
        diff_title_ratio=round(title_diff_num/num*100,1)
        diff_answer_ratio=round(answer_diff_num/num*100,1)
        diff_desc_ratio=round(desc_diff_num/num*100,1)
        print("总词数为：%d" % num)
        print("不一致行数比例为：{:.1f}%" .format(line_diff_ratio))
        print("测试版本减少图谱比例为：{:.1f}%" .format(desc_ratio))
        print("测试版本新增图谱比例为：{:.1f}%" .format(add_ratio))
        print("测试版本与线上版本图谱结果不同的比例为：{:.1f}%" .format(diff_ratio))
        print("其中pvtype不同所占比例为：{:.1f}%" .format(diff_pvtype_ratio))
        print("    title不同所占比例为：{:.1f}%" .format(diff_title_ratio))
        print("    answer不同所占比例为：{:.1f}%" .format(diff_answer_ratio))
        print("    desc不同所占比例为：{:.1f}%" .format(diff_desc_ratio))
    return [num,line_diff_ratio,(num-same_line),desc_ratio,desc_line,add_ratio,add_line,diff_ratio,round(diff_ratio*num/100),diff_pvtype_ratio,pvtype_num,diff_title_ratio,title_diff_num,diff_answer_ratio,answer_diff_num,diff_desc_ratio,desc_diff_num]
    result_desc_obj.close()
    result_add_obj.close()
    diff_file_obj.close()


def spilt_diff_result(diff_file,today):
    result_obj=open(diff_file,'r', encoding='utf8', errors='ignore')
    line_num=0
    i=0
    line_num_new=[]
    for line in result_obj:
        line_num=line_num+1
        if '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"' in line:
            i=i+1
            if i%300 ==0:
                line_num_new.append(line_num)
    result_obj.close()
    line_num_new.append(line_num)
    #print(line_num_new)
    left=0
    right=line_num_new[0]
    result_obj=open(diff_file,'r', encoding='utf8', errors='ignore')
    for q in range(0,len(line_num_new)):
        with open('diff'+today+'/'+'newfile'+str(q)+'.html','w', encoding='utf8', errors='ignore') as f1:
            for k in range(left,right):
                f1.writelines(result_obj.readline())
                left=int(line_num_new[q])
                if q<len(line_num_new)-1:
                    right=int(line_num_new[q+1])
        f1.close()
    result_obj.close()
    with open('diff_new'+today+'.html','w', encoding='utf8', errors='ignore') as f2:
        f2.writelines('<html><head><meta http-equiv="Content-Type"content="text/html; charset=utf-8" /></head><body><h1><a style="font-size:16px;" href="')
        for k in range(0,len(line_num_new)):
            f2.writelines('http://10.143.45.197/'+today+'/diff'+today+'/'+'newfile'+str(k)+'.html')
            f2.writelines('">http://10.143.45.197/newfile'+str(k)+'.html')
            f2.writelines('</a></h1><h1><a style="font-size:16px;" href="')
    f2.close()
        
    

def write_mysql(results,version,desc_file,add_file,today):
    db=pymysql.connect("10.143.45.197","root","Sogou","tupu");  
      
    cursor=db.cursor()  
      
    #print(version)
    #创建user表  
    cursor.execute("drop table if exists tupu_statistic")  
    sql="""CREATE TABLE IF NOT EXISTS `tupu_statistic` ( 
          `id` int(11) NOT NULL AUTO_INCREMENT, 
          `version` varchar(255) NOT NULL, 
          `time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          `total_num` int(11) NOT NULL,
          `line_diff_ratio` varchar(11) NOT NULL,
          `desc_ratio` varchar(11) NOT NULL,
          `add_ratio`  varchar(11) NOT NULL,
          `diff_ratio` varchar(11) NOT NULL,
          `diff_pvtype_ratio` varchar(11) NOT NULL,
          `diff_title_ratio` varchar(11) NOT NULL,
          `diff_answer_ratio` varchar(11) NOT NULL,
          `diff_desc_ratio` varchar(11) NOT NULL,
          `desc_file_dir` varchar(100) NOT NULL,
          `add_file_dir` varchar(100) NOT NULL,
          `diff_file_dir` varchar(100) NOT NULL,
          PRIMARY KEY (`id`) 
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""  
      
    cursor.execute(sql)  
      
    #print(num)
    #for j in range(len(results)):
    #try:
    #user插入数据  
    str3 = 'http://10.143.45.197/' + today +'/diff_new' + today + '.html'
    str4 = 'http://10.143.45.197/' + today + '/' + desc_file
    str5 = 'http://10.143.45.197/' + today + '/' +add_file
    print(str3)
    results.append(version)
    results.append(str4)
    results.append(str5)
    results.append(str3)
    #print(len(results))
    sql = "INSERT INTO tupu_statistic(total_num,line_diff_ratio,desc_ratio,add_ratio,diff_ratio,"\
       "diff_pvtype_ratio,diff_title_ratio,diff_answer_ratio,diff_desc_ratio,version,desc_file_dir,add_file_dir,diff_file_dir) VALUES ("
    for i in range(len(results)):
        #print(sql[:-1])
        sql = sql + "'" + str(results[i]) + "',"
    sql = sql[:-1] + ")"
    #print(sql)
    sql = sql.encode('utf-8')

      
    try:  
       # 执行sql语句  
       cursor.execute(sql)  
       # 提交到数据库执行  
       db.commit()  
    except:  
       # 如果发生错误则回滚  
       db.rollback() 


def sendMail(_user,_pwd,_to,results,version,desc_file,add_file,today):
        msg = MIMEMultipart('related')
        x = ''
        str2 = '<th>' + version + '</th>'
        result_new=[]
        #for x in results:    
        #    str2 = str2 + '<th>' + str(x) + '</th>'
        #print(str2)
        for x in range(0,len(results)):
            if x ==0:
                result_new.append(results[0])
            else:
                if x%2 ==0:
                    result_new.append(str(results[x]) + '个/' + str(results[x-1]))
        for x in range(0,len(result_new)):
            str2 = str2 + '<th>' + str(result_new[x]) + '</th>'
        #print(str2)
        str3 = 'http://10.143.45.197/'+ today + '/diff_new' + today + '.html'
        str4 = 'http://10.143.45.197/' + today + '/' + desc_file
        str5 = 'http://10.143.45.197/' + today + '/' + add_file
        body = MIMEText('<table border=1><tr><th>测试版本</th><th>总词数</th><th>不一致行数比例(包括减少与新增)(%)</th><th>测试版本减少比例(%)</th><th>测试版本新增比例(%)</th><th>diff比例(%)</th><th>pvytpe不一致比例(%)</th><th>title不一致比例(%)</th><th>answer不一致比例(%)</th><th>摘要不一致比例(%)</th></tr><tr>'+ str2 +'</tr><tr><th>线上版本与测试版本diff结果(左侧为线上版本右侧为测试版本)</th><th>' + str3 + '</th></tr><tr><th>测试版本图谱结果减少的查询词</th><th>' + str4 + '</th></tr><tr><th>测试版本图谱结果增加的查询词</th><th>' + str5 + '</th></tr>', 'HTML', 'gbk')#邮件内容
        msg['Subject'] = "图谱精准问答接口效果对比"+version#邮件的标题
        #msg['Subject'] = sub
        msg['From'] = _user
        msg['To'] = ','.join(_to)
        msg.attach(body)
        #msg.attach(answer)
        #发送邮件
        s = smtplib.SMTP()
        s.connect("mail.sogou-inc.com")
        s.login(_user,_pwd)  # 登录邮箱的账户和密码
        s.sendmail(_user,_to, msg.as_string())#发送邮件
        s.quit()



if __name__ == "__main__":
    result_num=[]
    _usr="qa_svnreader@sogou-inc.com"
    _pwd="New$oGou4U!"
#        #_to=['liuwei213289@sogou-inc.com','malu@sogou-inc.com','yinjingjing@sogou-inc.com']
    _to=['liuyangsi2810@sogou-inc.com']
    argv = sys.argv[1:]
    print(argv)
    _online_result = ''
    _test_result = ''
    _query_file = ''
    _desc_file = ''
    _add_file = ''
    _diff_file = ''
    _test_version = ''
    _today=''
    result_num_new=[]
    try:
        opts, args = getopt.getopt(argv, "", ["online_result=", "test_result=","query_file=","desc_file=","add_file=","diff_file=","test_version=","today="])
    except getopt.GetoptError:
        print('xxx')
        sys.exit(2)
    for opt, arg in opts:
        print(opt)
        if opt == "--query_file":
            _query_file = arg
        #elif opt == "--resultfile":
        #    _result_file = arg
        elif opt == "--online_result":
            _online_result = arg
        elif opt == "--test_result":
            _test_result = arg
        elif opt == "--desc_file":
            _desc_file = arg
        elif opt == "--add_file":
            _add_file = arg
        elif opt == "--diff_file":
            _diff_file = arg
        elif opt == "--test_version":
            _test_version = arg
        elif opt == "--today":
            _today = arg
   #     print(_online_result)
   #     print(_test_result)
   #     print(_query_file)
    result_num = get_result(online_result=_online_result,test_result=_test_result,query_file=_query_file,desc_file=_desc_file,add_file=_add_file,diff_file=_diff_file)
    spilt_diff_result(diff_file=_diff_file,today=_today)
    sendMail(_usr,_pwd,_to,result_num,version=_test_version,desc_file=_desc_file,add_file=_add_file,today=_today)
    for i in range(0,len(result_num)):
        if i == 0:
            result_num_new.append(result_num[0])
        else:
            if i%2 ==1:
                result_num_new.append(result_num[i])
    write_mysql(result_num_new,version=_test_version,desc_file=_desc_file,add_file=_add_file,today=_today)
