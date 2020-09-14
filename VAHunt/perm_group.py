import os

class perm_group:
    def __init__(self):
        pass
    def definePermGroup(self):
        permList = [([0] * 7) for i in range(9)]

        # 26 permissions
        # group:android.permission-group.CONTACTS
        permList[0][0] = "android.permission.WRITE_CONTACTS"
        permList[0][1] = "android.permission.READ_CONTACTS"
        permList[0][2] = "android.permission.GET_ACCOUNTS"

        # group:android.permission-group.PHONE
        permList[1][0] = "android.permission.READ_CALL_LOG"
        permList[1][1] = "android.permission.READ_PHONE_STATE"
        permList[1][2] = "android.permission.CALL_PHONE"
        permList[1][3] = "android.permission.WRITE_CALL_LOG"
        permList[1][4] = "android.permission.USE_SIP"
        permList[1][5] = "android.permission.PROCESS_OUTGOING_CALLS"
        permList[1][6] = "com.android.voicemail.permission.ADD_VOICEMAIL"

        # group:android.permission-group.CALENDAR
        permList[2][0] = "android.permission.WRITE_CALENDAR"
        permList[2][1] = "android.permission.READ_CALENDAR"

        # group:android.permission-group.CAMERA
        permList[3][0] = "android.permission.CAMERA"
        permList[3][1] = "com.sec.android.app.camera.permission.SHOOTING_MODE"

        # group:android.permission-group.SENSORS
        permList[4][0] = "android.permission.BODY_SENSORS"

        # group:android.permission-group.LOCATION
        permList[5][0] = "android.permission.ACCESS_FINE_LOCATION"
        permList[5][1] = "android.permission.ACCESS_COARSE_LOCATION"

        # group:android.permission-group.STORAGE
        permList[6][0] = "android.permission.READ_EXTERNAL_STORAGE"
        permList[6][1] = "android.permission.WRITE_EXTERNAL_STORAGE"

        # group:android.permission-group.MICROPHONE
        permList[7][0] = "android.permission.RECORD_AUDIO"

        # group:android.permission-group.SMS
        permList[8][0] = "android.permission.READ_SMS"
        permList[8][1] = "android.permission.RECEIVE_WAP_PUSH"
        permList[8][2] = "android.permission.RECEIVE_MMS"
        permList[8][3] = "android.permission.RECEIVE_SMS"
        permList[8][4] = "android.permission.SEND_SMS"
        permList[8][5] = "android.permission.READ_CELL_BROADCASTS"

        return permList



