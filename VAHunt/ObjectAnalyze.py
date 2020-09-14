# encoding: utf-8
import os
import sys
from MethodChainBackward import MethodChainBackward

# rootPath = os.getcwd()
# filePath = os.path.join(rootPath, "APPcode\\twittre-code.txt")

class ObjectAnalyze:
    def __init__(self):
        pass

    def filterSystemMethods(self, pathlist):
        filteredpathlist = []

        for pfunc in pathlist:
            if not pfunc[0].startswith("android.support.") and not pfunc[0].startswith("com.baidu.") and not pfunc[0].startswith("com.duoku.platform.single.") \
                    and not pfunc[0].startswith("com.alibaba.") and not pfunc[0].startswith("com.idsky.android.") \
                    and not pfunc[0].startswith("com.alipay.") and not pfunc[0].startswith("com.snmi.sdk.") \
                    and not pfunc[0].startswith("com.tencent.") and not pfunc[0].startswith("com.youdao.sdk.")\
                    and not pfunc[0].startswith("cn.egame.terminal.sdk") and not pfunc[0].startswith("com.aggregationad.database.")\
                    and not pfunc[0].startswith("com.idreamsky.ad.") and not pfunc[0].startswith("com.prime31.")\
                    and not pfunc[0].startswith("com.snmi.sdk.") and not pfunc[0].startswith("com.xiaomi.")\
                    and not pfunc[0].startswith("com.yumi.android.sdk.") and not pfunc[0].startswith("com.zplay.android.sdk.")\
                    and not pfunc[0].startswith("org.xwalk.core.") and not pfunc[0].startswith("org.cocos2dx.wgelib.") \
                    and not pfunc[0].startswith("org.cocos2dx.wgelib.") and not pfunc[0].startswith("org.chromium.") \
                    and not pfunc[0].startswith("com.maxthon.mge.") and not pfunc[0].startswith("com.google.android.") :
                if pfunc not in filteredpathlist:
                    filteredpathlist.append(pfunc)

        return filteredpathlist

    def getFinalmethodinVirtualMethod(self, lines, i):
        file_reg = lines[i].split('{')[1].split('}')[0]
        path_reg = ""
        path_reg1 = ""
        path_reg2 = ""
        path_reg3 = ""
        if lines[i + 1].find("move-result-object ") >= 0:
            path_reg = lines[i + 1].split('move-result-object ')[1].replace(
                "\n", "")
            path_reg1 = path_reg + ","
            path_reg2 = path_reg + "}"
            path_reg3 = "move-result-object " + path_reg
            # print "path_reg3---------1   " + path_reg3
        # 往后追溯reg对象被用于做什么了
        k = i
        final_method = ""
        final_Class = ""
        final_method0 = []
        # 一直寻找到这个方法结束，即下一个方法前
        while (lines[k].find("    #") < 0):
            k = k + 1
            # print "path_reg"
            # print path_reg
            # print path_reg1
            # print path_reg3
            if lines[k].find("invoke-") >= 0 and lines[k].find(
                    path_reg1) >= 0 or lines[k].find("invoke-") >= 0 and lines[k].find(path_reg2) >= 0:
                # print "invoke - args reg!"
                # print lines[k]
                final_method0 = []
                final_Class = lines[k].split(" L")[1].split(';')[0].replace('/',
                                                                            '.')
                final_method = lines[k].split(";.")[1].split(':')[0]
                final_args = lines[k].split("(")[1].split(')')[0]
                final_method0.append(final_Class)
                final_method0.append(final_method)
                final_method0.append(final_args)
                if lines[k + 1].find("move-result-object") >= 0:
                    path_reg = lines[k + 1].split("move-result-object ")[
                        1].replace("\n", "")
                    # print lines[k]
                    # print "move-result-object - " + path_reg
                    path_reg1 = path_reg + ","
                    path_reg2 = path_reg + "}"
                    path_reg3 = "move-result-object " + path_reg
                    # print "path_reg3---------2   " + path_reg3
                elif lines[k + 1].find("move-result ") >= 0 and (lines[k].find(";.append:") >= 0 or lines[k].find(";.substring:") >= 0 or lines[k].find(";.toString:") >= 0):
                    path_reg = lines[k + 1].split("move-result ")[
                        1].replace("\n", "")
                    # print "move-result-object - " + path_reg
                    path_reg1 = path_reg + ","
                    path_reg2 = path_reg + "}"
                    path_reg3 = "move-result-object " + path_reg
                    # print "path_reg3---------3   " + path_reg3
            elif lines[k].find(path_reg3) >= 0 and path_reg != "":
                # print "getAbsolutePath - move-result-object reg!" + path_reg
                final_method0 = []
                # print "path_reg3---------4   " + path_reg3
                # print lines[k-1]
                final_Class = lines[k - 1].split(" L")[1].split(';')[0]
                # print final_Class
                final_method = lines[k - 1].split(";.")[1].split(':')[0]
                final_args = lines[k - 1].split("(")[1].split(')')[0]
                final_method0.append(final_Class)
                final_method0.append(final_method)
                final_method0.append(final_args)

            elif lines[k].find(path_reg + "\n") >= 0 and lines[k].find(
                    "move-object/from16") >= 0:
                path_reg = lines[k].split("move-object/from16 ")[1].split(", ")[
                    0]
                # print "move-object/from16 - " + path_reg
                path_reg1 = path_reg + ","
                path_reg2 = path_reg + "}"
                path_reg3 = "move-result-object " + path_reg
        # print "-----------" + final_method
        # print "final_method0"
        # print final_method0
        return final_method0


    # 由于Flowdroid提取出来的CFG不完整，因此自己简单的提取与KeyMethod相关的方法
    def extractSensitiveObjectComplement(self, pathlist, codePath, apkcount, txt, recordfilename):
        # 提取出每一项敏感函数的返回Object
        class_name = ""
        class_comp = ""
        VirtualMethod = ""
        list1 = []
        install = 0


        filteredpathlist = self.filterSystemMethods(pathlist)
        print "filteredpathlist"
        print filteredpathlist
        print len(filteredpathlist)

        for pfunc in filteredpathlist:
            # if pfunc[1] == "init" and pfunc[2] == "getAbsolutePath":
            # print "pfunc--------------------------"
            # print pfunc
            count = 0
            class_name = pfunc[0]
            func_name = pfunc[1]
            pfunc_name = pfunc[2]
            method_class = pfunc[3]

            with open(codePath, "rU") as sf:
                lines = sf.readlines()
                lines_length = len(lines)
                # print "lines_length = "
                # print lines_length
                i = 0

                while i <= lines_length - 3:
                    # print i
                    while lines[i].startswith("    #") and lines[i + 1].startswith(
                            "      name") and i < lines_length - 3 and install == 0:
                        VirtualMethod = lines[i + 1].split("'")[1].replace("'", "")
                        # class_line是之后回溯寄存器的定义
                        class_line = i
                        # VirtualMethodStr = "in L" + VirtualMethod.replace('.', '/') + ";"
                        if VirtualMethod == func_name:
                            # if VirtualMethod == "init":
                            #     print "****************"
                            #     print lines[i]
                            i = i + 1
                            # rtn_reg = "default"
                            while not lines[i].startswith("    #") and not lines[i + 1].startswith(
                                    "      name") and i <= lines_length - 3 and install == 0:
                                if lines[i].find(" L") >= 0 and lines[i].find("invoke-") >= 0:  # 调用其他函数
                                    invokeVirtual = lines[i].split(' L')
                                    method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                                    method_name = invokeVirtual[1].split('.')[1].split(':')[0]
                                    # if lines[i].find("(L"):
                                    #     retn_value = lines[i].split('(L')[1].split(';')[0].replace('/','.')
                                    # elif lines[i].find(")L"):
                                    #     retn_value = lines[i].split(')L')[1].split(';')[0].replace('/', '.')
                                    # and retn_value == return_value0
                                    if method_name == pfunc_name:
                                        # print "*****************"
                                        # print method_name
                                        # 敏感函数及其被调用者所在的位置
                                        # 对于跨函数的怎么操作？
                                        if pfunc_name == "getFilesDir":
                                            # print "getFilesDir----------------"
                                            file_reg = lines[i].split('{')[1].split('}')[0]
                                            # 往前追溯reg对象是什么
                                            k = i
                                            while (class_line < k):
                                                k = k - 1
                                                if lines[i].find(file_reg) >= 0:
                                                    # print "getFilesDir - reg found!"
                                                    break
                                        elif pfunc_name == "getAbsolutePath" or pfunc_name == "getExternalStorageDirectory":
                                            # print "getAbsolutePath----------------"
                                            final_method0 = self.getFinalmethodinVirtualMethod(lines, i)
                                            if final_method0[0] == "com/lody/virtual/client/core/VirtualCore" and \
                                                    final_method0[1] == "installPackage":
                                                install = 1
                                                print "install0 = 1"
                                                print pfunc
                                                break
                                            else:
                                                # 对final_method进行追溯，看它最后是否调用的是VA中的安装方法
                                                mcb = MethodChainBackward()
                                                if install == 0:
                                                    install = mcb.backward2finalInstallation(codePath,
                                                                                             final_method0)
                                                elif install == 1:
                                                    print "install1 = 1"
                                                    print pfunc
                                                    break
                                        elif pfunc_name == "getAssets":
                                            file_reg = lines[i].split('{')[1].split('}')[0]
                                            path_reg = ""
                                            path_reg1 = ""
                                            path_reg2 = ""
                                            path_reg3 = ""
                                        elif pfunc_name == "installPackage" or pfunc_name == "installApk" or pfunc_name == "installApp":
                                            # print pfunc_name
                                            file_reg = lines[i].split('{')[1].split(', ')[1].split(', ')[0]
                                            path_reg = ""
                                            file_reg1 = file_reg + ","
                                            file_reg2 = file_reg + "}"
                                            file_reg3 = "const-string " + file_reg + ", "
                                            # 往前找install的对象
                                            # const - string v0, "/data/data/ABCDEFG.apk"
                                            k = i
                                            while (class_line < k):
                                                k = k - 1
                                                # print lines[k]
                                                # if lines[k].find(file_reg1) >= 0 or lines[k].find(file_reg2) >= 0:
                                                #     # print "getFilesDir - reg found!"
                                                #     pass
                                                if lines[k].find(file_reg3) >= 0:
                                                    print pfunc[0]
                                                    if pfunc[1] != "onTransact":
                                                        # print "---------------------"
                                                        print lines[k]
                                                        apkstr = \
                                                            lines[k].split(file_reg3)[1].split("\"")[1].split("\"")[0]
                                                        install = 1
                                                        print "install2 = 1"
                                                        print pfunc
                                                        print apkstr
                                                        break
                                i = i + 1
                        i = i + 1
                    i = i + 1

        recordfile = open(recordfilename, "a+")
        recordfile.write("%d-------------------\n" % apkcount)
        recordfile.write(txt + "\n")
        recordfile.write("install = " + str(install) + "\n")
        recordfile.close()
        print "install---------" + str(install)
        return install