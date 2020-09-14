# encoding: utf-8
import os
from code_api import code_api
from perm_group import perm_group
import sys
import datetime

class compare_perm:
    def __init__(self):
        pass

    def comparePermissions(self,codefile):
        sys.path.append('G:\\python2.7\\Lib\site-packages')
        # starttime = datetime.datetime.now()
        # recordfile = open("record.txt", "a+")
        # recordfile.write("permissions-----------------------------")

        rootPath = os.getcwd()
        filePath = os.path.join(rootPath, "resdata\\uses-permission.txt")
        # 提取manifest中的系统API
        manifestPermList = []

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0

            while i <= lines_length - 1:
                lines[i] = lines[i].replace('\n', '')
                if lines[i].startswith("android.permission."):
                    manifestPermList.append(lines[i])
                i = i + 1

        # print manifestPermList
        print "number of manifestperm"
        print len(manifestPermList)

        codePerm = code_api()
        lines_length, codePermList, res, pcount, cpcount, apcount, spcount, brpcount, cppcount = codePerm.extractPerminCode(codefile)
        if lines_length < 10:
            print "compare_perm, code file lines < 10"
            return 0
        if res == 2:
            print "packed apk"
            return 2

        # codePermSet = set(codePermList)
        # manifestPermSet = set(manifestPermList)
        # mixset = codePermSet & manifestPermSet
        # print "***********"
        # print "the intersection of codePermSet and manifestPermSet"
        # print mixset
        # print len(mixset)
        # # recordfile.write("\nthe intersection of codePermSet and manifestPermSet")
        # # recordfile.write(str(mixset))
        #
        # ##################compare in permission group
        # manifestPermGroupList = []
        # codePermGroupList = []
        # PermGroupList1 = []
        # PermGroupList2 = []
        #
        # p = perm_group()
        # pp = p.definePermGroup()
        # # pp is a list
        #
        # for i in codePermList:
        #     for pg in pp:
        #         for p in pg:
        #             if i == p:
        #                 # print i
        #                 # print p
        #                 # print pp.index(pg)
        #                 PermGroupList1.append(pp.index(pg))
        #                 codePermGroupList.append(i)
        #             # else:
        #             #     codePermGroupList.append(i)
        # mincodePermGroupList = {}.fromkeys(codePermGroupList).keys()
        # print "mincodePermGroupList"
        # print mincodePermGroupList
        # print len(mincodePermGroupList)
        #
        # for j in manifestPermList:
        #     for pg in pp:
        #         for p in pg:
        #             if j == p:
        #                 # print pp.index(pg)
        #                 PermGroupList2.append(pp.index(pg))
        #                 manifestPermGroupList.append(j)
        #             # else:
        #             #     manifestPermGroupList.append(j)
        # minmanifestPermGroupList = {}.fromkeys(manifestPermGroupList).keys()
        # print "minmanifestPermGroupList"
        # print minmanifestPermGroupList
        # print len(minmanifestPermGroupList)
        #
        # # print "PermGroupList1"
        # # print PermGroupList1
        # # print "PermGroupList2"
        # # print PermGroupList2
        #
        # mincodePermGroupSet = set(mincodePermGroupList)
        # minmanifestPermGroupSet = set(minmanifestPermGroupList)
        # mixGroupSet = mincodePermGroupSet & minmanifestPermGroupSet
        # print "mixGroupSet"
        # print mixGroupSet
        # print len(mixGroupSet)
        # # recordfile.write("\nthe intersection of codePermGroupSet and manifestPermGroupSet")
        # # recordfile.write(str(mixGroupSet))
        # # recordfile.write(str(len(mixGroupSet)))
        #
        # mixGroupList = list(mixGroupSet)

        # long running
        # endtime = datetime.datetime.now()
        # print "time1"
        # print (endtime-starttime).seconds
        if len(manifestPermList) == 0 and len(codePermList) == 0 :
            return 0
        else:
            return 1


