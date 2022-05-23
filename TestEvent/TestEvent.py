'''
    Show what copy of a particular piece of software is installed on your
    Windows nodes in the 'Extra Info 0-5' column.
'''

from System.Diagnostics import *
from System.IO import *
from System import TimeSpan

from Deadline.Events import *
from Deadline.Scripting import *

import _winreg
import time
import os


def GetDeadlineEventListener():
    return ConfigSlaveEventListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


class ConfigSlaveEventListener (DeadlineEventListener):
    def __init__(self):
        self.OnSlaveStartedCallback += self.OnSlaveStarted

    def Cleanup(self):
        del self.OnSlaveStartedCallback

    # This is called every time the Slave starts
    def OnSlaveStarted(self, slavename):
        if os.name == "nt":
            title = self.GetConfigEntry("Software Title")
            if ";" in title:
                title = title.split(";")
                slave = RepositoryUtils.GetSlaveSettings(slavename, True)
                for n in range(0, len(title)):
                    if n == 0:
                        slave.SlaveExtraInfo1 = self.GetVersion(title[n])
                    elif n == 1:
                        slave.SlaveExtraInfo2 = self.GetVersion(title[n])
                    elif n == 2:
                        slave.SlaveExtraInfo3 = self.GetVersion(title[n])
                    elif n == 3:
                        slave.SlaveExtraInfo4 = self.GetVersion(title[n])
                    elif n == 4:
                        slave.SlaveExtraInfo5 = self.GetVersion(title[n])
            else:
                slave = RepositoryUtils.GetSlaveSettings(slavename, True)
                slave.SlaveExtraInfo1 = self.GetVersion(title)
            time.sleep(2)
            RepositoryUtils.SaveSlaveSettings(slave)
        else:
            print ("Not windows slave.")
            return

    def GetVersion(self, software_title):
        versions = []
        try:
            i = 0
            explorer = _winreg.OpenKey(
                _winreg.HKEY_LOCAL_MACHINE,
                'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
            )

            while True:
                key = _winreg.EnumKey(explorer, i)
                if software_title in key and "Populate Data" not in key:
                    print('Found "{0}" in the list of installed software'.format(key))
                    try:
                        item = _winreg.OpenKey(explorer, key)
                        version, type = _winreg.QueryValueEx(item, 'DisplayVersion')
                        print(' Its version was {0}'.format(version))
                        _winreg.CloseKey(item)

                        #_winreg.CloseKey(explorer)
                        #return version
                        if version not in versions:
                            versions.append(version)
                    except:
                        print("No DisplayVersion key found. Trying DisplayName.")
                        try:
                            item = _winreg.OpenKey(explorer, key)
                            version, type = _winreg.QueryValueEx(item, 'DisplayName')
                            print(' Its version was {0}'.format(version))
                            _winreg.CloseKey(item)

                            #_winreg.CloseKey(explorer)
                            #return version
                            if version not in versions:
                                versions.append(version)
                        except:
                            _winreg.CloseKey(item)
                            print("No DisplayName key found.")
                        _winreg.CloseKey(item)
                        
                i += 1

        except WindowsError as e:
            print(e)

        _winreg.CloseKey(explorer)
        InstalledVersions = ""
        try:
            if versions[0] != "":
                for t in versions :
                    print(t)
                    if InstalledVersions == "":
                        InstalledVersions = t
                    else:
                        InstalledVersions = InstalledVersions + ", " + t
                return InstalledVersions
            else:
                return "unknown"
        except:
            return "unknown"