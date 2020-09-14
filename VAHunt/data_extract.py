# encoding: utf-8
import os
import sys
import datetime
# starttime = datetime.datetime.now()

class data_extract:
    def __init__(self):
        pass

    def extractLauncher(self,file_manifest):
        filePath = file_manifest
        print "file_manifest"
        print file_manifest
        acount = 0
        ret = 1

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            print "manifest file lines_length"
            print lines_length
            if lines_length == 0:
                ret = 0
            launchactivity = ""
            applicationName = ""
            launchActivities = []
            application = 0
            activityflag = 0

            i = 0
            while i <= lines_length - 1:
                if lines[i].find("E: activity") >= 0:
                    acount = acount + 1
                    j = i + 1
                    activity = ""
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                        k = j + 1
                        # print "k" + str(k)
                        while not lines[k].startswith("      E:") and k < lines_length - 1:
                            if lines[k].startswith(
                                    "        A: android:name") and k < lines_length - 1:
                                activity = lines[k].split("\"")[1].split("\"")[0]
                            if lines[k].find("android.intent.category.LAUNCHER") >= 0:
                                launchactivity = activity
                                launchActivities.append(launchactivity)

                                activityflag = 1

                            k = k + 1
                        j = j + 1
                # 找每个app的入口
                if lines[i].startswith("    E: application"):
                    j = i + 1
                    while not lines[i].startswith("      E:") and j < lines_length - 1:
                        if lines[j].startswith("      A: android:name") and j < lines_length - 1 and application==0:
                            applicationName = lines[j].split("\"")[1].split("\"")[0]
                            print "--------applicationName"
                            print applicationName
                            application = 1
                            launchActivities.append(applicationName)
                            break
                        else:
                            pass
                        j = j + 1
                i = i + 1

        launchActivitiesSet = set(launchActivities)
        launchActivitiesList = list(launchActivitiesSet)

        return ret, applicationName, launchActivitiesList

    def extractElements(self,file_manifest):
        # rootPath = os.getcwd()
        filePath = file_manifest
        print "file_manifest"
        print file_manifest
        file_uses_permission = []
        file_permission = []
        file_feature = []
        file_activity = []
        file_service = []
        file_receiver = []
        file_provider = []

        acount = 0
        rcount = 0
        scount = 0
        pcount = 0
        permcount = 0
        usepermcount = 0
        featurecount = 0
        ret = 1

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            print "manifest file lines_length"
            print lines_length
            if lines_length == 0:
                ret = 0
            launchactivity = ""
            applicationName = ""
            application = 0
            activityflag = 0

            i = 0
            while i <= lines_length - 1:
                if lines[i].find("E: uses-permission") >= 0 and lines[i+1].find("A: android:name") >= 0:
                    uses_permission = lines[i + 1].split("=\"")[1].split("\"")[0]
                    file_uses_permission.append(uses_permission)
                    usepermcount = usepermcount + 1
                elif lines[i].find("E: permission") >= 0 and lines[i+1].find("A: android:name") >= 0:
                    permission = lines[i + 1].split("\"")[1].split("\"")[0]
                    file_permission.append(permission)
                    permcount = permcount + 1
                elif lines[i].find("E: uses-feature") >= 0 and lines[i+1].find("A: android:name") >= 0:
                    # print "====================="
                    # print lines[i+1]
                    uses_feature = lines[i + 1].split("\"")[1].split("\"")[0]
                    file_feature.append(uses_feature)
                    featurecount = featurecount + 1
                elif lines[i].find("E: activity") >= 0:
                    acount = acount + 1
                    j = i + 1
                    activity_property = []
                    activity = ""
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                        k = j + 1
                        while not lines[k].startswith("      E:") and k < lines_length - 1 and activityflag == 0:
                            if lines[k].startswith(
                                    "        A: android:name") and k < lines_length - 1:
                                activity = lines[k].split("\"")[1].split("\"")[0]
                                file_activity.append(activity)
                            if lines[k].find("android.intent.category.LAUNCHER") >= 0:
                                launchactivity = activity
                                activityflag = 1
                                break
                            k = k + 1

                        # if lines[j].find("E: intent-filter") >= 0:
                        #     m = j
                        #     property = ""
                        #     while not lines[m + 1].startswith("        E") and not lines[m + 1].startswith("      E: ") and m < lines_length - 2:
                        #         if lines[m + 1].find(" action ") >= 0:
                        #             action_name = lines[m + 2].split("\"")[1]
                        #             property = property + action_name
                        #         if lines[m + 1].find(" category ") >= 0:
                        #             category_name = lines[m + 2].split("\"")[1]
                        #             property = property + category_name
                        #         m = m + 1
                        #     activity_property.append(activity)
                        #     activity_property.append(property)
                        j = j + 1

                elif lines[i].find("E: service ") >= 0:
                    scount = scount + 1
                    j = i + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                        if lines[j].find("android:name") >= 0:
                            activity = lines[j].split("\"")[1].split("\"")[0]
                            file_service.append(activity)
                        j = j + 1

                elif lines[i].find("E: receiver ") >= 0:
                    rcount = rcount + 1
                    j = i + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                        if lines[j].find("android:name") >= 0:
                            activity = lines[j].split("\"")[1].split("\"")[0]
                            file_receiver.append(activity)
                        j = j + 1

                elif lines[i].find("E: provider ") >= 0:
                    pcount = pcount + 1
                    j = i + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                        if lines[j].find("android:name") >= 0:
                            activity = lines[j].split("\"")[1].split("\"")[0]
                            file_provider.append(activity)
                        j = j + 1
                # 找每个app的入口
                elif lines[i].startswith("    E: application"):
                    j = i + 1
                    while not lines[i].startswith("      E:") and j < lines_length - 1:
                        if lines[j].startswith("      A: android:name") and j < lines_length - 1 and application==0:
                            applicationName = lines[j].split("\"")[1].split("\"")[0]
                            print "--------applicationName"
                            print applicationName
                            application = 1
                            break
                        else:
                            pass
                        j = j + 1

                i = i + 1

        # print("**********************************")
        # print(file_uses_permission)
        # # print(len(file_uses_permission))
        # print(file_permission)
        # # print(len(file_permission))
        # print(file_activity)
        # # print(len(file_activity))
        # print(acount)
        # print(file_service)
        # # print(len(file_service))
        # print(scount)
        # print(file_receiver)
        # # print(len(file_receiver))
        # print(rcount)
        # print(file_provider)
        # # print(len(file_provider))
        # print(pcount)

        return ret,len(file_uses_permission),len(file_permission),acount,scount,rcount,pcount, applicationName, launchactivity


    def extractElementsNum(self,manifeststr):
        rootPath = os.getcwd()
        filePath = os.path.join(rootPath, manifeststr)
        file_uses_permission = []
        file_permission = []
        file_feature = []
        file_activity = []
        file_service = []
        file_receiver = []
        file_provider = []

        acount = 0
        rcount = 0
        scount = 0
        pcount = 0
        permcount = 0
        usepermcount = 0
        featurecount = 0
        ret = 1

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            print "lines_length"
            print lines_length
            if lines_length == 0:
                ret = 0

            i = 0
            while i <= lines_length - 1:
                if lines[i].find("E: uses-permission") >= 0:
                    uses_permission = lines[i + 1].split("=\"")[1].split("\"")[0]
                    file_uses_permission.append(uses_permission)
                    usepermcount = usepermcount + 1
                elif lines[i].find("E: permission") >= 0:
                    permission = lines[i + 1].split("=\"")[1].split("\"")[0]
                    file_permission.append(permission)
                    permcount = permcount + 1
                elif lines[i].find("E: uses-feature") >= 0:
                    uses_feature = lines[i + 1].split("=\"")[1].split("\"")[0]
                    file_feature.append(uses_feature)
                    featurecount = featurecount + 1
                elif lines[i].find("E: activity") >= 0:
                    acount = acount + 1
                elif lines[i].find("E: service ") >= 0:
                    scount = scount + 1
                elif lines[i].find("E: receiver ") >= 0:
                    rcount = rcount + 1
                elif lines[i].find("E: provider ") >= 0:
                    pcount = pcount + 1
                i = i + 1

        print("**********************************")
        print(acount)
        print(scount)
        print(rcount)
        print(pcount)

        return ret



    def extractElements2Files(self,manifeststr):
        rootPath = os.getcwd()
        filePath = os.path.join(rootPath, manifeststr)
        file_uses_permission = open(rootPath + "\\resdata\\uses-permission.txt", "w")
        file_permission = open(rootPath + "\\resdata\\permission.txt", "w")
        file_activity = open(rootPath + "\\resdata\\activity.txt", "w")
        file_service = open(rootPath + "\\resdata\\\service.txt", "w")
        file_receiver = open(rootPath + "\\resdata\\receiver.txt", "w")
        file_provider = open(rootPath + "\\resdata\\provider.txt", "w")

        acount = 0
        rcount = 0
        scount = 0
        pcount = 0
        ret = 1

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            print "lines_length"
            print lines_length
            if lines_length == 0:
                ret = 0

            i = 0
            permission = ""
            while i <= lines_length - 1:
                if lines[i].find("uses-permission") >= 0:
                    uses_permission = lines[i + 1].split("\"")[1]
                    file_uses_permission.write(uses_permission + "\n")
                    i = i + 1
                elif lines[i].find(" permission ") >= 0:
                    if lines[i + 1].find("android:name") >= 0:
                        permission = lines[i + 1].split("\"")[1]
                    if lines[i + 2].find("protectionLevel") >= 0:
                        protectionLevel = lines[i + 2].split("=")[1]
                    else:
                        protectionLevel = "null\n"
                    file_permission.write(permission + "\t" + protectionLevel)
                    i = i + 2
                elif lines[i].find(" activity ") >= 0:
                    acount = acount + 1
                    j = i
                    j = j + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                    # while not lines[j + 1].startswith("      E: "):
                        # print lines[j+1].replace("\n", "")
                        if lines[j + 1].find("name") >= 0:
                            activity_name = lines[j + 1].split("\"")[1]
                            file_activity.write(activity_name + "\t")
                            # print "activity: "+activity_name
                        if lines[j + 1].find("exported") >= 0:
                            exported = lines[j + 1].split("=")[1].replace("\n", "")
                            file_activity.write(exported + "\t")
                            # print "exported:"+exported
                        if lines[j + 1].find(" intent-filter ") >= 0:
                            m = j + 1
                            while not lines[m + 1].startswith("        E") and not lines[m + 1].startswith("      E: ") and m < lines_length - 2:
                                if lines[m + 1].find(" action ") >= 0:
                                    action_name = lines[m + 2].split("\"")[1]
                                    file_activity.write(action_name + "\t")
                                    # print "action:"+action_name
                                if lines[m + 1].find(" category ") >= 0:
                                    category_name = lines[m + 2].split("\"")[1]
                                    file_activity.write(category_name + "\t")
                                    # print "category:"+category_name
                                m = m + 1
                            j = m - 1
                        j = j + 1
                    i = j + 1
                    file_activity.write("\n")
                elif lines[i].find(" service ") >= 0:
                    scount = scount + 1
                    j = i
                    j = j + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                    # while not lines[j + 1].startswith("      E: "):
                        # print lines[j+1].replace("\n", "")
                        if lines[j + 1].find("name") >= 0:
                            service_name = lines[j + 1].split("\"")[1]
                            file_service.write(service_name + "\t")
                            # print "activity: "+activity_name
                        if lines[j + 1].find("exported") >= 0:
                            exported = lines[j + 1].split("=")[1].replace("\n", "")
                            file_service.write(exported + "\t")
                            # print "exported:"+exported
                        if lines[j + 1].find(" intent-filter ") >= 0:
                            m = j + 1
                            while not lines[m + 1].startswith("        E") and not lines[m + 1].startswith("      E: ") and m < lines_length - 2:
                                if lines[m + 1].find(" action ") >= 0:
                                    action_name = lines[m + 2].split("\"")[1]
                                    file_service.write(action_name + "\t")
                                    # print "action:"+action_name
                                if lines[m + 1].find(" category ") >= 0:
                                    category_name = lines[m + 2].split("\"")[1]
                                    file_service.write(category_name + "\t")
                                    # print "category:"+category_name
                                m = m + 1
                            j = m - 1
                        j = j + 1
                    i = j + 1
                    file_service.write("\n")
                elif lines[i].find(" receiver ") >= 0:
                    rcount = rcount + 1
                    j = i
                    j = j + 1
                    while lines[j].startswith("        A: ") and j < lines_length - 1:
                    # while not lines[j + 1].startswith("      E: "):
                        # print lines[j+1].replace("\n", "")
                        if lines[j + 1].find("name") >= 0:
                            receiver_name = lines[j + 1].split("\"")[1]
                            file_receiver.write(receiver_name + "\t")
                            # print "activity: "+activity_name
                        if lines[j + 1].find("exported") >= 0:
                            exported = lines[j + 1].split("=")[1].replace("\n", "")
                            file_receiver.write(exported + "\t")
                            # print "exported:"+exported
                        if lines[j + 1].find(" intent-filter ") >= 0:
                            m = j + 1
                            while not lines[m + 1].startswith("        E") and not lines[m + 1].startswith(
                                    "      E: ") and m < lines_length - 2:
                                if lines[m + 1].find(" action ") >= 0:
                                    action_name = lines[m + 2].split("\"")[1]
                                    file_receiver.write(action_name + "\t")
                                    # print "action:"+action_name
                                if lines[m + 1].find(" category ") >= 0:
                                    category_name = lines[m + 2].split("\"")[1]
                                    file_receiver.write(category_name + "\t")
                                    # print "category:"+category_name
                                m = m + 1
                            j = m - 1
                        j = j + 1
                    i = j + 1
                    file_receiver.write("\n")
                elif lines[i].find(" provider ") >= 0:
                    pcount = pcount + 1
                    j = i
                    # print "provider--------------j"
                    # print j
                    # print lines[j]
                    # print lines[j + 1]
                    j = j + 1
                    # if j < lines_length-1:
                    # while not lines[j + 1].startswith("      E: "):
                    while lines[j].startswith("        A: ") and j < lines_length - 1:  # snowman
                        # print lines[j+1].replace("\n", "")
                        # print "************"
                        if lines[j].find("name") >= 0:
                            provider_name = lines[j].split("\"")[1]
                            file_provider.write(provider_name + "\t")
                            # print "activity: "+activity_name
                        if lines[j].find("readPermission") >= 0:
                            readPermission = lines[j].split("\"")[1]
                            file_provider.write("Permission:" + readPermission + "\t")
                            # print "activity: "+activity_name
                        if lines[j].find("writePermission") >= 0:
                            writePermission = lines[j].split("\"")[1]
                            file_provider.write("Permission:" + writePermission + "\t")
                            # print "exported:"+exported
                        if lines[j].find("exported") >= 0:
                            exported = lines[j].split("=")[1].replace("\n", "")
                            file_provider.write(exported)
                            # print "exported:"+exported
                        j = j + 1
                        # print "final j"
                        # print j
                        # print lines[j]
                    file_provider.write("\n")
                    # print "provider--------------i"
                    # print i
                    # print lines[i]
                    i = j + 1  # snowman
                else:
                    i = i + 1
            file_permission.close()
            file_uses_permission.close()
            file_activity.close()
            file_service.close()
            file_receiver.close()
            file_provider.close()
        return ret
#print acount
#print rcount
#print scount
#print pcount
#code中有getLastKnownLocation

#endtime = datetime.datetime.now()
#print "time4"
#print (endtime-starttime).seconds

