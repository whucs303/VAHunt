import os
from code_api import code_api
import sys

class testShell:
    def __init__(self):
        pass

    def detectShell(self,file_codetxt):
        sys.path.append('G:\\python2.7\\Lib\site-packages')
        lines_length = 0
        res = 0

        codePerm = code_api()
        try:
            lines_length, res = codePerm.shell(file_codetxt)
        except Exception as err:
            print(err)

        if lines_length < 10:
            return 0
        if res == 2:
            return 2
