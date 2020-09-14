# encoding: utf-8
import os
import numpy as np
from framework_map_api import framework_map_api
from class_hieracy import class_hieracy
from KeyMethod import KeyMethod

class code_api:
    def __init__(self):
        pass

    ###############求framework和code中的权限和method的最小集合
    def overlappedMethodinManifestandCode(self, methodlistinC, methodlistinF, map1):
        set1 = set(methodlistinC)
        set2 = set(methodlistinF)
        mixset = set1 & set2
        # transform list into set to calculate the permission APIs in code
        mixlist = list(mixset)
        # mixlist is a methodName list
        mixpermlist = []
        newminpermlist = []

        for i in mixlist:
            if i in methodlistinF:
                # print "*****************"
                # print i
                # print methodlistinF.index(i)
                # print map1[methodlistinF.index(i),0]
                mixperm = map1[methodlistinF.index(i), 3]
                # print mixperm
                mixpermlist.append(mixperm)

        # code中API涉及的权限
        minpermlist = {}.fromkeys(mixpermlist).keys()

        # 但是此时，由于有些API涉及的权限不止一个，因此去重的时候比较的元素并不是单一的permission，这里需要做一下处理
        for ele in minpermlist:
            # print ele
            ele = ele.replace('\n', '')
            if ele.find(", "):
                newEle = ele.split(', ')
                for newele in newEle:
                    newminpermlist.append(newele)

        #print newminpermlist
        #print len(newminpermlist)

        finalpermlist = {}.fromkeys(newminpermlist).keys()
        # dereplication
        print "finalpermlist"
        print finalpermlist
        print len(finalpermlist)
        return finalpermlist

    ###############
    # extractpermlist
    # 将code中的method与axploer数据库中有perm的Method对应起来
    def extractpermlist(self, list1, completelist, file_list0):
        #这里的class要区分自己的class还是所属code中的class
        # print "list1"
        # print list1

        mapq = framework_map_api()
        # map0 is a nx4 array from framework, which includes method_name, return_value, method_class and method_perm
        map0 = mapq.extractMethod()
        map1 = map0.tolist()
        # transform all methodName into a List
        methodlistinF = list(map0[:, 0])
        # transform all returnValue into a List
        rtnvaluelistinF = list(map0[:, 1])
        # transform all methodClass into a List
        methodclasslistinF = list(map0[:, 2])
        # transform all methodperm into a List
        methodpermlistinF = list(map0[:, 3])
        # print "list1 前十"
        # print list1[:10]

        # list1 is a 嵌套 nx5 list from code, which includes class_name, comp, VirtualMethod, method_name and method_class
        arraytmp = np.array(list1)
        # print arraytmp
        # classarray = arraytmp[:, 0]
        # classlistinC = classarray.tolist()
        # comparray = arraytmp[:, 1]
        # complistinC = comparray.tolist()
        # virtualmethodarray = arraytmp[:, 2]
        # virtualmethodlistinC = virtualmethodarray.tolist()
        # print "arraytmp"
        # print arraytmp
        methodarray = arraytmp[:, 3]
        methodlistinC = methodarray.tolist()
        # methodclassarray = arraytmp[:, 4]
        # methodclasslistinC = methodclassarray.tolist()

        pcount = 0
        cpcount = 0      # 有组件的API数量
        apcount = 0      # 组件为Activity的API数量
        spcount = 0      # 组件为Service的API数量
        brpcount = 0     # 组件为BroadcastReceiver的API数量
        cppcount = 0     # 组件为ContentProvider的API数量
        # 为list1中的每个method_name添加method_perm，生成新的completelist，即completelist是所有有perm的item集合
        for i in list1:
            for p in map1:
                # print "i & p"
                # print i
                # print p
                if i[3] == p[0]:
                # if i[3] == p[0] and i[4] == p[2]:
                #     print "permission"
                #     print p[3]   # permission
                #     print i[4]
                #     print p[2]
                    i.append(p[3])
                    # print map1[methodlistinF.index(p),3]   #权限
                    #i.append(map1[methodlistinF.index(p), 3])
                    completelist.append(i)
                    pcount = pcount + 1
                    if i[1] != "0":
                        cpcount = cpcount + 1
                        # print "i[1]"
                        # print i[1]
                        if(i[1]=="Activity"):
                            apcount = apcount + 1
                        elif (i[1] == "Service"):
                            spcount = spcount + 1
                        elif (i[1] == "BroadcastReceiver"):
                            brpcount = brpcount + 1
                        elif (i[1] == "ContentProvider"):
                            cppcount = cppcount + 1
                    break

        file_list0.write(str(completelist))
        # print "pcount:list1 with permission number:"
        # print pcount
        # print "cpcount:list1 with component and permission number:"
        # print cpcount
        # completelist = {}.fromkeys(completelist).keys()
        count = 0
        for i in completelist:
            if i[1] != "0":
                count = count + 1
            # print i
        # print "count:list1 with component number:"
        # print count
        return map0, methodlistinC, methodlistinF, pcount, cpcount, apcount, spcount, brpcount, cppcount

    #################
    # extractPerminCode
    # 对外调用的函数
    def extractPerminCode(self, file_codetxt, applicationName, launchactivity):
        rootPath = os.getcwd()
        selfpermPath = os.path.join(rootPath, "resdata\\permission.txt")
        providerselfpermPath = os.path.join(rootPath, "resdata\\provider.txt")
        file_list0 = open(rootPath + "\\resdata\\list0.txt", "w")
        file_list1 = open(rootPath + "\\resdata\\list1.txt", "w")

        activitycomp = ['Landroid/app/Activity;', 'Landroid/support/v7/app/ActionBarActivity;', 'Landroid/support/v7/app/AppCompatActivity;','Landroid/app/AccountAuthenticatorActivity;','Landroid/app/ActivityGroup;','Landroid/app/AliasActivity;','Landroid/app/ExpandableListActivity;','Landroid/app/FragmentActivity;','Landroid/app/ListActivity;','Landroid/app/NativeActivity;','Landroid/app/ActionBarActivity;','Landroid/app/AppCompatActivity;','Landroid/app/LauncherActivity;','Landroid/app/PreferenceActivity;','Landroid/app/TabActivity;']
        servicecomp = ['Landroid/app/Service;', 'Landroid/inputmethodservice/AbstractInputMethodService;','Landroid/accessibilityservice/AccessibilityService;','Landroid/service/media/CameraPrewarmService;','Landroid/service/carrier/CarrierMessagingService;','Landroid/service/carrier/CarrierService;','Landroid/service/chooser/ChooserTargetService;','Landroid/telecom/ConnectionService;','Landroid/support/customtabs/CustomTabsService;','Landroid/service/dreams/DreamService;','Landroid/nfc/cardemulation/HostApduService;',
                       'Landroid/telecom/InCallService;','Landroid/app/IntentService;','Landroid/app/InputMethodService;','Landroid/app/job/JobService;','Landroid/service/media/MediaBrowserService;','Landroid/support/v7/media/MediaRouteProviderService;','Landroid/media/midi/MidiDeviceService;','Landroid/support/v4/app/NotificationCompatSideChannelService;','Landroid/service/notification/NotificationListenerService;','Landroid/nfc/cardemulation/OffHostApduService;','Landroid/printservice/PrintService;','Landroid/speech/RecognitionService;',
                       'Landroid/widget/RemoteViewsService;','Landroid/location/SettingInjectorService;','Landroid/service/textservice/SpellCheckerService;','Landroid/speech/tts/TextToSpeechService;','Landroid/media/tv/TvInputService;','Landroid/service/voice/VoiceInteractionService;','Landroid/service/voice/VoiceInteractionSessionService;','Landroid/net/VpnService;','Landroid/service/wallpaper/WallpaperService;']
        broadcastcomp = ['Landroid/content/BroadcastReceiver;','Landroid/appwidget/AppWidgetProvider;','Landroid/app/admin/DeviceAdminReceiver;','Landroid/service/restrictions/RestrictionsReceiver;','Landroid/support/v4/content/WakefulBroadcastReceiver;']
        contentcomp = ['Landroid/content/ContentProvider;','Landroid/provider/DocumentsProvider;','Landroid/support/v4/content/FileProvider;','Landroid/test/mock/MockContentProvider;','Landroid/content/SearchRecentSuggestionsProvider;']
        threadcomp = ['Ljava/lang/Thread;']
        asynctaskcomp = ['Landroid/os/AsyncTask;']


        selfperm = []
        providerperm = []
        comp = ""
        method_class = ""
        apkentrance = 0
        # #自定义权限
        # with open(selfpermPath, "rU") as sf:
        #     lines0 = sf.readlines()
        #     lines_length0 = len(lines0)
        #     k = 0
        #     while k <= lines_length0 - 1:
        #         if lines0[k] != "":
        #             selfperm0 = lines0[k].split("	")[0]
        #             selfperm.append(selfperm0)
        #         k = k+1
        #     # print "selfperm:"
        #     # print selfperm

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            ret = 0
            print "code file lines_length"
            print lines_length
            if lines_length < 10:
                print "lines_length < 10, unnormal!"
                return lines_length, selfperm, ret, 0, 0, 0, 0, 0, 0, 0

            i = 0
            class_count = 0
            blanklist = []
            list1 = []
            selflist = []
            completelist = []
            activitylist = []
            servicelist = []
            broadcastlist = []
            contentlist = []
            threadlist = []
            threadrunnablelist = []
            threadasynclist = []
            tmplist = []
            tmpselflist = []
            method_name = ""
            class_name = ""
            class_shell = []

            VirtualMethod = ""
            class_interface1 = ""
            class_interface = ""

            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    if class_name == "com.qihoo.util.Configuration" or class_name == "com.qihoo.util.QHDialog" or class_name == "com.qihoo.util.QhJobService":
                        class_shell.append(class_name)
                    elif class_name == "com.tencent.StubShell.TxAppEntry" or class_name == "com.tencent.bugly.legu.Bugly":
                        class_shell.append(class_name)
                    elif class_name == "com.secshell.shellwrapper.SecAppWrapper" or class_name == "com.secshell.shellwrapper.DexInstall" or class_name == "com.SecShell.SecShell.DexInstall":
                        class_shell.append(class_name)
                    elif class_name == "com.baidu.protect.StubApplication" or class_name == "com.baidu.protect.StubProvider":
                        class_shell.append(class_name)
                    elif class_name == "com.ali.mobisecenhance.StubApplication":
                        class_shell.append(class_name)
                    elif class_name == "com.example.bestart.BeStartActivity":
                        class_shell.append(class_name)
                    elif class_name == applicationName or class_name == launchactivity:
                        apkentrance = 1


                    if lines[i + 3].startswith("  Superclass") and i+ 3 <= lines_length - 3:
                        class_comp = lines[i + 3].split("'")[1]
                        if class_comp in activitycomp:
                            comp = "Activity"
                            activitylist.append(class_name)
                        elif class_comp in servicecomp:
                            comp = "Service"
                            servicelist.append(class_name)
                        elif class_comp in broadcastcomp:
                            comp = "BroadcastReceiver"
                            broadcastlist.append(class_name)
                        elif class_comp in contentcomp:
                            comp = "ContentProvider"
                            contentlist.append(class_name)
                        # elif class_comp in threadcomp:
                        #     comp = "Thread"
                        #     threadlist.append(class_name)
                        # elif class_comp == "Ljava/lang/Object;":
                        #     if lines[i+4].startswith("  Interfaces") and lines[i+5].startswith("    #"):
                        #         #print i
                        #         #print lines[i+5]
                        #         class_interface1 = lines[i + 5].split("'")[1]
                        #         class_interface = class_interface1.strip("L").replace(';', '').replace('/', '.')
                        #         if class_interface == "Ljava/lang/Runnable;":
                        #             comp = "ThreadRunnable"
                        #             threadrunnablelist.append(class_name)
                        # elif class_comp in asynctaskcomp:
                        #     comp = "AsyncTask"
                        #     threadasynclist.append(class_name)
                        else:
                            comp = "0"
                    class_count = class_count + 1
                    i = i + 1
                while lines[i].startswith("    #") & lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    # print "####"
                    # print VirtualMethod
                    i = i + 1
                while lines[i].find("invoke-virtual") >= 0 or lines[i].find("invoke-static") >= 0 or lines[i].find(
                        "invoke-super") >= 0:
                    tmplist = []
                    if lines[i].find(" L") >= 0:
                        invokeVirtual = lines[i].split(' L')
                        method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                        # print "================="
                        # print invokeVirtual[1]
                        if invokeVirtual[1].find(".")>=0:
                            method_name1 = invokeVirtual[1].split('.')[1]
                            method_name = method_name1.split(':')[0]
                            tmplist.append(class_name)
                            tmplist.append(comp)
                            tmplist.append(VirtualMethod)
                            tmplist.append(method_name)
                            tmplist.append(method_class)
                            list1.append(tmplist)
                    elif lines[i].find("[L") >= 0:
                        invokeVirtual = lines[i].split('[L')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]
                    elif lines[i].find("[B") >= 0:
                        invokeVirtual = lines[i].split('[B')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]
                    elif lines[i].find("[I") >= 0:
                        invokeVirtual = lines[i].split('[I')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]
                    i = i + 1
                while lines[i].find("const-string") >= 0:
                    # print "====================="
                    # print lines[i]
                    if lines[i].find('"')>=0:
                        str1 = lines[i].split('"')[1]
                        tmpselflist = []
                        # print str
                        for sp in selfperm:
                            if str1 == sp:
                                tmpselflist.append(class_name)
                                tmpselflist.append(comp)
                                tmpselflist.append(VirtualMethod)
                                tmpselflist.append(method_name)
                                tmpselflist.append(method_class)
                                tmpselflist.append(sp)
                                # print tmpselflist
                                selflist.append(tmpselflist)
                    i = i + 1

                i = i + 1

            print "class_shell"
            print class_shell
            if class_count == 0:
                ret = 0
            elif len(class_shell)!= 0:
                ret = 2
            else:
                ret = 1
            # print "code_api-selflist"
            # print selflist
            # print lines_length
            # print list1[0:5]

        # # provider在manifest中定义的权限
        # with open(providerselfpermPath, "rU") as pf:
        #     lines1 = pf.readlines()
        #     lines_length1 = len(lines1)
        #     print lines_length1
        #     j = 0
        #     while j <= lines_length1 - 1:
        #         if lines1[j].find("Permission:"):
        #             tmpproviderpermlist = []
        #             selfperm1 = lines1[j].split("\t")
        #             class_name = selfperm1[0]
        #             comp = "ContentProvider"
        #             VirtualMethod = "null"
        #             method_name = "null"
        #             tmpproviderpermlist.append(class_name)
        #             tmpproviderpermlist.append(comp)
        #             tmpproviderpermlist.append(VirtualMethod)
        #             tmpproviderpermlist.append(method_name)
        #             tmpproviderpermlist.append(method_class)
        #             n = len(selfperm1)
        #             #print n
        #             while n > 1:
        #                 if selfperm1[n-1].startswith("Permission:"):
        #                     sp1 = selfperm1[n-1].replace('Permission:', '')
        #                     tmpproviderpermlist.append(sp1)
        #                 n = n-1
        #             providerperm.append(tmpproviderpermlist)
        #         else:
        #             print "provider不含权限限制"
        #         j = j+1
        #     # print "providerperm........................"
        #     # print providerperm

        activitylist = {}.fromkeys(activitylist).keys()
        servicelist = {}.fromkeys(servicelist).keys()
        broadcastlist = {}.fromkeys(broadcastlist).keys()
        contentlist = {}.fromkeys(contentlist).keys()
        threadlist = {}.fromkeys(threadlist).keys()
        threadrunnablelist = {}.fromkeys(threadrunnablelist).keys()
        threadasynclist = {}.fromkeys(threadasynclist).keys()
        # print activitylist
        # print servicelist
        # print broadcastlist
        # print contentlist
        # file_list0.write(str(list1))
        # print "code_api testing..................."

        ch = class_hieracy()
        list1, activitylist, servicelist, broadcastlist, contentlist, threadlist, threadrunnablelist, threadasynclist = ch.extractComponent(list1, activitylist, servicelist, broadcastlist, contentlist, threadlist, threadrunnablelist, threadasynclist, file_codetxt)

        if list1:
            # print "length of list1"
            # print len(list1)
            for l in list1:
                if l[0] in activitylist and l[1] == "0":
                    l[1] = "Activity"
                elif l[0] in servicelist and l[1] == "0":
                    l[1] = "Service"
                elif l[0] in broadcastlist and l[1] == "0":
                    l[1] = "BroadcastReceiver"
                elif l[0] in contentlist and l[1] == "0":
                    l[1] = "ContentProvider"
                elif l[0] in threadlist and l[1] == "0":
                    l[1] = "Thread"
                elif l[0] in threadrunnablelist and l[1] == "0":
                    l[1] = "ThreadRunnable"
                elif l[0] in threadasynclist and l[1] == "0":
                    l[1] = "ThreadAsync"

            file_list1.write(str(list1))
            map1, methodlistinC, methodlistinF, pcount, cpcount, apcount, spcount, brpcount, cppcount = self.extractpermlist(
                list1, completelist, file_list0)
            finalpermlist = self.overlappedMethodinManifestandCode(methodlistinC, methodlistinF, map1)

            km = KeyMethod()
            apis = km.extractSensitiveAPI(list1)
            print "apis"
            # print apis
            # print len(apis)
            return lines_length, finalpermlist, ret, pcount, cpcount, apcount, spcount, brpcount, cppcount, apkentrance

        return lines_length, blanklist, ret, 0, 0, 0, 0, 0, 0, apkentrance


        #return lines_length, finalpermlist, ret, pcount, cpcount, apcount, spcount, brpcount, cppcount

