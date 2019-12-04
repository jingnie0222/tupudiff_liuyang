import paramiko
import os
import sys
import random
import re

def getlog(srcIp,port,user,pwd,srcDir,desDir):
    files = os.listdir(desDir)
    for f in files:
        os.remove(os.path.join(desDir,f))
    paramiko.util.log_to_file("paramiko.log")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=srcIp, port=port, username=user, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    files = sftp.listdir(srcDir)
    files.sort()
    for f in files:
        #now_f = sftp.listdir(srcDir)
        sftp.get(os.path.join(srcDir,f), os.path.join(desDir,f))
    ssh.close()

def getWords(dir,query_file):
    words = open(query_file,'a+', encoding='utf8', errors='ignore')
    words_add=open('pressQuery.add','w+', encoding='utf8', errors='ignore')
    word_type={}
    #print(words.tell()) 
    words.seek(0,0) 
    for word in words:
        #print(word) 
        w_t=word.split('\t',1)
        w_t[0]=w_t[0].strip('\n')
        w_t[1]=w_t[1].strip('\n')
        word_type[w_t[0]]=w_t[1]
        #print(word_type)
    #p1=r",pvtype=[^_\"]+_[^_\"]+_[^_\"]+,"
    p1=r"(?<=,pvtype=)[^_,]+_[^_,]+_[^_,]+"
    p2=r"(?<=,queryString=)([\s\S]*?),pvtype="
    p3=r"(?<=Sogou-Observer)([\s\S]*?)"
    pattern1=re.compile(p1)
    pattern2=re.compile(p2)
    pattern3=re.compile(p3)
    files = os.listdir(dir)
    #print files
    for f in files:
        with open(os.path.join(dir,f),'r', encoding='gbk', errors='ignore') as f1:
            for line in f1:
                if pattern3.findall(line):
                    #print(line)
                    pvtype=pattern1.findall(line)
                    if pvtype:
                        query = pattern2.findall(line)
                        #print(word_type)
                        if query and query[0] not in word_type:
                            #print(query[0])
                            word_type[query[0]]=pvtype[0]
                            words.writelines(query[0]+'\t'+pvtype[0]+'\n')
                            words_add.writelines(query[0]+'\t'+pvtype[0]+'\n')
                        #print query
                        #print pvtype
            f1.close()
    words.close()
    words_add.close()


if __name__ == "__main__":
    srcIdc = ["djt","1.tc","gd","1.gd","js"]
    srcIp = "cache0"+str(random.randint(1, 8))+".tupu."+srcIdc[random.randint(0, 4)]+".ted"
#EOF
    print(srcIp)
    user = "guest"
    port = 22
    pwd = "Sogou@)!$"
    srcDir = "/search/odin/daemon/searchhub/log/history"
    desDir = "/search/odin/liuyang/tupush_diff/logs"
    #getlog(srcIp,port,user,pwd,srcDir,desDir)	
    getWords(desDir,'pressQuery.bak')	
