# encoding: utf-8
import os
import time
from KeyMethod import KeyMethod
from ObjectAnalyzenew import ObjectAnalyzenew
from MethodChainBackward import MethodChainBackward
from UIAnalyzer import UIAnalyzer
from Config import Config

class ExtractCFGnew:
    def __init__(self):
        pass

    def checkInvoked(self, file_codetxt,class_name_pre):
        class_name_new = class_name_pre.replace(".","/")
        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0

            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    i = i + 1
                while lines[i].startswith("    #") & lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    classline = i
                    i = i + 1
                # new-instance v0, Lio/virtualapp/home/adapters/CloneAppListAdapter
                while (lines[i].find("new-instance") >= 0):
                    if lines[i].find("L"+class_name_new) >= 0 and VirtualMethod == "onViewCreated":
                        # print "new-instance-------"
                        # print lines[i]
                        return 1
                    i = i + 1
                i = i + 1
        return 0

    def checkXMLname(self, apk, xmlnum):
        # 在manifest文件中通过xmlnum寻找xmlname
        xmlname = "default"
        apkname = apk.split(".zip")[0]
        manifestfile = apkname + ".zip-manifest.txt"
        file_manifesttxt = Config.MANIFEST_PATH + manifestfile

        with open(file_manifesttxt, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)

            i = 0
            while i <= lines_length - 1:
                if lines[i].find(xmlnum) >= 0 and lines[i].find(":") >= 0:
                    xmlname = lines[i].split(":")[1].split(":")[0]
                    if xmlname.find("layout/")>=0:
                        xmlname = xmlname.split("layout/")[1]
                    return xmlname
                i = i + 1
        return xmlname

    def checkXMLitems(self, apkpath, apk, xmlnum):
        # 查看xml中的Item
        image = 0
        textview = 0
        rootPath = os.getcwd()
        xmlname = self.checkXMLname(apk, xmlnum)
        print "xmlname"
        print xmlname
        # aapt dump xmlstrings 725.apk res/layout/item_clone_app.xml
        if xmlname != "default":
            apkfile = apkpath + apk
            xmlfile = "res/layout/" + xmlname + ".xml"
            xmlconstruct = rootPath + "\\resdata\\" + xmlname + ".txt"
            command = "aapt.exe dump xmlstrings " + apkfile + " " + xmlfile + " > " + xmlconstruct
            print "command"
            print command
            result = os.popen(command)
            time.sleep(0.5)
            if os.path.exists(xmlconstruct):
                print "提取XML文件内容成功！"
            else:
                print "提取XML文件失败！"
                return 0, 0

            with open(xmlconstruct, "r") as f:
                lines = f.readlines()
                lines_length = len(lines)
                print "length"
                print lines_length

                i = 0
                while i <= lines_length - 1:
                    # print lines[i]
                    if lines[i].find("ImageView") >= 0:
                        image = 1
                    if (lines[i].find("TextView") >= 0 or lines[i].find("MarqueeTextView") >= 0):
                        textview = 1

                    i = i + 1
        return image, textview
        # 查看xml中的Item中是否有ListView


    # extractPerminCode
    # 对外调用的函数
    def extractCFGinCode(self, file_codetxt, apkcount, apkpath, apk, recordfilename, applicationName, launchActivities):
        selfperm = []
        install = 0
        hide = 0
        click = 0
        show = 0
        slient = 0
        result = 0
        pkglist = 0
        imageflag = 0
        textviewflag = 0
        installnum = 0
        comp = ""
        method_class = ""

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            ret = 0
            print "code file lines_length"
            print lines_length
            if lines_length < 10:
                print "lines_length < 10, unnormal!"
                return lines_length, selfperm, ret

            i = 0
            invoked = 0
            class_count = 0
            apkentrance = 0
            pathlist = []
            method_name = ""
            class_name = ""
            class_shell = []
            VirtualMethod = ""
            oa = ObjectAnalyzenew()
            km = KeyMethod()
            sensitiveapilist = km.extractSensitivePathAPI()
            UIClasslist = []
            linkClass = ""
            linkClasslist = []
            startActivities = []

            while i <= lines_length - 3:
                # super_class = ""
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    class_count = class_count + 1
                    # if lines[i+3].find("  Superclass        :")>=0 and lines[i+3].find("'L")>=0:
                    #     super_class = lines[i+3].split("'L")[1].split(";")[0]
                    i = i + 1
                while lines[i].startswith("    #") & lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    classline = i
                    i = i + 1
                while (lines[i].find("invoke-virtual") >= 0 or lines[i].find("invoke-static") >= 0 or lines[i].find(
                        "invoke-super") >= 0) and class_name.find("com.lody.virtual")< 0 and class_name.find("android.support.")<0:
                    tmplist = []
                    if lines[i].find(" L") >= 0:
                        invokeVirtual = lines[i].split(' L')
                        if invokeVirtual[1].find(".")>=0:
                            method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                            method_name1 = invokeVirtual[1].split('.')[1]
                            method_name = method_name1.split(':')[0]
                            method_pkg = invokeVirtual[1].split(';')[0].replace('/', '.')

                        if (method_name == "installApp" or method_name == "installPackage") and method_class == "com.lody.virtual.client.core.VirtualCore":
                            rootMethod = []
                            rootMethod.append(method_class)
                            rootMethod.append(method_name)
                            firstInvokeMethod = []
                            firstInvokeMethod.append(class_name)
                            firstInvokeMethod.append(VirtualMethod)
                            # print "firstInvokeMethod============="
                            # print firstInvokeMethod
                            ui = UIAnalyzer()
                            if firstInvokeMethod[1] == "onCreate":
                                result = 1
                                print "result = 1 ---3"
                            elif firstInvokeMethod[1] == "onItemClick" or firstInvokeMethod[1] == "onClick":
                                click = 1
                            elif firstInvokeMethod[1] == "doInBackground":
                                # 先找到真正的调用者
                                firstInvokeMethod = ui.processThreadInterupt(file_codetxt, firstInvokeMethod)
                                result = ui.findMethodChain(file_codetxt, rootMethod, firstInvokeMethod,
                                                            launchActivities)
                                print "result = 1 - --5"
                            elif firstInvokeMethod[1] == "run":
                                InvokeMethod = ui.processThreadStart(file_codetxt, firstInvokeMethod)
                                print "InvokeMethod"
                                print InvokeMethod
                                if InvokeMethod != []:
                                    if InvokeMethod[1] == "onCreate":
                                        result = 1
                                        print "result = 1 ---1"
                                    elif InvokeMethod[1] == "onItemClick" or InvokeMethod[1] == "onClick":
                                        click = 1
                                    if result != 1 and click != 1:
                                        result = ui.findMethodChain(file_codetxt, rootMethod, InvokeMethod,
                                                            launchActivities)
                                        print "result = 1 ---2"
                            elif firstInvokeMethod[1] == "onRequestInstall" and firstInvokeMethod[0].find("$")>=0:
                                firstInvokeMethod[0] = firstInvokeMethod[0].replace(".","/")
                                InvokeMethod = ui.processIntussusception(file_codetxt, firstInvokeMethod)
                                if InvokeMethod != []:
                                    if InvokeMethod[1] == "onCreate":
                                        result = 1
                                        print "result = 1 ---6"
                                    elif InvokeMethod[1] == "onItemClick" or InvokeMethod[1] == "onClick":
                                        click = 1
                                    if result != 1 and click != 1:
                                        result = ui.findMethodChain(file_codetxt, rootMethod, InvokeMethod,
                                                            launchActivities)
                                        print "result = 1 ---7"
                            else:
                                result = ui.findMethodChain(file_codetxt, rootMethod, firstInvokeMethod, launchActivities)
                                print "result ---4"
                                print result
                            if result == 1:
                                print "install sliently in the begining..."
                                slient = 1
                            elif result == 2:
                                print "install with user click"
                                click = 1
                            else:
                                print "install with user click perhaps"

                        if VirtualMethod == "onCreateViewHolder" and method_name == "inflate":
                            inflate_line = i
                            inflate_regs = lines[i].split(' {')[1].split('}')[0]
                            num = inflate_regs.count(',')
                            if class_name not in UIClasslist:
                                UIClasslist.append(class_name)
                            if num == 2:
                                xmlreg = inflate_regs.split(', ')[1].split(', ')[0]
                                # 往前追溯xmlreg，找到十六进制的xml文件数字
                                while(inflate_line > classline and invoked == 0):
                                    if lines[inflate_line].find(xmlreg) >= 0 and lines[inflate_line].find("const") >= 0:
                                        if lines[inflate_line].find("// #") >= 0:
                                            xmlnum = lines[inflate_line].split("// #")[1].replace("\n","")
                                            print "xmlnum"
                                            print xmlnum
                                            # 判断是否有xml中是否有ListView
                                            imageflag, textviewflag = self.checkXMLitems(apkpath, apk, xmlnum)
                                            print "image = " + str(imageflag)
                                            print "textview = " + str(textviewflag)
                                            if imageflag == 1 and textviewflag == 1:
                                                # print "class_name ----"
                                                # print class_name
                                                invoked = self.checkInvoked(file_codetxt,class_name)
                                    inflate_line = inflate_line - 1
                        if (VirtualMethod == "onCreateView" or VirtualMethod == "onViewCreated") and method_name == "setOnItemClickListener":
                            # 判断展示的小方格Class是否在UIClasslist中
                            # invoke-virtual {v1, v2}, Lio/virtualapp/Adapter/CloneAppListAdapter;.setOnItemClickListener:(Lio/virtualapp/Adapter/CloneAppListAdapter$ItemEventListener;)V
                            linkClass = lines[i].split(";.setOnItemClickListener")[0].split(" L")[1].replace("/",".")
                            # print "linkClass = " + linkClass
                            if linkClass not in linkClasslist:
                                linkClasslist.append(linkClass)

                        if method_name == "getInstalledPackages" and method_pkg == "android.content.pm.PackageManager":
                            # 判断有没有获取安装列表
                            q = i
                            in_reg = lines[q].split("{")[1].split(", ")[0]
                            while(q >= classline):
                                if lines[q].find("move-result-object "+ in_reg) >=0:
                                    if lines[q-1].find("invoke-virtual ")>=0 and lines[q-1].find("Landroid/content/Context;.getPackageManager:()Landroid/content/pm/PackageManager;")>=0:
                                        pkglist = 1
                                        #print "pkglist ===========1"
                                q = q - 1

                        for s in sensitiveapilist:
                            #if s == "installApp":
                            if s == method_name:
                                tmplist.append(class_name)
                                tmplist.append(VirtualMethod)
                                tmplist.append(method_name)
                                tmplist.append(method_class)
                                if tmplist not in pathlist:
                                    pathlist.append(tmplist)
                                    # 此时需要往前往后追溯该敏感函数的最终动作
                                    # oa.extractSensitiveObjectComplement(tmplist, classline, filePath, apkcount, txt)
                                    pfunc_name = tmplist[2]
                                    pmethod_class = tmplist[3]
                                    j = i

                                    # 由于Flowdroid提取出来的CFG不完整，因此自己简单的提取与KeyMethod相关的方法
                                    trueres = oa.filterSystemMethods(tmplist)
                                    if trueres:
                                        # ***************************
                                        # if pfunc_name == "getFilesDir":
                                        #     # print "getFilesDir----------------"
                                        #     file_reg = lines[j].split('{')[1].split('}')[0]
                                        #     # 往前追溯reg对象是什么
                                        #     k = j
                                        #     while (classline < k):
                                        #         k = k - 1
                                        #         if lines[i].find(file_reg) >= 0:
                                        #             # print "getFilesDir - reg found!"
                                        #             break
                                        if pfunc_name == "getAbsolutePath" or pfunc_name == "getExternalStorageDirectory" and install==0:
                                            # print "getAbsolutePath----------------"
                                            final_method0 = oa.getFinalmethodinVirtualMethod(lines, i)
                                            if final_method0[0] == "com/lody/virtual/client/core/VirtualCore" and \
                                                    (final_method0[1] == "installPackage" or final_method0[1] == "installApp" or final_method0[1] == "installApk"):
                                                install = 1
                                                print "install0 = 1"
                                                print tmplist
                                                break
                                            else:
                                                # 对final_method进行追溯，看它最后是否调用的是VA中的安装方法
                                                mcb = MethodChainBackward()
                                                if install == 0:
                                                    install = mcb.backward2finalInstallation(file_codetxt,
                                                                                             final_method0)
                                                elif install == 1:
                                                    #print "install1 = 1"
                                                    #print tmplist
                                                    break
                                        # elif pfunc_name == "getAssets":
                                        #     file_reg = lines[i].split('{')[1].split('}')[0]
                                        elif pfunc_name == "setComponentEnabledSetting" and hide == 0:
                                            regs = lines[j].split('{')[1].split('}')[0]
                                            num = (len(regs) - len(regs.replace(",", "")))
                                            startActivity = ""
                                            if num == 3:
                                                comp_reg0 = regs.split(', ')[0]
                                                comp_reg1 = regs.split(', ')[1].split(', ')[0]
                                                flag_reg = regs.split(', ')[3]
                                                state_reg = regs.split(', ')[2].split(', ')[0]
                                                flag_value = 0
                                                state_value = 0
                                                # 往前找state和flag的值
                                                k = j
                                                while (classline < k):
                                                    k = k - 1
                                                    if lines[k].find(flag_reg) >= 0 and lines[k].find("const")>=0 and lines[k].find("#int ")>=0:
                                                        flag_value = lines[k].split("#int ")[1]
                                                        if flag_value.find(" // ")>=0:
                                                            flag_value = flag_value.split(" // ")[0]
                                                    elif lines[k].find(state_reg) >= 0 and lines[k].find("const")>=0 and lines[k].find("#int ")>=0:
                                                        state_value = lines[k].split("#int ")[1]
                                                        if state_value.find(" // ")>=0:
                                                            state_value = state_value.split(" // ")[0]
                                                    # 这里要判断隐藏的是否是LAUNCH ACTIVITY
                                                    if state_value == "2" and flag_value == "1":
                                                        # 这里往前回溯，寻找LAUNCH ACTIVITY
                                                        # print "state_value = 2 and flag_value = 1, " + str(j)
                                                        comp_flag = 0
                                                        p = k
                                                        while (classline < p):
                                                            p = p - 1
                                                            if lines[p].find("Landroid/content/ComponentName;.<init>")>=0 and lines[p].find("}")>=0:
                                                                comps = lines[p].split("{")[1].split("}")[0]
                                                                comp_num = comps.count(",")
                                                                if comp_num == 2:
                                                                    comp_reg = comps.split(", ")[2]
                                                                    # print "comp_reg"
                                                                    # print comp_reg
                                                                    comp_flag = 1
                                                                    p = p - 1
                                                            if comp_flag == 1 and lines[p].find("const-class " + comp_reg)>=0:
                                                                if lines[p].find(", L")>=0:
                                                                    ConstClass = lines[p].split(", L")[1].split(";")[0]
                                                                    startActivity = ConstClass.replace("/",".")
                                                                    if startActivity not in startActivities:
                                                                        startActivities.append(startActivity)
                                                                    print "startActivity"
                                                                    print startActivity
                                                                    break
                                                        for la in launchActivities:
                                                            for sa in startActivities:
                                                                if sa == la:
                                                                    print "hideIcon"
                                                                    hide = 1
                                                                    break

                                        elif (pfunc_name == "installPackage" or pfunc_name == "installApk" or pfunc_name == "installApp") and install == 0:
                                            # print pfunc_name
                                            # print "===================="
                                            # print j
                                            file_reg = lines[j].split('{')[1].split(', ')[1].split(', ')[0]
                                            path_reg = ""
                                            file_reg1 = file_reg + ","
                                            file_reg2 = file_reg + "}"
                                            file_reg3 = "const-string " + file_reg + ", "
                                            # 往前找install的对象
                                            # const - string v0, "/data/data/ABCDEFG.apk"
                                            k = j
                                            while (classline < k):
                                                k = k - 1
                                                # print lines[k]
                                                # if lines[k].find(file_reg1) >= 0 or lines[k].find(file_reg2) >= 0:
                                                #     # print "getFilesDir - reg found!"
                                                #     pass
                                                if lines[k].find(file_reg3) >= 0:
                                                    # print pathlist
                                                    if tmplist[1] != "onTransact":
                                                        # print "---------------------"
                                                        print lines[k]
                                                        apkstr = \
                                                            lines[k].split(file_reg3)[1].split("\"")[1].split("\"")[0]
                                                        install = 1
                                                        print "install2 = 1"
                                                        print tmplist
                                                        print apkstr
                                                        installnum = k
                                                        break
                    i = i + 1
                i = i + 1

            if class_count == 0:
                ret = 0
            elif len(class_shell) != 0:
                ret = 2
            else:
                ret = 1

            # print "UIClasslist & linkClasslist"
            # print UIClasslist
            # print linkClasslist
            for linkClass in linkClasslist:
                if linkClass != "" and linkClass in UIClasslist:
                    click = 1
                    break

            if invoked == 1:
                show = 1

            recordfile = open(recordfilename, "a+")
            recordfile.write("silent = " + str(slient) +"\n")
            recordfile.close()
            print "silent---------" + str(slient)

            # 从这里开始寻找UI界面的调用链
            # ui = UIAnalyzer()
            # listview, listpm = ui.findListView(file_codetxt,installnum)
            # click = ui.findClick()

        return ret
