# encoding: utf-8
import os
import zipfile
import time
import glob
import string
import shutil
import threadpool

from data_extract import data_extract
from intent_state import intent_state
from Z3judge.APIbackward import APIbackward
from code_api import code_api
from testShell import testShell
from Config import Config


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        try:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                if file.endswith(".dex"):
                    fz.extract(file, dst_dir)
        except Exception as e:
            print('unnormal IOError：',e)
        # finally:
            # print("unzip IOError")
    else:
        print('This is not zip')

def file_name(file_dir):
    files = []
    for root, dirs, files in os.walk(file_dir):
        pass
        #print files
    return files

# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        print "file size"
        print size
        return formatSize(size)
    except Exception as err:
        print(err)

def search_file(dir,sname,classeslist):
    if sname in os.path.split(dir)[1]:
        # 检验文件名里是否包含sname
        # 打印相对路径，相对指相对于当前路径
        # print(os.path.relpath(dir))
        # 打印文件名
        # print os.path.split(dir)[1]
        classeslist.append(os.path.split(dir)[1])
    if os.path.isfile(dir):
        # 如果传入的dir直接是一个文件目录 他就没有子目录，就不用再遍历它的子目录了
        return
    for dire in os.listdir(dir):
        # 遍历子目录  这里的dire为当前文件名
        search_file(os.path.join(dir,dire),sname,classeslist)
        # join一下就变成了当前文件的绝对路径
        # 对每个子目录路劲执行同样的操作
    return classeslist

def delfile(path):
    #   read all the files under the folder
    fileNames = glob.glob(path + r'\*')
    for fileName in fileNames:
        try:
            # delete file
            os.remove(fileName)
        except:
            try:
                # delete empty folders
                os.rmdir(fileName)
            except:
                # Not empty, delete files under folders
                delfile(fileName)
                # now, folders are empty, delete it
                # os.rmdir(fileName)


# apk-manifest文件的生成
def extractManifest(recordfile, file_manifesttxt, apkfile, broken_directory, apkpath, apk):
    if not os.path.exists(file_manifesttxt):
        command = "aapt.exe l -a " + apkfile + " > " + file_manifesttxt
        print "command"
        print command
        result = os.popen(command)
        time.sleep(5)
        if os.path.exists(file_manifesttxt):
            print "提取manifest文件成功！"
        else:
            print "提取manifest文件失败！"
            # 移动文件
            if os.path.exists(apkfile):
                shutil.move(apkfile, broken_directory)
            recordfile.write("未能正确提取manifest文件——失败\n")
            return 0

        # 修改后缀名，修改.apk为.zip
        portion = os.path.splitext(apk)  # 分离文件名字和后缀
        if portion[1] == ".apk":  # 根据后缀来修改,如无后缀则空
            newname = apkpath + portion[0] + ".zip"  # 要改的新后缀
            os.rename(apkfile, newname)
            print "重命名成功！" + newname
    return 1

# apk-code文件的生成
def extractCode(recordfile, apkfile, broken_directory, dexPath, file_codetxt):
    if not os.path.exists(file_codetxt):
        unzip_file(apkfile, dexPath)
        # 处理多dex问题
        classeslist = []
        classeslist = search_file(dexPath, 'classes', classeslist)
        print classeslist
        print len(classeslist)

        if len(classeslist) > 1:
            num = 0
            for i in classeslist:
                dexname = dexPath + i
                if num == 0:
                    command0 = "dexdump.exe -d " + dexname + " > " + file_codetxt
                    result0 = os.popen(command0)
                    time.sleep(10)
                    file_size = getDocSize(file_codetxt)
                else:
                    command1 = "dexdump.exe -d " + dexname + " >> " + file_codetxt
                    result1 = os.popen(command1)
                num = num + 1
        elif len(classeslist) == 1:
            dexname = dexPath + "classes.dex"
            command2 = "dexdump.exe -d " + dexname + " > " + file_codetxt
            # command1 = "dexdump.exe -d C:\Users\lu\Desktop\DataExTract-complete-20190114\DataExTract\dex\classes.dex > C:\Users\lu\Desktop\DataExTract-complete-20190114\DataExTract\dex\lest.txt"
            result1 = os.popen(command2)

        time.sleep(3)
        if os.path.exists(file_codetxt):
            print "提取code文件成功！"
        else:
            print "提取code文件失败！"
            # 移动文件
            if os.path.exists(apkfile):
                try:
                    shutil.move(apkfile, broken_directory)
                except Exception as e:
                    print('move error!  ', e)
            recordfile.write("未能正确提取code文件——失败\n")
            return 0
    return 1



