import os
import numpy as np

class class_hieracy:
    def __init__(self):
        pass
    def extractComponent(self, list1, activitylist, servicelist, broadcastlist, contentlist, threadlist, threadrunnablelist, threadasynclist, file_codetxt):

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            # print "lines_length"
            # print lines_length
            count = 1
            class_count = 0
            n = 0

            compareactivitylist = activitylist
            compareservicelist = servicelist
            comparebroadcastlist = broadcastlist
            comparecontentlist = contentlist
            comparethreadlist = threadlist
            comparethreadrunnablelist = threadrunnablelist
            comparethreadasynclist = threadasynclist

            while count > 0:
                i = 0
                n = n + 1
                count = 0
                newactivitylist = []
                newservicelist = []
                newbroadcastlist = []
                newcontentlist = []
                newthreadlist = []
                newthreadrunnablelist = []
                newthreadasynclist = []

                while i <= lines_length - 3:
                    while lines[i].startswith("Class #"):
                        class_count = class_count + 1
                        class_name1 = lines[i + 1].split("'")[1]
                        class_name = class_name1.strip("L").replace(';', '').replace('/', '.')  #io.virtualapp.home.oadingActivity
                        class_name_unformat = class_name1.replace('L', '')

                        if lines[i + 3].startswith("  Superclass"):
                            class_comp1 = lines[i + 3].split("'")[1]
                            class_comp = class_comp1.strip("L").strip(";").replace('/', '.')
                            comp = "0"
                            for c in compareactivitylist:
                                if class_comp == c:
                                    comp = "Activity"
                                    if class_name not in activitylist:
                                        newactivitylist.append(class_name)
                                        count = count + 1
                            for s in compareservicelist:
                                if s == class_comp:
                                    comp = "Service"
                                    if class_name not in servicelist:
                                        newservicelist.append(class_name)
                                        count = count + 1
                            for b in comparebroadcastlist:
                                if b == class_comp:
                                    comp = "BroadcastReceiver"
                                    if class_name not in broadcastlist:
                                        newbroadcastlist.append(class_name)
                                        count = count + 1
                            for con in comparecontentlist:
                                if con == class_comp:
                                    comp = "ContentProvider"
                                    if class_name not in contentlist:
                                        newcontentlist.append(class_name)
                                        count = count + 1
                            for t in comparethreadlist:
                                if t == class_comp:
                                    comp = "Thread"
                                    if class_name not in threadlist:
                                        newthreadlist.append(class_name)
                                        count = count + 1
                            for tr in comparethreadrunnablelist:
                                if tr == class_comp:
                                    comp = "ThreadRunnable"
                                    if class_name not in threadrunnablelist:
                                        newthreadrunnablelist.append(class_name)
                                        count = count + 1
                            for tr in comparethreadasynclist:
                                if tr == class_comp:
                                    comp = "ThreadAsync"
                                    if class_name not in threadasynclist:
                                        newthreadasynclist.append(class_name)
                                        count = count + 1

                            i = i + 1
                        i = i + 1
                    i = i + 1

                for a1 in newactivitylist:
                    activitylist.append(a1)
                # print "=======================================new activitylist"
                # print newactivitylist
                for s1 in newservicelist:
                    servicelist.append(s1)
                for b1 in newbroadcastlist:
                    broadcastlist.append(b1)
                for con1 in newcontentlist:
                    contentlist.append(con1)
                for t1 in newthreadlist:
                    threadlist.append(t1)
                for tr1 in newthreadrunnablelist:
                    threadrunnablelist.append(tr1)
                for ta1 in newthreadasynclist:
                    threadasynclist.append(ta1)

                newactivitylist = {}.fromkeys(newactivitylist).keys()
                newservicelist = {}.fromkeys(newservicelist).keys()
                newbroadcastlist = {}.fromkeys(newbroadcastlist).keys()
                newcontentlist = {}.fromkeys(newcontentlist).keys()
                newthreadlist = {}.fromkeys(newthreadlist).keys()
                newthreadrunnablelist = {}.fromkeys(newthreadrunnablelist).keys()
                newthreadasynclist = {}.fromkeys(newthreadasynclist).keys()

                compareactivitylist = newactivitylist
                compareservicelist = newservicelist
                comparebroadcastlist = newbroadcastlist
                comparecontentlist = newcontentlist
                comparethreadlist = newthreadlist
                comparethreadrunnablelist = newthreadrunnablelist
                comparethreadasynclist = newthreadasynclist


        activitylist = {}.fromkeys(activitylist).keys()
        servicelist = {}.fromkeys(servicelist).keys()
        broadcastlist = {}.fromkeys(broadcastlist).keys()
        contentlist = {}.fromkeys(contentlist).keys()
        threadlist = {}.fromkeys(threadlist).keys()
        threadrunnablelist = {}.fromkeys(threadrunnablelist).keys()
        threadasynclist = {}.fromkeys(threadasynclist).keys()
        #print len(activitylist)
        #print len(servicelist)
        #print len(broadcastlist)
        #print len(contentlist)
        #print len(threadlist)

        return list1, activitylist, servicelist, broadcastlist, contentlist, threadlist, threadrunnablelist, threadasynclist