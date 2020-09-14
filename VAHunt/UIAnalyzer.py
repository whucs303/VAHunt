# encoding: utf-8
import operator

#节点数据结构
class Node(object):
    # 初始化一个节点
    def __init__(self,value = None):
        self.value = value  # 节点值
        self.child_list = []    # 子节点列表

    # 添加一个孩子节点
    def add_child(self,node):
        self.child_list.append(node)

# 初始化一颗测试二叉树
#          A
#      B   C   D
#    EFG       HIJ
def init():
    root = Node('A')
    B = Node('B')
    root.add_child(B)
    root.add_child(Node('C'))
    D = Node('D')
    root.add_child(D)
    B.add_child(Node('E'))
    B.add_child(Node('F'))
    B.add_child(Node('G'))
    D.add_child(Node('H'))
    D.add_child(Node('I'))
    D.add_child(Node('J'))
    return root

def get_leaves(node):
    if not node.child_list:
        yield node

    for child in node.child_list:
        for leaf in get_leaves(child):
             yield leaf

if __name__=="__main__":
    root = init()
    # print "root"
    # print root.child_list[0].value
    leaves = get_leaves(root)
    print "leaves"
    for leaf in leaves:
        print leaf.value


class UIAnalyzer:
    def __init__(self):
        pass

    def processIntussusception(self, file_codetxt, invokeMethod):
        oriInvokeMethod = invokeMethod
        print "oriInvokeMethod----processIntussus"
        print oriInvokeMethod
        invokeMethod = []
        VirtualMethodClass = ""
        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0
            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    i = i + 1
                while lines[i].startswith("    #") and lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    if lines[i].find("(in L")>=0:
                        VirtualMethodClass = lines[i].split("(in L")[1].split(';)')[0].replace("/",".")
                    classline = i
                    i = i + 1
                while (lines[i].find("new-instance") >= 0 and lines[i].find(oriInvokeMethod[0]) >= 0):
                    print "new-instance-------"
                    if lines[i + 1].find("invoke-direct") >= 0 and lines[i+1].find(oriInvokeMethod[0]+";.<init>:") >= 0:
                        print "invoke-derict-----"
                        invokeMethod = []
                        invokeMethod.append(class_name)
                        invokeMethod.append(VirtualMethod)
                        return invokeMethod
                    i = i + 1
                i = i + 1
        return invokeMethod

    def processThreadStart(self, file_codetxt, invokeMethod):
        oriInvokeMethod = invokeMethod
        invokeMethod = []
        VirtualMethodClass = ""
        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0

            while i <= lines_length - 3:

                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    i = i + 1
                while lines[i].startswith("    #") and lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    if lines[i].find("(in L")>=0:
                        VirtualMethodClass = lines[i].split("(in L")[1].split(';)')[0].replace("/",".")
                        # print "VirtualMethodClass"
                        # print VirtualMethodClass
                    classline = i
                    i = i + 1
                while (lines[i].find("new-instance") >= 0 and lines[i].find("Ljava/lang/Thread") >= 0) and class_name.find("com.lody.virtual") < 0 and class_name.find(
                    "android.support.") < 0:
                    if lines[i + 1].find("invoke-direct") >= 0 and lines[i+1].find("Ljava/lang/Thread;.<init>:(Ljava/lang/Runnable") >= 0:
                        if VirtualMethodClass == oriInvokeMethod[0] and lines[i+2].find("Ljava/lang/Thread;.start") >= 0:
                            invokeMethod = []
                            invokeMethod.append(class_name)
                            invokeMethod.append(VirtualMethod)
                            print invokeMethod
                    i = i + 1
                i = i + 1
        return invokeMethod

    def processThreadInterupt(self, file_codetxt, invokeMethod):
        oriInvokeMethod = invokeMethod
        invokeMethod = []
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
                while (lines[i].find("invoke-direct") >= 0) and class_name.find("com.lody.virtual") < 0 and class_name.find(
                    "android.support.") < 0:
                    if lines[i].find(" L") >= 0:
                        invokeVirtual = lines[i].split(' L')
                        method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]
                        if method_class == oriInvokeMethod[0] and method_name == "<init>":
                            invokeMethod = []
                            invokeMethod.append(class_name)
                            invokeMethod.append(VirtualMethod)
                    i = i + 1
                i = i + 1
        return invokeMethod

    def repeateReadFile(self, file_codetxt, invokeMethod, root):
        childNode = None
        oriInvokeMethod = invokeMethod
        invokeMethod = []
        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)
            i = 0
            # super_class = ""

            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    # if lines[i+3].find("  Superclass        :")>=0 and lines[i+3].find("'L")>=0:
                    #     super_class = lines[i+3].split("'L")[1].split(";")[0]
                    i = i + 1
                while lines[i].startswith("    #") & lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    classline = i
                    i = i + 1
                while (lines[i].find("invoke-virtual") >= 0 or lines[i].find("invoke-static") >= 0 or lines[i].find(
                        "invoke-super") >= 0 or lines[i].find(
                        "invoke-direct") >= 0) and class_name.find("com.lody.virtual") < 0 and class_name.find(
                    "android.support.") < 0:
                    if lines[i].find(" L") >= 0:
                        invokeVirtual = lines[i].split(' L')
                        method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]
                        # 1.先得找到真正的被调用者
                        # 2.碰到doInBackground再进行处理
                        if method_name == oriInvokeMethod[1] and method_class == oriInvokeMethod[0]:
                            if class_name + VirtualMethod != method_class + method_name:
                                invokeMethod = []
                                invokeMethod.append(class_name)
                                invokeMethod.append(VirtualMethod)
                                # print class_name + "---" + VirtualMethod
                                childNode = Node(invokeMethod)
                                root.add_child(childNode)
                    i = i + 1
                i = i + 1
        return invokeMethod, childNode

    def findMethodChain(self, file_codetxt, rootMethod, firstInvokeMethod, launchActivities):
        invokeMethod = firstInvokeMethod
        root = Node(rootMethod)
        ori_root = root
        invokeChain = []
        count = 0
        action = 0
        while(invokeMethod != []):
            oldInvokeMethod = invokeMethod
            if oldInvokeMethod[1] == "onDone":
                print "===========onDone"
                newinvokeMethod = []
                newinvokeMethod[0] = oldInvokeMethod[0].replace(".","/")
                newinvokeMethod[1] = oldInvokeMethod[1]
                invokeMethod = self.processIntussusception(file_codetxt, newinvokeMethod)
            else:
                invokeMethod, childNode = self.repeateReadFile(file_codetxt, invokeMethod, root)
                root = childNode
                print "invokeMethod2"
                print invokeMethod
                if invokeMethod != []:
                    if invokeMethod[1] == "onDone":
                        print "===========onDone1"
                        newinvokeMethod = []
                        newinvokeMethod.append(invokeMethod[0].replace(".", "/"))
                        newinvokeMethod.append(invokeMethod[1])
                        print newinvokeMethod
                        invokeMethod = self.processIntussusception(file_codetxt, newinvokeMethod)
                        print invokeMethod

            if invokeMethod not in invokeChain:
                invokeChain.append(invokeMethod)
            else:
                return 0
            # 判断是否是LAUNCHER组件
            if invokeMethod != []:
                if operator.eq(oldInvokeMethod, invokeMethod) is False:
                    # action = self.judgeAction(file_codetxt, invokeMethod, launchActivities)
                    for la in launchActivities:
                        if invokeMethod[0] == la:
                            print "invokeMethod3 " + str(invokeMethod)
                            return 1
                    if invokeMethod[1] == "doInBackground":
                        # 先找到真正的调用者
                        invokeMethod = self.processThreadInterupt(file_codetxt, invokeMethod)
                    elif invokeMethod[1] == "run":
                        invokeMethod = self.processThreadInterupt(file_codetxt, invokeMethod)
                    elif invokeMethod[1] == "onCreate":
                        print "invokeMethod1 " + str(invokeMethod)
                        return 1
                    # 用户点击
                    elif invokeMethod[1] == "onItemClick" or invokeMethod[1] == "onClick":
                        print "Click " + str(invokeMethod)
                        return 2
                if invokeMethod != [] and len(invokeMethod) == 2:
                    if invokeMethod[1] == "onCreate":
                        print "invokeMethod2 " + str(invokeMethod)
                        return 1

        # leaves = get_leaves(ori_root)
        # print "leaves"
        # for leaf in leaves:
        #     print leaf.value
        return 0

    def findListViewAndPM(self):
        listpm = 1
        return listpm

    def findListView(self, file_codetxt, installline):
        listview = 1

        with open(file_codetxt, "rU") as f:
            lines = f.readlines()
            lines_length = len(lines)

            while i <= lines_length - 3:
                while lines[i].startswith("Class #"):
                    class_name1 = lines[i + 1].split("'")[1]
                    class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                    class_count = class_count + 1
                    i = i + 1
                while lines[i].startswith("    #") & lines[i + 1].startswith("      name"):
                    VirtualMethod = lines[i + 1].split("'")[1]
                    classline = i
                    i = i + 1
                while lines[i].find("invoke-virtual") >= 0 or lines[i].find("invoke-static") >= 0 or lines[i].find(
                        "invoke-super") >= 0:
                    tmplist = []
                    if lines[i].find(" L") >= 0:
                        invokeVirtual = lines[i].split(' L')
                        method_class = invokeVirtual[1].split(';')[0].replace('/', '.')
                        method_name1 = invokeVirtual[1].split('.')[1]
                        method_name = method_name1.split(':')[0]

        listpm = self.findListViewAndPM()
        return listview, listpm


    def findClick(self):
        click = 1
        return click