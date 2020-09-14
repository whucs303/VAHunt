# encoding: utf-8
import os
import sys

# 被ObjectAnalyze中的数据流分析调用
# 目的是找到敏感路径函数之后如何定位apk文件对象是否最终被VA安装了
class MethodChainBackward:
    def __init__(self):
        pass

    # start_method0包含要追溯的方法所在的Class，方法名和参数类型
    def backward2finalInstallation(self, file_codetxt, start_method0):
        # print "start_method0"
        # print start_method0
        with open(file_codetxt, "rU") as sf:
            lines = sf.readlines()
            lines_length = len(lines)

            i = 0
            start_class = start_method0[0]
            start_method = start_method0[1]
            start_args = start_method0[2]
            finalmethodchain = []

            while i <= lines_length - 3:
                while lines[i].startswith("    #") and lines[i + 1].startswith("      name"):
                    # print lines[i+2]
                    VirtualMethod = lines[i + 1].split("'")[1].replace("'", "")
                    VirtualMethodClass = lines[i].split("in L")[1].split(";)")[0].replace("/",".")
                    if lines[i + 2].find("(") >= 0:
                        VirtualMethodType = lines[i + 2].split("(")[1].split(")")[0]
                    else:
                        try:
                            VirtualMethodType = lines[i + 2].split("'")[1].split("'")[0]
                        except Exception as err:
                            pass
                            # print "=============="
                            # print(lines[i + 2])

                    # print "========="
                    # print VirtualMethod
                    # print VirtualMethodClass
                    # print VirtualMethodType

                    if VirtualMethod == start_method and VirtualMethodClass == start_class and VirtualMethodType == start_args:
                        i = i + 1
                        # print "==============="
                        # 找所有的invoke语句
                        while not lines[i].startswith("    #") and not lines[i + 1].startswith("      name") and i <= lines_length - 3:
                            methodchain = []
                            if lines[i].find(" L") >= 0 and lines[i].find("invoke-") >= 0:
                                # print "invoke-" + lines[i]
                                onemethod = []
                                invokeVirtual = lines[i].split(' L')
                                method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                                method_name = invokeVirtual[1].split('.')[1].split(':')[0]
                                method_args = invokeVirtual[1].split('(')[1].split(')')[0]
                                # print "method_name"
                                # print method_name
                                if method_name != "<init>" and method_name != "exists" and method_name != "execute":
                                    onemethod.append(method_class)
                                    onemethod.append(method_name)
                                    onemethod.append(method_args)
                                    methodchain.append(onemethod)
                                elif method_name == "execute":
                                    # print "execute-----------------------"
                                    # .execute:([Ljava/lang/Object;)Landroid/os/AsyncTask;
                                    # name          : 'doInBackground'
                                    # type          : '([Ljava/lang/Void;)Ljava/lang/String;'
                                    method_name = "doInBackground"
                                    method_args = "[Ljava/lang/Void;"
                                    onemethod.append(method_class)
                                    onemethod.append(method_name)
                                    onemethod.append(method_args)
                                    methodchain.append(onemethod)
                                    # print methodchain
                                    finalmethodchain = methodchain
                            i = i + 1
                    i = i + 1
                i = i + 1
        # 继续寻找分支的函数调用链
        # print "finalmethodchain"
        # print finalmethodchain
        install = MethodChainBackward.backward2meanInstallation(self, file_codetxt, finalmethodchain)
        return install

    # mean_methodchain包含要追溯的方法所在的Class，方法名和参数类型
    def backward2meanInstallation(self, file_codetxt, mean_methodchain):
        with open(file_codetxt, "rU") as sf:
            lines = sf.readlines()
            lines_length = len(lines)
            i = 0
            install = 0
            final_method = ""
            for start_method0 in mean_methodchain:
                # print "==================================="
                if start_method0[0] != "com.lody.virtual.client.core.VirtualCore" and start_method0[1] != "installPackage" or start_method0[0] != "com.lody.virtual.client.core.VirtualCore" and start_method0[1] != "installApp":
                    start_class = start_method0[0]
                    start_method = start_method0[1]
                    start_args = start_method0[2]
                    final_method = ""
                    # install = 0
                    finalmethodchain = []
                    # print "start_method0"
                    # print start_method0

                    while i <= lines_length - 3 and install == 0:
                        while lines[i].startswith("    #") and lines[i + 1].startswith("      name") and install == 0:
                            VirtualMethod = lines[i + 1].split("'")[1].replace("'", "")
                            VirtualMethodClass = lines[i].split("in L")[1].split(";)")[0].replace("/", ".")
                            if lines[i + 2].find("(") >= 0:
                                VirtualMethodType = lines[i + 2].split("(")[1].split(")")[0]
                            else:
                                VirtualMethodType = lines[i + 2].split("'")[1].split("'")[0]
                            # VirtualMethodType = lines[i + 2].split("(")[1].split(")")[0]
                            if VirtualMethod == start_method and VirtualMethodClass == start_class and VirtualMethodType == start_args:
                                # print "start_method - i"
                                # print i
                                i = i + 1
                                # 找所有的invoke语句
                                while not lines[i].startswith("    #") and not lines[i + 1].startswith(
                                        "      name") and install == 0:
                                    methodchain = []
                                    if lines[i].find(" L") >= 0 and lines[i].find("invoke-") >= 0:
                                        # print lines[i]
                                        onemethod = []
                                        invokeVirtual = lines[i].split(' L')
                                        method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                                        method_name = invokeVirtual[1].split('.')[1].split(':')[0]
                                        method_args = invokeVirtual[1].split('(')[1].split(')')[0]
                                        onemethod.append(method_class)
                                        onemethod.append(method_name)
                                        onemethod.append(method_args)
                                        methodchain.append(onemethod)
                                        finalmethodchain = methodchain
                                        # print "onemethod"
                                        # print onemethod
                                        if method_class == "com.lody.virtual.client.core.VirtualCore" and method_name == "installPackage" or method_class == "com.lody.virtual.client.core.VirtualCore" and method_name == "installApp":
                                            install = 1
                                            print "install = 1"
                                            break
                                    i = i + 1
                            i = i + 1
                        i = i + 1
                    if install == 0:
                        install = self.backward2meanInstallation(file_codetxt, finalmethodchain)
                        if install == 1:
                            return install
                else:
                    install = 1
                    # print "install ====== 1"
        # print "meanInstall"
        # print install
        return install