# wechat: 36  actual 38  apply 38(53)
# lbe: 46  actual 52  apply 94(114)
    def shell(self, file_codetxt):
        selfperm = []
        apkentrance = 0

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            ret = 0
            print "code file lines_length"
            print lines_length
            if lines_length < 10:
                print "lines_length < 10, unnormal!"
                return lines_length, selfperm, ret, 0, 0, 0, 0, 0, 0

            i = 0
            class_count = 0
            class_shell = []

            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    if class_name == "com.qihoo.util.Configuration" or class_name == "com.qihoo.util.QHDialog" or class_name == "com.qihoo.util.QhJobService":
                        class_shell.append(class_name)
                    elif class_name == "com.tencent.StubShell.TxAppEntry" or class_name == "com.tencent.bugly.legu.Bugly":
                        class_shell.append(class_name)
                    elif class_name == "com.secshell.shellwrapper.SecAppWrapper" or class_name == "com.secshell.shellwrapper.DexInstall" or class_name == "com.SecShell.SecShell.DexInstall":
                        class_shell.append(class_name)
                    elif class_name == "com.baidu.protect.StubApplication" or class_name == "com.baidu.protect.StubProvider":
                        class_shell.append(class_name)
                    elif class_name == "com.ali.mobisecenhance.StubApplication":
                        class_shell.append(class_name)
                    elif class_name == "com.example.bestart.BeStartActivity" or class_name == "com.secneo.apkwrapper.DexInstall":
                        class_shell.append(class_name)
                    class_count = class_count + 1
                    i = i + 1
                i = i + 1

            print "class_count"
            print class_count
            print "class_shell"
            print class_shell
            if class_count == 0:
                ret = 0
            elif len(class_shell)!= 0:
                ret = 2
            else:
                ret = 1

        return lines_length, ret
