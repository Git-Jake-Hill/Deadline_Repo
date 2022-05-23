'''
    Show what versions of 3dsMax is installed on your
    Windows nodes in the 'Extra Info 0' column.
'''

from System.Diagnostics import *
from System.IO import *
from System import *

import os.path

import clr, sys, re, os, array
from ctypes import *

from Deadline.Events import *
from Deadline.Scripting import *

def GetDeadlineEventListener():
	return ConfigSlaveEventListener()


def CleanupDeadlineEventListener(eventListener):
	eventListener.Cleanup()

def GetPhoenixInfo():
	if os.path.isfile('C:\ChaosPhoenix\ChaosPhoenix 3ds Max 2018.log'):
		f = open('C:\ChaosPhoenix\ChaosPhoenix 3ds Max 2018.log', "rt")
		lines = f.readlines()
		words = lines[1].split(" ")   # words is a list (of strings from a line), delimited by " ".
		versionInfo = words[1]
		versionInfo = versionInfo[:-1] #Remove a , from the end of the line
	else:
		versionInfo = "NONE"
	return versionInfo

class ConfigSlaveEventListener (DeadlineEventListener):
	def __init__(self):
		self.OnSlaveStartedCallback += self.OnSlaveStarted

	def Cleanup(self):
		del self.OnSlaveStartedCallback

	# This is called every time the Slave starts
	def OnSlaveStarted(self, slavename):


		# exit if not Windows slave
		if os.name != 'nt':
			return

		configVersions = self.GetConfigEntry("programVersions").strip()
		programVersions = StringUtils.FromSemicolonSeparatedString(configVersions)

		versionList = []

		for programVersion in programVersions:
			if File.Exists(programVersion):
				# Figure out .NET FileVersion of 3dsmax.exe
				exeVersion = FileUtils.GetExecutableVersion(programVersion)
				# append to our list
				versionList.append(exeVersion)
				self.LogInfo("Program Version: %s" % exeVersion)
			else:
				versionList.append("NOT FOUND")

		if len(versionList) > 0:
			versions = ','.join(versionList)
			self.LogInfo("Program Versions: %s" % versions)

			slave = RepositoryUtils.GetSlaveSettings(slavename, True)
			# The order of the versions is set in the Param file
			slave.SlaveExtraInfo0 = versionList[0] # MAX
			slave.SlaveExtraInfo1 = versionList[1] # BACKBURNER
			slave.SlaveExtraInfo2 = versionList[2] # VRAY
			slave.SlaveExtraInfo3 = versionList[3] # FOREST PACK
			slave.SlaveExtraInfo4 = versionList[4] # RAIL CLONE
			#slave.SlaveExtraInfo5 = versionList[5] # PHOENIX -- DOESN'T WORK ON THIS FILE
			slave.SlaveExtraInfo6 = versionList[5] # ANIMA
			slave.SlaveExtraInfo7 = versionList[6] # AFTER EFFECTS
			
			phoenixVersion = GetPhoenixInfo()
			slave.SlaveExtraInfo5 = phoenixVersion

			RepositoryUtils.SaveSlaveSettings(slave)