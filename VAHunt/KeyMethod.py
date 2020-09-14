# encoding: utf-8

class KeyMethod:
    def __init__(self):
        pass
        # self.name = ''     # 名称
        # self.size = 10     # 尺寸
        # self.list = []     # 列表

    def extractSensitiveAPI(self,list1):
        # a = item()  # 定义结构对象
        # a.name = 'cup'
        # a.size = 8
        # a.list.append('water')
        # print a.list
        sensitiveAPI = []

        # 18 + 3 Android APIs to get file paths
        filepathAPI = ['getDataDirectory', 'getCacheDir', 'getFilesDir', 'getFileStreamPath', 'openFileOutput',
                       'getDataDir', 'openOrCreateDatabase', 'openDatabase',
                       'getSharedPreferences', 'getDefaultSharedPreferences', 'getPreferences', 'getDir',
                       'openOrCreateDatabase', 'getExternalStorageDirectory',
                       'getExternalStoragePublicDirectory', 'getObbDir', 'getExternalCacheDir', 'getExternalFilesDir',
                       'getAssets', 'getPath', 'getCanonicalPath', 'getAbsolutePath']
        writeAPI =['write','writeBytes','writeTo']
        threadAPI =['onPreExecuate','doInBackground','onProgressUpdate','onPostExecuate']
        # doInBackground是必须要实现的方法， onPostExecuate

        # 在api_code中的使用
        # for l in list1:
        #     if l[3] in filepathAPI:
        #         sensitiveAPI.append(l)
        #     elif l[3] in writeAPI:
        #         sensitiveAPI.append(l)
        #     elif l[3] in threadAPI:
        #         sensitiveAPI.append(l)

        # 在CFGparse中的使用
        for l in list1:
            if l[1] in filepathAPI:
                sensitiveAPI.append(l)
            # elif l[1] in writeAPI:
            #     sensitiveAPI.append(l)
            # elif l[1] in threadAPI:
            #     sensitiveAPI.append(l)
        return sensitiveAPI

    def extractSensitivePathAPI(self):
        # 18 + 3 Android APIs to get file paths
        filepathAPI = ['getDataDirectory', 'getCacheDir', 'getFilesDir', 'getFileStreamPath', 'openFileOutput',
                       'getDataDir', 'openOrCreateDatabase', 'openDatabase',
                       'getSharedPreferences', 'getDefaultSharedPreferences', 'getPreferences', 'getDir',
                       'openOrCreateDatabase', 'getExternalStorageDirectory',
                       'getExternalStoragePublicDirectory', 'getObbDir', 'getExternalCacheDir', 'getExternalFilesDir',
                       'getAssets', 'getPath', 'getCanonicalPath', 'getAbsolutePath',
                       "installPackage", "installApk", "installApp","setComponentEnabledSetting"]
        VirtualMethod = ['onCreateViewHolder']
        writeAPI =['write','writeBytes','writeTo']
        threadAPI =['onPreExecuate','doInBackground','onProgressUpdate','onPostExecuate']

        return filepathAPI
