# encoding: utf-8

class ObjectAnalyzenew:
    def __init__(self):
        pass

    def filterSystemMethods(self, pathlist):

        if pathlist[0].startswith("android.support.") or pathlist[0].startswith("com.baidu.") or pathlist[0].startswith(
                "com.duoku.platform.single.") \
                or pathlist[0].startswith("com.alibaba.") or pathlist[0].startswith("com.idsky.android.") \
                or pathlist[0].startswith("com.alipay.") or pathlist[0].startswith("com.snmi.sdk.") \
                or pathlist[0].startswith("com.tencent.") or pathlist[0].startswith("com.youdao.sdk.") \
                or pathlist[0].startswith("cn.egame.terminal.sdk") or pathlist[0].startswith(
            "com.aggregationad.database.") \
                or pathlist[0].startswith("com.idreamsky.ad.") or pathlist[0].startswith("com.prime31.") \
                or pathlist[0].startswith("com.snmi.sdk.") or pathlist[0].startswith("com.xiaomi.") \
                or pathlist[0].startswith("com.yumi.android.sdk.") or pathlist[0].startswith("com.zplay.android.sdk.") \
                or pathlist[0].startswith("org.xwalk.core.") or pathlist[0].startswith("org.cocos2dx.wgelib.") \
                or pathlist[0].startswith("org.cocos2dx.wgelib.") or pathlist[0].startswith("org.chromium.") \
                or pathlist[0].startswith("com.maxthon.mge.") or pathlist[0].startswith("com.google.android."):
            return False
        else:
            return True

    def getFinalmethodinVirtualMethod(self, lines, i):
        lines_length = len(lines)
        file_reg = lines[i].split('{')[1].split('}')[0]
        path_reg = ""
        path_reg1 = ""
        path_reg2 = ""
        path_reg3 = ""
        if lines[i + 1].find("move-result-object ") >= 0:
            path_reg = lines[i + 1].split('move-result-object ')[1].replace(
                "\n", "")
            path_reg1 = path_reg + ","
            path_reg2 = path_reg + "}"
            path_reg3 = "move-result-object " + path_reg
            # print "path_reg3---------1   " + path_reg3
        # 往后追溯reg对象被用于做什么了
        k = i
        final_method = ""
        final_Class = ""
        final_method0 = []
        # 一直寻找到这个方法结束，即下一个方法前
        while (lines[k].find("    #") < 0) and k <= lines_length - 3:
            k = k + 1
            # print "path_reg"
            # print path_reg
            # print path_reg1
            # print path_reg3
            if lines[k].find("invoke-") >= 0 and lines[k].find(
                    path_reg1) >= 0 or lines[k].find("invoke-") >= 0 and lines[k].find(path_reg2) >= 0 and k <= lines_length - 3:
                # print "invoke - args reg!"
                # print lines[k]
                final_method0 = []
                final_Class = lines[k].split(" L")[1].split(';')[0].replace('/',
                                                                            '.')
                final_method = lines[k].split(";.")[1].split(':')[0]
                final_args = lines[k].split("(")[1].split(')')[0]
                final_method0.append(final_Class)
                final_method0.append(final_method)
                final_method0.append(final_args)
                if lines[k + 1].find("move-result-object") >= 0:
                    path_reg = lines[k + 1].split("move-result-object ")[
                        1].replace("\n", "")
                    # print lines[k]
                    # print "move-result-object - " + path_reg
                    path_reg1 = path_reg + ","
                    path_reg2 = path_reg + "}"
                    path_reg3 = "move-result-object " + path_reg
                    # print "path_reg3---------2   " + path_reg3
                elif lines[k + 1].find("move-result ") >= 0 and (lines[k].find(";.append:") >= 0 or lines[k].find(";.substring:") >= 0 or lines[k].find(";.toString:") >= 0):
                    path_reg = lines[k + 1].split("move-result ")[
                        1].replace("\n", "")
                    # print "move-result-object - " + path_reg
                    path_reg1 = path_reg + ","
                    path_reg2 = path_reg + "}"
                    path_reg3 = "move-result-object " + path_reg
                    # print "path_reg3---------3   " + path_reg3
            elif lines[k].find(path_reg3) >= 0 and path_reg != "":
                # print "getAbsolutePath - move-result-object reg!" + path_reg
                final_method0 = []
                # print "path_reg3---------4   " + path_reg3
                # print lines[k-1]
                if lines[k - 1].find(" L") >= 0:
                    final_Class = lines[k - 1].split(" L")[1].split(';')[0]
                    # print final_Class
                    final_method = lines[k - 1].split(";.")[1].split(':')[0]
                    final_args = lines[k - 1].split("(")[1].split(')')[0]
                    final_method0.append(final_Class)
                    final_method0.append(final_method)
                    final_method0.append(final_args)

            elif lines[k].find(path_reg + "\n") >= 0 and lines[k].find(
                    "move-object/from16") >= 0:
                path_reg = lines[k].split("move-object/from16 ")[1].split(", ")[
                    0]
                # print "move-object/from16 - " + path_reg
                path_reg1 = path_reg + ","
                path_reg2 = path_reg + "}"
                path_reg3 = "move-result-object " + path_reg
        # print "-----------" + final_method
        # print "final_method0"
        # print final_method0
        return final_method0
