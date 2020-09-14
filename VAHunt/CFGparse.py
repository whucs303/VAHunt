# encoding: utf-8
import os
import sys
from KeyMethod import KeyMethod
from ObjectAnalyze import ObjectAnalyze

rootPath = os.getcwd()
# filePath = os.path.join(rootPath, "CFG\\00ACA8659E49450D123B0F8C7BA5DAF7.txt")

class CFGparse(object):
    def __init__(self):
        pass
        # 数据结构:  class method 返回值 参数 调用了哪个method 调用的method的相关信息等8个信息
        # self.methodname = ''
        # self.classname = ''
        # self.returntype = ''
        # self.args = ''
        # self.callee = ''
        # self.calleeclass = ''
        # self.calleereturntype = ''
        # self.calleeargs = ''

    def extractAllCFGcalls(self,filePath):
        CFGcalls = []

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0

            while i <= lines_length - 1:
                methodlist = []
                # print i
                if lines[i].find("->") >= 0:
                    # 存在调用与被调用情况
                    class_name = lines[i].split('<')[1].split(': ')[0]
                    # print class_name
                    returntype = lines[i].split(': ')[1].split(' ')[0]
                    method_name = lines[i].split(': ')[1].split(' ')[1].split('(')[0]
                    args = lines[i].split('(')[1].split(')')[0]
                    callee = lines[i].split('->"')[1].split(': ')[1].split(' ')[1].split('(')[0]
                    calleeclass = lines[i].split('->"')[1].split('<')[1].split(': ')[0]
                    calleereturntype = lines[i].split('->')[1].split(': ')[1].split(' ')[0]
                    calleeargs = lines[i].split('->')[1].split('(')[1].split(')')[0]
                    methodlist.append(class_name)
                    methodlist.append(method_name)
                    methodlist.append(returntype)
                    methodlist.append(args)
                    methodlist.append(calleeclass)
                    methodlist.append(callee)
                    methodlist.append(calleereturntype)
                    methodlist.append(calleeargs)
                    CFGcalls.append(methodlist)
                elif lines[i].find("<") >= 0:
                    # 不存在调用与被调用情况
                    class_name = lines[i].split('<')[1].split(': ')[0]
                    returntype = lines[i].split(': ')[1].split(' ')[0]
                    method_name = lines[i].split(': ')[1].split(' ')[1].split('(')[0]
                    args = lines[i].split('(')[1].split(')')[0]
                    calleeclass = 'null'
                    callee = 'null'
                    calleereturntype = 'null'
                    calleeargs = 'null'
                    methodlist.append(class_name)
                    methodlist.append(method_name)
                    methodlist.append(returntype)
                    methodlist.append(args)
                    methodlist.append(calleeclass)
                    methodlist.append(callee)
                    methodlist.append(calleereturntype)
                    methodlist.append(calleeargs)
                    if methodlist not in CFGcalls:
                        CFGcalls.append(methodlist)
                i = i + 1
        return CFGcalls

    def extractSensitiveMethod(self, methodlist):
        km = KeyMethod()
        sensitiveapilist = km.extractSensitiveAPI(methodlist)
        print "sensitiveapilist"
        print sensitiveapilist
        sensitiveflowlist = []

        # 往前回溯，找到调用敏感函数的所有method及其class，判断class的component
        for s in sensitiveapilist:
            for m in methodlist:
                if s[1] == m[5]:
                    # print "--------"
                    # print m
                    sensitiveflowlist.append(m)
        # 这里返回的应该是一个很多Method的调用链
        return sensitiveflowlist

    # 循环寻找某一个sensitive API的所有调用链
    # 深度遍历
    # 没有使用该函数
    def parseCFGfromFlowDroid(self, sensitiveflowlist, methodCallList, filePath):
        sensitiveCFGlist = []
        methodinchain = []
        methodchain = []
        lifecyclelist = ['onCreate','onRestart','onStart','onPause','onStop','onResume','onDestory','onPostCreate','onPostResume','dummyMainMethod']
        recordfile = open("malResult.txt", "a+")

        for sf in sensitiveflowlist:
            flag = 0
            methodchain = []
            methodinchain.append(sf[4])
            methodinchain.append(sf[5])
            methodinchain.append(sf[6])
            methodinchain.append(sf[7])
            if methodinchain not in methodchain:
                methodchain.append(methodinchain)
            methodinchain = []
            methodinchain.append(sf[0])
            methodinchain.append(sf[1])
            methodinchain.append(sf[2])
            methodinchain.append(sf[3])
            if methodinchain not in methodchain:
                methodchain.append(methodinchain)
            # 循环找调用者作为被调用者的情况
            count = 0
            while flag == 0:
                xunhuan = 0
                for mc in methodCallList:
                    methodinchain = []
                    if sf[0] == mc[4] and sf[1] == mc[5] and sf[2] == mc[6] and sf[3] == mc[7] and xunhuan == 0:
                        # print "**********"
                        # print mc
                        # 这里存在循环调用的问题，比如a方法调用b方法，B方法又调用a方法，形成死锁
                        methodinchain.append(mc[0])
                        methodinchain.append(mc[1])
                        methodinchain.append(mc[2])
                        methodinchain.append(mc[3])
                        if methodinchain not in methodchain:
                            methodchain.append(methodinchain)
                        else:
                            count = count + 1
                            # print count
                        # print methodinchain

                        if count > 10:
                            # recordfile.write(filePath + "--xunhuan!\n")
                            # recordfile.close()
                            xunhuan = 1
                            # print "xunhuan function"
                            # return sensitiveCFGlist

                        if mc[1] not in lifecyclelist:
                            sf[0] = mc[0]
                            sf[1] = mc[1]
                            sf[2] = mc[2]
                            sf[3] = mc[3]
                        else:
                            flag = 1

            # 这里依旧有问题——同一个敏感API可能出现在不同的方法及class中
            if methodchain not in sensitiveCFGlist:
                sensitiveCFGlist.append(methodchain)

        recordfile.write(filePath + "--normal!\n")
        recordfile.close()
        return sensitiveCFGlist

# if __name__=="__main__":
#     cfgp = CFGparse()
#     filePath = rootPath + "\\CFG\\" + "00ACA8659E49450D123B0F8C7BA5DAF7.txt"
#     methodCallList = cfgp.extractAllCFGcalls(filePath)
#     sensitiveFlowList = cfgp.extractSensitiveMethod(methodCallList)
#     # filePath = os.path.join(rootPath, "CFG\\03087C55020D668EFE34C2562D8C96ED.txt")
#     sensitiveCFGList = cfgp.parseCFGfromFlowDroid(sensitiveFlowList, methodCallList, filePath)
#     print "sensitiveCFGList"
#     print sensitiveCFGList
#     print len(sensitiveCFGList)
