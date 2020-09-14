import os
import numpy as np

class framework_map_api:
    def __init__(self):
        pass
    def extractMethod(self):
        rootPath = os.getcwd()
        filePath = os.path.join(rootPath, "APImap\\framework-map-22_new.txt")

        with open(filePath, "r") as f:
            lines = f.readlines()
            lines_length = len(lines)
            fmap = np.zeros((lines_length / 2, 4), basestring)
            #print lines_length

            i = 0
            count = 0
            while i <= lines_length-1:
                if i % 2 == 0:
                    method_name1 = lines[i].split(" ")[2]
                    method_name = method_name1.split("(")[0]
                    #print method_name
                    return_value = lines[i].split(" ")[1]
                    #print return_value
                    method_class1 = lines[i].split(" ")[0]
                    method_class = method_class1.replace('<', '').replace(':', '')
                    #print method_class
                    method_perm = lines[i + 1]
                    #print method_perm
                    fmap[count][0] = method_name
                    fmap[count][1] = return_value
                    fmap[count][2] = method_class
                    fmap[count][3] = method_perm
                    count = count + 1
                i = i + 2
        return fmap           #an array
