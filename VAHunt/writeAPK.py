# encoding: utf-8
import os
from Config import Config

def file_name(file_dir):
    files = []
    for root, dirs, files in os.walk(file_dir):
        print files
    return files

if __name__ == '__main__':
    # 将所有的apk文件名写入benign_va-filename
    rootPath = os.getcwd()
    # rootPath = "E:\PycharmProjects\DataExTract-complete-20190114\DataExTract"
    print rootPath
    va_filename = rootPath + Config.VA_SUBNAME1
    # print BVA_FILENAME
    apklist = file_name(Config.VA_SAMPLE_PATH1)
    vafile = open(va_filename, "a+")

    for apk in apklist:
        apk = apk.replace(".zip",".zip\n")
        vafile.write(apk)

    vafile.close()
