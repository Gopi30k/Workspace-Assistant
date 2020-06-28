import time
import tkinter as tk
import tkinter.messagebox as tmsg
import logging
import ctypes
import pythoncom
import pyHook
import sys

class WorkspaceAssistant():

    workTime = 0
    breakTime = 0
    alertTime = 0
    freezeTime = 0
    

    def __init__(self, wTime, bTime, aTime, fTime):
        self.workTime = wTime
        self.breakTime = bTime
        self.alertTime = aTime
        self.freezeTime = fTime

    def minsTimer(self, workMinute, breakMinute):
        totalIter = workMinute * 60
        while totalIter >= 0:
            m, s = divmod(totalIter, 60)
            h, m = divmod(m, 60)
            timer = str(h).zfill(2) + ":" + \
                str(m).zfill(2) + ":" + str(s).zfill(2)
            print(timer)
            totalIter -= 1
            time.sleep(1)
            if(totalIter == (breakMinute * 60)):
                return True
        return False

    def secsTimer(self, workMinute, breakMinute):
        while workMinute >= 0:
            m, s = divmod(workMinute, 60)
            h, m = divmod(m, 60)
            timer = str(h).zfill(2) + ":" + \
                str(m).zfill(2) + ":" + str(s).zfill(2)
            print(timer)
            workMinute -= 1
            time.sleep(1)
            if(workMinute == breakMinute):
                return True
        return False

    def blockUserActions(self):
        # print(" You are freezed!, Please Take 10 mins break it is needed for you ")
        tmsg.showinfo('WorkSpace Assistant',
                      'You are freezed!, Please Take 10 mins break it is needed for you')
        hm = pyHook.HookManager()
        # hm.MouseAll = lambda event : False
        hm.KeyAll = lambda event: False
        # hm.HookMouse()
        hm.HookKeyboard()
        while time.process_time() < self.freezeTime:
            pythoncom.PumpWaitingMessages()
        # ctypes.windll.User32.LockWorkStation()

    def count_down(self,sec):
        # start with 2 minutes --> 120 seconds
        for t in range(sec, -1, -1):
            # format as 2 digit integers, fills with zero to the left
            # divmod() gives minutes, seconds
            sf = "{:02d}:{:02d}".format(*divmod(t, 60))
            #print(sf)  # test
            time_str.set(sf)
            root.update()
            # delay one second
            time.sleep(1)

    def task_executioner(self):
        if self.secsTimer(self.workTime, self.breakTime):
            choice = tmsg.askyesno(
                'WorkSpace Assistant', 'You have been working for 90 Mins!! \nTake a break for 10 mins')
            # choice = int(input("Take a Break for 10 mins \n 1. sure \n 2. Hold On \n Enter "))
            if choice == True:
                if(tmsg.showinfo('WorkSpace Assistant',
                                 'Okay!! You have 10 mins to take break')):
                    
                    
                    self.count_down(120)
                    


                if self.secsTimer(self.breakTime, self.alertTime):
                    # print('You will be freezed in 2 mins for Break')
                    tmsg.showwarning(
                        'WorkSpace Assistant', 'You will be freezed in 2 mins !! \nTake 10 mins break and come back')
                    if self.secsTimer(self.alertTime, 0):
                        self.blockUserActions()
            if choice == False:
                # print('Okay Grace time 10 mins Added')
                tmsg.showinfo('WorkSpace Assistant',
                              'Okay!! You are provided with 10 mins grace time')
                if self.secsTimer(self.breakTime * 2, self.alertTime):
                    # print('You will be freezed in 2 mins for Break')
                    tmsg.showwarning(
                        'WorkSpace Assistant', 'Oops !! Your grace time ended, freezing in 2 mins \nTake 10 mins break and come back')
                    if self.secsTimer(self.alertTime, 0):
                        self.blockUserActions()


if __name__ == "__main__":
    root = tk.Tk()
    time_str = tk.StringVar()
    label_font = ('helvetica', 40)
    tk.Label(root, textvariable=time_str, font=label_font, bg='white', 
                            fg='blue', relief='raised', bd=3).pack(fill='x', padx=5, pady=5)
    root.title("WorkSpace Assistant")
    root.iconbitmap(
        r'C:\\Users\\g.krishnan.gajendran\\Desktop\\My Stuffs\\Learning\\Python Learning\\favicon.ico')
    root.overrideredirect(1)
    root.withdraw()
    WorkspaceAssistant(6, 4, 2, 5).task_executioner()