# encoding: utf-8
import os

# 判断Intent操作函数
class intent:
    def __init__(self):
        pass
    def IntentSubstitute(self, file_intentfunc):
        type = ""
        with open(file_intentfunc, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0

            VirtualMethod = []
            count = 0
            list0 = []
            list1 = []
            list2 = []
            satlist = []

            while i <= lines_length - 1:
                ClassNametmp = lines[i].split(" ")[0]
                VirtualMethodtmp = lines[i].split(" ")[1]
                targetIntenttmp = lines[i].split(" ")[2]
                otherOperationstmp = lines[i].split(" ")[3]
                finalIntenttmp = lines[i].split(" ")[4]
                relatedFunctmp = lines[i].split(" ")[5].replace("\n","")

                if VirtualMethodtmp not in VirtualMethod:
                    count = 0
                    Comptmp = ""
                    Typetmp = ""
                    list0 = []
                    list1 = []
                    list2 = []
                    list3 = []
                    list4 = []
                    list5 = []
                    list6 = []
                    list7 = []
                    list8 = []
                    VirtualMethod.append(VirtualMethodtmp)
                else:
                    count = count + 1

                if relatedFunctmp.find("getComponent") != -1:
                    Comptmp = finalIntenttmp
                    list0.append(ClassNametmp)
                    list0.append(VirtualMethodtmp)
                    list0.append(targetIntenttmp)
                    list0.append(otherOperationstmp)
                    list0.append(finalIntenttmp)
                    list0.append(relatedFunctmp)
                elif relatedFunctmp.find("setType") != -1:
                    Typetmp = otherOperationstmp
                    list1.append(ClassNametmp)
                    list1.append(VirtualMethodtmp)
                    list1.append(targetIntenttmp)
                    list1.append(otherOperationstmp)
                    list1.append(finalIntenttmp)
                    list1.append(relatedFunctmp)
                elif relatedFunctmp.find("setClassName") != -1:
                    list2.append(ClassNametmp)
                    list2.append(VirtualMethodtmp)
                    list2.append(targetIntenttmp)
                    list2.append(otherOperationstmp)
                    list2.append(finalIntenttmp)
                    list2.append(relatedFunctmp)
                elif relatedFunctmp.find("setComponent") != -1:
                    setComptmplist = []
                    setComptmplist.append(ClassNametmp)
                    setComptmplist.append(VirtualMethodtmp)
                    setComptmplist.append(targetIntenttmp)
                    setComptmplist.append(otherOperationstmp)
                    setComptmplist.append(finalIntenttmp)
                    setComptmplist.append(relatedFunctmp)
                    list3.append(setComptmplist)
                elif relatedFunctmp.find("putExtra") != -1:
                    putExtratmplist = []
                    putExtratmplist.append(ClassNametmp)
                    putExtratmplist.append(VirtualMethodtmp)
                    putExtratmplist.append(targetIntenttmp)
                    putExtratmplist.append(otherOperationstmp)
                    putExtratmplist.append(finalIntenttmp)
                    putExtratmplist.append(relatedFunctmp)
                    list4.append(putExtratmplist)
                elif relatedFunctmp.find("addFlags") != -1:
                    list5.append(ClassNametmp)
                    list5.append(VirtualMethodtmp)
                    list5.append(targetIntenttmp)
                    list5.append(otherOperationstmp)
                    list5.append(finalIntenttmp)
                    list5.append(relatedFunctmp)
                elif relatedFunctmp.find("access$") != -1:
                    accesstmplist = []
                    accesstmplist.append(ClassNametmp)
                    accesstmplist.append(VirtualMethodtmp)
                    accesstmplist.append(targetIntenttmp)
                    accesstmplist.append(otherOperationstmp)
                    accesstmplist.append(finalIntenttmp)
                    accesstmplist.append(relatedFunctmp)
                    list6.append(accesstmplist)
                elif relatedFunctmp.find("startActivity") != -1:
                    list7.append(ClassNametmp)
                    list7.append(VirtualMethodtmp)
                    list7.append(targetIntenttmp)
                    list7.append(otherOperationstmp)
                    list7.append(finalIntenttmp)
                    list7.append(relatedFunctmp)
                else:
                    otherstmplist = []
                    otherstmplist.append(ClassNametmp)
                    otherstmplist.append(VirtualMethodtmp)
                    otherstmplist.append(targetIntenttmp)
                    otherstmplist.append(otherOperationstmp)
                    otherstmplist.append(finalIntenttmp)
                    otherstmplist.append(relatedFunctmp)
                    list8.append(otherstmplist)

                # virtualapp
                if len(list0) != 0 and len(list1) != 0 and len(list2) != 0:
                    if (list0[4] == list1[3] and list0[1] == list1[1] and list1[1] == list2[1] and list2[2] == list1[2] and list0[2] != list1[2]):
                        print "virtualapp-------"
                        # print list0
                        # print list1
                        # print list2
                        type = "virtualapp"
                        if list2 not in satlist:
                            satlist.append(list2)
                # droidplugin
                if len(list3) == 1 and len(list4) != 0 and len(list5) != 0:
                    for extra in list4:
                        if extra[0]== list3[0][0] and extra[0]== list5[0] and extra[1]== list3[0][1] and extra[1]== list5[1] and extra[3].find(list5[3])>=0:
                            if list5[5].find("#int268435456") >=0 and extra[5].find("OldIntent\"")>=0:
                                print("droidplugin--------")
                                type = "droidplugin"
                                print list5
                                print extra
                                if list5 not in satlist:
                                    satlist.append(list5)
                                break
                i = i + 1

        return satlist,type

