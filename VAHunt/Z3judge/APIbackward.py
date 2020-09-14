# encoding: utf-8
# from z3 import *
import os
import re
from intent import intent
import datetime

class APIbackward:
    def __init__(self):
        pass
    # 确定最终的stub Activity是否是空的，并决定final是否=1
    def IntentTraceback(self,file_intentfunc, file_codetxt, recordfilename):
        # starttime = datetime.datetime.now()
        ch = intent()
        print "file_intentfunc"
        print file_intentfunc
        print "file_codetxt"
        print file_codetxt
        satlist,type = ch.IntentSubstitute(file_intentfunc)
        print "satlist and type"
        print satlist
        print type
        recordfile = open(recordfilename, "a+")

        # satlist不为空
        if len(satlist) and type == "virtualapp":
            with open(file_codetxt, "rU") as sf:
                lines = sf.readlines()
                lines_length = len(lines)
                k = 0
                chain_func = ""
                chain = []
                VirtualMethodNum = ""
                StubActivity = ""
                VirtualMethod0 = satlist[0][0].replace(".", "/")
                VirtualMethod = "(in L" + VirtualMethod0
                method = satlist[0][1]
                func_name = satlist[0][5].replace("\n", "")
                func = func_name.split(",")
                print "func"
                print func

                for i in func:
                    # print "i"
                    print i
                    final = 0
                    direct = 0
                    flag = 0

                    if i.find(";") != -1:
                        print "i"
                        print i
                        # 获得setClassName的所有参数相关的函数funt及其所属包名pkg
                        pkg = i.split(";")[0].replace(".", "/")
                        rtn = ""
                        tmp = ""
                        ccq = ""
                        j = 0
                        funct = i.split(";")[1]
                        printcount = 0
                        # print "final"
                        # print final
                        # print "direct"
                        # print direct

                        while final == 0 and funct != "toString":
                            k = 0
                            print "pkg"
                            print pkg
                            printcount =printcount +1
                            if printcount > 100:
                                return 0
                            print "funct"
                            print funct
                            content = ""
                            while k <= lines_length - 1:
                                if direct == 0 and lines[k].find("      name          : '") != -1 and lines[
                                    k - 1].find(pkg) != -1 and lines[k+3].find("      name          : '")== -1:
                                    accfunct = lines[k].split("      name          : '")[1].split("'")[0]
                                    if accfunct == funct:
                                        print "k"
                                        print k
                                        VirtualMethodNum = lines[k]

                                        # 直到找到下一个method
                                        while lines[k].find("    #") == -1:
                                            k = k + 1
                                        # print k
                                        # 开始回溯该函数的返回值的变量名rtn及其对应的函数或值
                                        j = k
                                        while lines[j] != VirtualMethodNum and j <= lines_length - 3:
                                            j = j - 1
                                            if lines[j].find("return-object") != -1 and j <= lines_length - 3:
                                                rtn = lines[j].split("return-object ")[1]
                                                tmp = "move-result-object " + rtn
                                            if lines[j].find(tmp) != -1 and lines[j - 1].find(".") != -1 and j <= lines_length - 3:
                                                # chain还未结束
                                                funct = lines[j - 1].split(".")[1].split(":")[0]
                                                pkg = lines[j - 1].split(", L")[1].split(".")[0].replace(";", "")
                                                print "func and pkg"
                                                print funct + "...1" + pkg
                                                break
                                            elif lines[j].find("move-result-object ") != -1 and lines[j - 1].find(
                                                    "invoke") != -1 and j <= lines_length - 3:
                                                funct = lines[j - 1].split(".")[1].split(":")[0]
                                                pkg = lines[j - 1].split(", L")[1].split(".")[0]
                                                print "func and pkg"
                                                print funct + "...2" + pkg
                                                break
                                            elif lines[j].find("iget-object") != -1 and lines[j].find(".") != -1 and j <= lines_length - 3:
                                                # chain已经结束
                                                funct = lines[j].split(".")[1].split(":")[0]
                                                pkg = lines[j].split(", L")[1].split(".")[0]
                                                print "func and pkg"
                                                print funct + "...3" + pkg
                                                break
                                            elif lines[j].find("sget-object") != -1 and lines[j].find(".") != -1 and j <= lines_length - 3 and lines[j - 1].find(".") != -1:
                                                # 遇到非函数
                                                direct = 1
                                                # print "================"
                                                # print lines[j - 1]
                                                funct = lines[j - 1].split(".")[1].split(":")[0]
                                                pkg = lines[j - 1].split(", L")[1].split(".")[0]
                                                print "func and pkg"
                                                print funct + "...4" + pkg
                                                break
                                            elif lines[j].find("sget-object") != -1 and lines[j].find(".") != -1 and j <= lines_length - 3 and lines[j - 1].find(".") < 0:
                                                funct = lines[j].split(".")[1].split(":")[0]
                                                pkg = lines[j].split(", L")[1].split(".")[0]
                                                print "func and pkg"
                                                print funct + "...5" + pkg
                                                break
                                            elif lines[j + 1].find("    #") != -1 and lines[j - 3].find("    #") != -1 and j <= lines_length - 3:
                                                print "final = 1"
                                                final = 1
                                                break
                                elif direct == 1:
                                    i = 0
                                    while k <= lines_length - 1:
                                        # 找到sget-object的目标class和method
                                        while lines[i].find("Direct methods    -") != -1 and lines[i + 1].find(
                                                pkg) != -1:
                                            i = i + 1
                                            print "direct methods...."
                                            if lines[i].find(funct) != -1 and lines[i].find("sput-object") != -1:
                                                ccq = lines[i].split("sput-object ")[1].split(",")[0]
                                                break
                                        while flag == 0:
                                            i = i - 1
                                            # print "flag = 0"
                                            if lines[i].find(ccq) != -1 and lines[i].find("const-class") != -1:
                                                pkg = lines[i].split(", L")[1].split(";")[0]
                                                direct = 0
                                                break
                                        k = k + 1
                                elif lines[k].find("'" + funct + "'") != -1 and lines[k].find("name") != -1 and lines[
                                    k + 4].find("name") != -1:
                                    print "over"
                                    print k
                                    final = 1
                                    break
                                elif funct == "format":
                                    print lines[j]
                                    print j
                                    g = j
                                    args = lines[g - 1].split("{")[1].split("}")[0]
                                    types = lines[g - 1].split("(")[1].split(")")[0]
                                    count = args.count(", ") + 1
                                    m = 1
                                    if count == 3:
                                        m = 1
                                    elif count == 2:
                                        m = 0

                                    for i in range(m, count):
                                        arg = args.split(", ")[i]
                                        type = types.split(";")[i]
                                        cont = []
                                        num = 0
                                        numstr = ""
                                        name = 0
                                        mid = ""

                                        argcount = 1
                                        # print arg
                                        # print type
                                        if type == "Ljava/lang/String":
                                            # 向上回溯该参数
                                            h = g
                                            # print g
                                            while lines[h].find("const-string") == -1 or lines[h].find(arg) == -1:
                                                h = h - 1
                                            # pattern = re.compile('"(.*)"')
                                            # content = pattern.findall(lines[h])
                                            content = lines[h].split("\"")[1].split("\"")[0]
                                            argcount = content.count("%")
                                            print "content"
                                            print content
                                            print argcount
                                        elif type.find("Ljava/lang/Object") != -1:
                                            h = g
                                            while lines[h].find("aput-object") == -1 and lines[h].find(arg) == -1:
                                                h = h - 1
                                            print lines[h-1]
                                            h = h - 1
                                            mid0 = lines[h].split("aput-object ")[1].split(",")[0]
                                            mid = "move-result-object " + mid0
                                            print mid
                                            print h

                                            while lines[h].find(mid) == -1:
                                                h = h - 1
                                            if lines[h - 1].split(")")[1].find("Ljava/lang/Integer") != -1:
                                                num = 1
                                                # print "num == 1"

                                            while lines[h].find("sget-object") == -1:
                                                h = h - 1

                                            # print lines[h]
                                            funct = lines[h].split(".")[1].split(":")[0]
                                            pkg = lines[h].split(", L")[1].split(";")[0]
                                            # print funct

                                            if num == 1:
                                                print "content......"
                                                print content
                                                numstr = '%d' % num
                                                StubActivity = content.replace("%d", numstr).replace("%s", funct)
                                                print "StubActivity"
                                                print StubActivity

                                    # final = 1
                                    break

                                k = k + 1
                        print "final"
                        print final
                        if final == 1:
                            recordfile.write("final = 1 " + type + "\n")
                            break
        elif type == "replugin" or type == "droidplugin":
            print "type"
            print type
            recordfile.write("final = 1 " + type + "\n")
            return 1
        else:
            # satlist是空的
            return 2

        recordfile.close()
        return 1

        # solv = Solver()

        # endtime = datetime.datetime.now()
        # print "time3"
        # print (endtime-starttime).seconds
