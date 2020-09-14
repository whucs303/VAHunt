# encoding: utf-8
import os

# to configure file paths and running parameters
class Config:

    @staticmethod
    def read_file(filename):
        ret = []
        with open(filename, "r") as fin:
            return fin.readlines()

    rootPath = os.getcwd()

    VA_SAMPLE_PATH = "E:\\samples\\va\\"
    VA_SUBNAME1 = "\\config\\va-success-apklist.txt"
    VA_SUBNAME2 = "\\config\\va-apklist.txt"
    VA_FINISH_SUBNAME1 = "\\resdata\\finishAPK-record.txt"
    MALVA_FINISH_SUBNAME1 = "\\resdata\\finishMAL-record.txt"
    RESULT_RECORD_FILENAME = "\\resdata\\Record.txt"
    RESULT_RECORD_MALNAME = "\\resdata\\MalRecord.txt"
    BROKEN_PATH = "E:\\samples\\broken\\"
    MANIFEST_PATH = rootPath + "\\APPmanifest\\"
    CODE_PATH = rootPath + "\\APPcode\\"
    TRAIN_NUM = "\\trainNumber.txt"
    RES_DIR = "\\res\\"

if __name__ == '__main__':
    print(Config.VA_SAMPLE_PATH)

