# encoding: utf-8
import os
import datetime

class intent_state:
    def __init__(self):
        pass
    # 向intentfunc文件中写与intent相关的操作
    def IntentRegister(self,file_intentfunc, file_codetxt):
        intentfunc = open(file_intentfunc, "w")

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            # snowman这里i应该是1
            i = 0
            new_intent = []
            param_intent = []
            new_intent0 = ""
            class_count = 0
            writelist = []
            param1 = []
            intent = []
            paramlist = []
            paramlists = []
            class_name = ""
            VirtualMethod = ""
            VirtualMethodNum = ""
            item = ""
            var = "null"
            res = "null"
            intentcount = 0

            while i <= lines_length - 3:
                func_name = []
                vmflag = 0
                newintentinVirtualMethod = []

                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    class_count = class_count + 1
                    i = i + 1
                while lines[i].startswith("    #") and lines[i + 1].startswith("      name"):
                    vmflag = i  # 回溯的终点
                    # print "vmflag"
                    # print vmflag
                    VirtualMethod = lines[i + 1].split("'")[1]
                    paramlist = []
                    paramlists = []
                    newintentinVirtualMethod = []
                    intentcount = 0
                    i = i + 1
                # 第一种情况：函数中新创建的intent
                # 以VirtualMethod为模块，记录其中的new-instance和对应的行号
                # vmflag = i   # 回溯的终点
                # print "vmflag"
                # print vmflag
                # while not lines[i].startswith("    #") and not lines[i + 1].startswith("      name") and i <= lines_length - 3:
                #     if lines[i].find("new-instance") >= 0 and lines[i].find("Landroid/content/Intent") >= 0:
                #         new_intent0 = lines[i].split("new-instance ")[1].split(",")[0]
                #         new_intent = []
                #         # new_intent中存放的是一个VirtualMethod中所有新创建的intent regs和其行号，如[[v1,100],[v5,123]]
                #         new_intent.append(new_intent0)          # new intent reg
                #         new_intent.append(i)                    # row number
                #         newintentinVirtualMethod.append(new_intent)
                #         # func_name = []
                #         intentcount = intentcount + 1
                #     i = i + 1

                while lines[i].find("new-instance") >= 0 and lines[i].find("Landroid/content/Intent") >= 0 and i <= lines_length - 3\
                        or lines[i].find("check-cast") >= 0 and lines[i].find("Landroid/content/Intent") >= 0 and i <= lines_length - 3 \
                        or lines[i].find("invoke-virtual") >= 0 and lines[i].find(":(") >= 0:
                    if lines[i].find("new-instance") >= 0 :
                        new_intent0 = lines[i].split("new-instance ")[1].split(",")[0]
                        new_intent = []
                        # new_intent中存放的是一个VirtualMethod中所有新创建的intent regs和其行号，如[[v1,100],[v5,123]]
                        new_intent.append(new_intent0)  # new intent reg
                        new_intent.append(i)  # row number
                        newintentinVirtualMethod.append(new_intent)
                        # func_name = []
                        intentcount = intentcount + 1
                        i = i + 1
                    elif lines[i].find("check-cast") >= 0 :
                        new_intent0 = lines[i].split("check-cast ")[1].split(",")[0]
                        new_intent = []
                        # new_intent中存放的是一个VirtualMethod中所有新创建的intent regs和其行号，如[[v1,100],[v5,123]]
                        new_intent.append(new_intent0)  # new intent reg
                        new_intent.append(i)  # row number
                        newintentinVirtualMethod.append(new_intent)
                        # func_name = []
                        intentcount = intentcount + 1
                        i = i + 1
                    elif lines[i].find("invoke-virtual") >= 0 and lines[i].find(":(") >= 0:
                        params = lines[i].split(":(")[1].split(")")[0]
                        if params.find("Landroid/content/Intent") >= 0:
                            params_type = params.split("Landroid/content/Intent")[0]
                            semicount = params_type.count(';')
                            if lines[i].find("{")>=0 and lines[i].find("}")>=0:
                                params_var = lines[i].split("{")[1].split("}")[0]
                                param_intent = params_var.split(", ")[semicount+1]
                                new_intent = []
                                new_intent.append(param_intent)  # new intent reg
                                new_intent.append(i)  # row number
                                flag = 0
                                for ni in newintentinVirtualMethod:
                                    if param_intent == ni[0]:
                                        flag = 1
                                if flag == 0:
                                    newintentinVirtualMethod.append(new_intent)
                                    intentcount = intentcount + 1
                        i = i + 1

                if newintentinVirtualMethod:       # 该VirtualMethod中有new intent
                    # print "newintentinVirtualMethod"
                    # print newintentinVirtualMethod
                    for niv in newintentinVirtualMethod:
                        ni = niv[0]        # ni是intent的reg
                        j = niv[1]         # rownumber
                        # new_inetnt后面跟“，”或者“}”来区分出v1与v12这样的例子
                        ni1 = ni + ","
                        ni2 = ni + "}"
                        # paramlist.append(ni)  # 把new intent放在第一位
                        var = "null"
                        res = "null"
                        # 对于每个new intent，在该VirtualMethod模块中，从创建它的那一行开始遍历，寻找相关的regs
                        while not lines[j].startswith("    #") and not lines[j + 1].startswith(
                                "      name") and j <= lines_length - 4:
                            while lines[j].find(ni1) >= 0 and lines[j].find("invoke-") >= 0 or lines[j].find(
                                    ni2) >= 0 and lines[j].find("invoke-") >= 0:
                                paramlist = []
                                func_name = []
                                # 与该Intent相关的functions
                                func_name_tmp = lines[j].split(".")[1].split(":")[0]
                                # print "func_name_tmp"
                                # print func_name_tmp
                                if func_name_tmp not in func_name:
                                    func_name.append(func_name_tmp)

                                param = lines[j].split("{")[1].split("}")[0]  # param是涉及intent的函数的其他regs
                                paramlen = 0
                                if param.find(",") >= 0:  # 该函数的参数中含有其他函数或者变量
                                    paramlen = len(param.split(","))
                                for p in range(0, paramlen):
                                    # paramlist存放的是与该intent的寄存器相关的其他变量名regs，如[v1,v4,v11]和[v5,v7]
                                    ip = param.split(",")[p].replace(" ", "")
                                    if ip not in paramlist and ip != ni:
                                        paramlist.append(ip)
                                    # if ni in paramlist:
                                    #     paramlist.remove(ni)
                                var = "null"
                                res = "null"

                                # print "paramlist..............."
                                # print paramlist
                                if func_name_tmp == "getComponent":
                                    # 则找到下一句的move-result-object
                                    # print "***************getComponent"
                                    if lines[j + 1].find("move-result-object ") >= 0:
                                        var_tmp = lines[j + 1].split("move-result-object ")[1]
                                        res = var_tmp.replace("\n", "")
                                        # print "getComponent return value"
                                        # print res
                                #if func_name_tmp == "putExtra":
                                    # print "***************addFlags"
                                elif func_name_tmp != "<init>":
                                    # print "func_name_tmp"
                                    # print func_name_tmp
                                    # elif func_name_tmp == "putExtra":
                                    # 回溯前几行代码来查看另外几个参数对应的函数是什么
                                    # print "paramlist"
                                    # print paramlist
                                    var = ','.join(paramlist)

                                    for pp in paramlist:
                                        # print "pp"
                                        # print pp
                                        pp1 = pp + ","
                                        pp2 = pp + "}"
                                        if lines[j].find(pp1) >= 0 or lines[j].find(pp2) >= 0:
                                            q = j-1
                                            # print lines[j]
                                            # print lines[q]
                                            # while lines[q] != VirtualMethodNum:
                                            while q > vmflag:
                                                if lines[q].find("move-result-object " + pp) >= 0:
                                                    # print "move-result-object " + pp
                                                    if lines[q - 1].find(".") >= 0:
                                                        func_tmp = lines[q - 1].split(".")[1]
                                                        func_tmp1 = func_tmp.split(":")[0]
                                                        class_tmp = lines[q - 1].split(".")[0]
                                                        if class_tmp.find(", L") >= 0:
                                                            class_tmp1 = class_tmp.split(", L")[1].replace("/", ".")
                                                        else:
                                                            if class_tmp.find(", [")>=0:
                                                                class_tmp1 = class_tmp.split(", [")[1]
                                                        # print class_tmp1 + func_tmp1
                                                        if func_name_tmp == "setType":
                                                            var_tmp = lines[q - 1].split("{")[1]
                                                            var = var_tmp.split("}")[0].replace(" ", "")
                                                            # print "var"
                                                            # print var
                                                        if class_tmp1 + func_tmp1 not in func_name:
                                                            # print "*******"
                                                            # print func_tmp1
                                                            if func_tmp1 != "getString" and func_tmp1 != "toString" and func_tmp1 != "append":
                                                                # print "================"
                                                                # print func_tmp1
                                                                func_name.append(class_tmp1 + func_tmp1)
                                                                # print "func_name"
                                                                break
                                                elif lines[q].find("const") >= 0 and lines[q].find(
                                                        pp + ",") >= 0 and q < j:
                                                    # print q
                                                    value = lines[q].split(pp + ", ")[1]
                                                    # print "value = " + value
                                                    if lines[q].find("//") >= 0:
                                                        value = value.split(" //")[0].replace(" ", "")
                                                        # if func_name != "append":
                                                        func_name.append(value)
                                                        break
                                                q = q - 1
                                j = j + 1

                                if func_name and func_name_tmp != "<init>" and func_name_tmp != "append" and func_name_tmp != "toString":
                                    # print "VirtualMethod2"
                                    # print VirtualMethod
                                    # print "class_name"
                                    # print class_name
                                    # print "========="
                                    # print func_name
                                    item = class_name + " " + VirtualMethod + " " + ni + " " + var + " " + res

                                    sep = ','
                                    writecontent = item + " " + sep.join(func_name) + "\n"
                                    if writecontent not in writelist:
                                        writelist.append(writecontent)
                                        intentfunc.write(writecontent)
                                        # print(writecontent)
                            j = j + 1

                        if paramlist and paramlist not in paramlists:
                            # paramlists存放的是所有的paramlist，如[[v1,v4,v11],[v5,v7]]
                            paramlists.append(paramlist)
                        # print "paramlists========================"
                        # print paramlists

                i = i + 1
                # print i
                # print lines[i]