# 获取还未处理的apk列表
def read_apk_list(apkpath, apkfinishfilename):
    # apk_list = Config.read_file(apkfilename)
    apk_list = file_name(apkpath)
    print(len(apk_list))
    # print "******************************"
    # print apk_list[0:10]
    finish_apk_list = Config.read_file(apkfinishfilename)
    #print(len(finish_apk_list))
    print(len(set(finish_apk_list)))
    #print finish_apk_list[:10]
    for x in range(len(finish_apk_list)):
        finish_apk_list[x] = (finish_apk_list[x].replace('\n', ''))
    # print finish_apk_list[0:10]
    wait_apk_list = []
    for apk in apk_list:
        if apk not in finish_apk_list:
            wait_apk_list.append(apk)
    # wait_apk_list = list(set(apk_list) ^ set(finish_apk_list))
    print "============="
    print(len(wait_apk_list))
    return wait_apk_list

def startVADetect(apkpath, recordfilename, apkfinishfilename):
    rootPath = os.getcwd()
    # apklist = file_name(apkpath)
    print "apkpath"
    print apkpath
    apklist = read_apk_list(apkpath, apkfinishfilename)
    # print "apklist"
    # print apklist[0:20]
    count = 0
    broken_directory = Config.BROKEN_PATH

    for apk in apklist:
        count = count + 1
        print "count"
        print count
        finishrecordfile = open(apkfinishfilename, "a+")
        apkname = apk.split(".zip")[0]   # apk名，不带后缀
        # apk = apk.split("\n")[0]
        apkfile = apkpath + apk
        manifestfile = apkname + ".zip-manifest.txt"
        codefile = apkname + "-code.txt"
        intentfuncfile = apkname + "-intentfunc.txt"
        file_codetxt = Config.CODE_PATH + codefile
        file_manifesttxt = Config.MANIFEST_PATH + manifestfile
        file_intentfunc = rootPath + "\\resdata\\" + intentfuncfile
        dexPath = rootPath + "\\dex\\"
        recordfile = open(recordfilename, "a+")
        recordfile.write(apkname + "\n")
        recordfile.close()
        recordfile = open(recordfilename, "a+")

        # 生成apk-manifest文件
        mflag = extractManifest(recordfile, file_manifesttxt, apkfile, broken_directory, apkpath, apk)
        if mflag == 0:
            # 移动文件
            finishrecordfile.write(apk + "\n")
            if os.path.exists(apkfile):
                shutil.move(apkfile, broken_directory)
            continue
        # 生成apk-code文件
        print "=========="
        print apkfile
        print dexPath
        print file_codetxt
        cflag = extractCode(recordfile, apkfile, broken_directory, dexPath, file_codetxt)
        if cflag == 0:
            # 移动文件
            finishrecordfile.write(apk + "\n")
            if os.path.exists(apkfile):
                shutil.move(apkfile, broken_directory)
            continue


        # intent相关的寄存器获取
        ins = intent_state()
        ins.IntentRegister(file_intentfunc, file_codetxt)

        # 检测组件代理 ###### 单独入口
        # z3中的APIbackward
        ab = APIbackward()
        res = ab.IntentTraceback(file_intentfunc, file_codetxt, recordfilename)
        if res == 0:
            print "失败——循环"
            recordfile.write("失败——循环\n")
        elif res == 2:
            print "无VA引擎"
            recordfile.write("无VA引擎\n")

        delfile(dexPath)
        finishrecordfile.write(apk + "\n")
        finishrecordfile.close()
        recordfile.close()



if __name__ == '__main__':
    start = time.time()
    rootPath = os.getcwd()
    APKpath = rootPath + "\\APKs\\"
    recordfilename1 = rootPath + Config.RESULT_RECORD_FILENAME
    apkfinishfilename1 = rootPath + Config.VA_FINISH_SUBNAME1
    filePath1 = [APKpath, recordfilename1, apkfinishfilename1]
    # par_list = [(filePath1, None), (filePath2, None)]
    par_list = [(filePath1, None)]
    pool = threadpool.ThreadPool(32)
    requests = threadpool.makeRequests(startVADetect, par_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    end = time.time()
    print "running time"
    print (str(end - start))

