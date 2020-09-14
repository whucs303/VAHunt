# encoding: utf-8
import os
import zipfile
import time
import glob
import shutil
import threading
import threadpool
from CFGparse import CFGparse
from ObjectAnalyzenew import ObjectAnalyzenew
from ExtractCFGnew import ExtractCFGnew
from Config import Config
from testShell import testShell
from data_extract import data_extract

def file_name(file_dir):
    files = []
    for root, dirs, files in os.walk(file_dir):
        print files
    return files


def unzip_file(zip_src, dst_dir):
    try:
        r = zipfile.is_zipfile(zip_src)
        if r:
            try:
                fz = zipfile.ZipFile(zip_src, 'r')
                for file in fz.namelist():
                    if file.endswith(".dex"):
                        fz.extract(file, dst_dir)
            except Exception as e:
                print('unnormal IOError：', e)
            # finally:
            # print("unzip IOError")
        else:
            print('This is not zip')
    except Exception as e:
        print('unnormal IOError：', e)


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
                os.rmdir(fileName)

# apk-manifest文件的生成
def extractManifest(recordfile, file_manifesttxt, apkfile, broken_directory, apkpath, apk):
    if not os.path.exists(file_manifesttxt):
        command = "aapt.exe l -a " + apkfile + " > " + file_manifesttxt
        print "command"
        print command
        result = os.popen(command)
        time.sleep(3)
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
            result1 = os.popen(command2)

        time.sleep(3)
        if os.path.exists(file_codetxt):
            print "提取code文件成功！"
        else:
            print "提取code文件失败！"
            # 移动文件
            if os.path.exists(apkfile):
                shutil.move(apkfile, broken_directory)
            recordfile.write("未能正确提取code文件——失败\n")
            return 0
    return 1

# 获取还未处理的apk列表
def read_apk_list(apkpath, apkfinishfilename):
    # apk_list = Config.read_file(apkfilename)
    apk_list = file_name(apkpath)
    print(len(apk_list))
    finish_apk_list = Config.read_file(apkfinishfilename)
    print(len(set(finish_apk_list)))
    for x in range(len(finish_apk_list)):
        finish_apk_list[x] = (finish_apk_list[x].replace('\n', ''))
    wait_apk_list = []
    for apk in apk_list:
        if apk not in finish_apk_list:
            wait_apk_list.append(apk)
    # wait_apk_list = list(set(apk_list) ^ set(finish_apk_list))
    print "============="
    print(len(wait_apk_list))
    return wait_apk_list

def startMalDetect(apkpath, recordfilename, apkfinishfilename):
    # 检测恶意性
    rootPath = os.getcwd()
    cfgtxtlist = read_apk_list(apkpath, apkfinishfilename)
    broken_directory = Config.BROKEN_PATH
    count = 0

    for apk in cfgtxtlist:
        apkname = apk.split(".zip")[0]  # apk名，不带后缀
        apkfile = apkpath + apk
        manifestfile = apkname + ".zip-manifest.txt"
        codefile = apkname + "-code.txt"
        finishrecordfile = open(apkfinishfilename, "a+")
        file_codetxt = Config.CODE_PATH + codefile
        file_manifesttxt = Config.MANIFEST_PATH + manifestfile
        dexPath = rootPath + "\\dex\\"
        count = count + 1
        print "count------"
        print count
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
        cflag = extractCode(recordfile, apkfile, broken_directory, dexPath, file_codetxt)
        if cflag == 0:
            # 移动文件
            finishrecordfile.write(apk + "\n")
            if os.path.exists(apkfile):
                shutil.move(apkfile, broken_directory)
            continue

        # 检测加壳
        ts = testShell()
        permres = ts.detectShell(file_codetxt)
        if permres == 0:
            print "权限提取——失败"
            recordfile.write("权限提取——失败\n")
            continue
        elif permres == 2:
            print "packed apk---1"
            recordfile.write("未能提取出正常代码——packed apk——失败\n")
            continue

        # 提取apk入口
        de = data_extract()
        ret, applicationName, launchActivities = de.extractLauncher(file_manifesttxt)
        print "launchActivities"
        print launchActivities
        # 获取加载策略相关
        extractcfg = ExtractCFGnew()
        if os.path.exists(file_codetxt):
            print "There exists codefilePath " + file_codetxt
            ret = extractcfg.extractCFGinCode(file_codetxt, count, apkpath, apk, recordfilename, applicationName, launchActivities)
            if ret == 0:
                print "code file broken!"
            elif ret == 2:
                print "packed apk"
        else:
            print "There exists none code file."
            recordfile.write("code文件不存在——失败\n")

        # 删除文件
        delfile(dexPath)
        finishrecordfile.write(apk + "\n")
        finishrecordfile.close()
        recordfile.close()


if __name__=="__main__":
    start = time.time()
    # 多线程检测
    rootPath = os.getcwd()
    APKpath = rootPath + "\\APKs\\"
    recordMalname1 = rootPath + Config.RESULT_RECORD_MALNAME
    apkfinishMalname1 = rootPath + Config.MALVA_FINISH_SUBNAME1
    filePath1 = [APKpath, recordMalname1, apkfinishMalname1]
    par_list = [(filePath1, None)]
    pool = threadpool.ThreadPool(32)
    requests = threadpool.makeRequests(startMalDetect, par_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    end = time.time()
    print "运行时间"
    print (str(end-start))
