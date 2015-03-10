"""
Created on Fri Feb 02 2013

@author: PAING HEIN THU
"""
import os
import sys
import zipfile
import subprocess
import shlex
from datetime import datetime
from ftplib import FTP,error_perm
from glob import glob
from ConfigParser import SafeConfigParser
import codecs

now=datetime.now()
fil_name="%s"%now.date()

__version__='1.0'

def LogFile(Logname): #Process Log Save File
    def _wrapper(arg):
        log_text=open("log.txt","a")
        lst=str(Logname(arg))
        log_text.write(lst)
        log_text.close
        return lst
    return _wrapper

@LogFile
def save_log(val):
    return val

def file_argv(val):
    return val

def CheckDay(st_date,en_date): #process Start Check Day
    try:
        chk_date=parser_config(2,'cr_date','')
        if datetime.strptime(chk_date,'%Y-%m-%d').date()<=now.date() or parser_config(2,'ctrl','') ==0:
            if now.isoweekday()==int(st_date) or now.isoweekday()==int(en_date) and now.time().isoformat()>str(parser_config(2,'ctrl_time','')):
                return True
            return False
    except Exception,msg:
        save_log("Error msg CheckDay>>%s>>%s\n"%(datetime.now().isoformat(),msg))
        parser_config(1,'ctrl',str(0))
    
def Delete_File(_path,ext,cmd): #Check And File Delete
    try:
        for dirname,subdirs,files in os.walk(_path):
            for fil in files:
                if fil.endswith(ext):
                    command="%s %s"%cmd,os.path.join(_path,fil)
                    arg=shlex.split(command)
                    proc=subprocess.Popen(arg)
                    return True
            return True
    except Exception,msg:
        save_log("Error msg Delete_File>>%s>>%s\n"%(datetime.now().isoformat(),msg))
        parser_config(1,'ctrl',str(0))
    
def parser_config(ctrl,option,val):
    try:
        parser = SafeConfigParser()
        if ctrl==1:
            parser.read('config.ini')
            parser.set('auto_sync',option,val)
            with open('config.ini', 'w') as configfile:
                parser.write(configfile)
        if ctrl==2:
            with codecs.open('config.ini', 'r') as f:
                parser.readfp(f)
                ret_val = parser.get('auto_sync',option)
                return ret_val
    except Exception,msg:
        save_log("Error msg parser_config>>%s>>%s\n"%(datetime.now().isoformat(),msg))
        parser_config(1,'ctrl',str(0))
        
def Check_log(src_path):
    try:
        chk_date=parser_config(2,'cr_date','')
        if datetime.strptime(chk_date,'%Y-%m-%d').date()<datetime.fromtimestamp(os.path.getmtime(src_path)).date():
            return True
        else:
            return False
    except Exception,msg:
        save_log("Error msg Check_log>>%s>>%s\n"%(datetime.now().isoformat(),msg))
        parser_config(1,'ctrl',str(0))

def Create_Zip(src_path):
    zf=zipfile.ZipFile(fil_name+'.zip', mode='w')
    try:
        for dirname,subdirs,files in os.walk(src_path):
            for fil in files:
                zf.write(os.path.join(dirname,fil))
    except Exception,msg:
        save_log("Error msg Create_Zip>>%s>>%s\n"%(datetime.now().isoformat(),msg))
        parser_config(1,'ctrl',str(0))
    finally:
        zf.close()
        return True

def Upload(path,svr,usr,usr_pass):
    _ftp=FTP(svr,usr,usr_pass)
    if _ftp!=None:
        fullname="/%s.zip"%fil_name
        f=open(os.path.join(path,fil_name+".zip"),"rb")
        try:
            _ftp.storbinary("STOR "+fullname,f,8*1024)
            f.close()
            save_log("Date:%s\n" % now.date())
            parser_config(1,'cr_date',str(now.date()))
            parser_config(1,'ctrl',str(1))
        except error_perm,msg:
         save_log("Error msg upload>>%s>>%s\n"%(datetime.now().isoformat(),msg))
         parser_config(1,'ctrl',str(0))
          
def main():

    st_date = parser_config(2,'st_date','')
    en_date = parser_config(2,'en_date','')
    path = str(parser_config(2,'path',''))
    ext = str(parser_config(2,'ext',''))
    src_path = str(parser_config(2,'src_path',''))
    svrname = str(parser_config(2,'svr_name',''))
    usrname = str(parser_config(2,'usrname',''))
    svr_pass = str(parser_config(2,'pass',''))
    cmd = str(parser_config(2,'cmd',''))
    
    if CheckDay(st_date,en_date):
        if Delete_File(path,ext,cmd):
            if Check_log(src_path):
                if Create_Zip(src_path):
                    Upload(path,svrname,usrname,svr_pass)
                    
if __name__ == '__main__':
    main()
        
    
    