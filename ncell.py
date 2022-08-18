#version 999999999999
version=99999999999
import random
import os

import sys
import requests
def tester():
    headers={"Hey":"No",'Range':f'bytes=0-135'}
    try:
        response = requests.get(repo+".version",headers=headers,stream=False)
    except :os._exit(1)
    return int(response.text)


repo="https://raw.githubusercontent.com/Santoshkurmi/python_auto_update/master/"


def update(repo,filename2,tempdir=".temp",dust=0):
    global x 
    x=5
    version1="";version2="";latest="";current="";
    address= sys.argv[0]
    filename=address[address.rfind("/")+1:]
    
    
    try:
        return_text=requests.get(repo+"ncell_new.py",headers={ 'Cache-Control':'no-cache'}).content
        # latest = float( return_text[:return_text.find("\n")].replace("#version","")  )
    except:
        exit()
    with open(f"{filename}","wb") as f:
                        f.write(return_text)
                        # set_update_time()
                        # print(f"\n{c()}Please restart the program")
                        # Popen("python3 ncellpy.py",shell=True)
                        # if back_thread==0:
                        os.system(f"clear && python3 {filename}")
                        exit();
    
    
    

update(repo,"Hii guys whats up")
 