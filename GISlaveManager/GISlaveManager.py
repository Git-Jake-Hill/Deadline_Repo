###############################################################
# Imports
###############################################################
from System import *

from System.Diagnostics import *
from System.IO import *
from System.Text.RegularExpressions import *

from Deadline.Events import *
from Deadline.Scripting import *
from Deadline.Jobs import *

import re

def GetDeadlineEventListener():
	return GISlaveManagerListener()


def CleanupDeadlineEventListener(eventListener):
	eventListener.Cleanup()

def AnimGIJobCheck(job):
	GIPattern = '- GI'
	if re.search(GIPattern, job.JobName):
		if job.JobTaskCount > 1: # check if it's an animation
			#Need to check if animation is every frame or Nth frame.  If every frame then it's a prepass for animation which can be on all machines
			#startFrame = deadlinePlugin.GetStartFrame()
			#endFrame = deadlinePlugin.GetEndFrame()
			#self.LogInfo("START FRAME: " + startFrame)
			#self.LogInfo("END FRAME: " + endFrame)
			#frames = Job.JobFrames
			#self.LogInfo("FRAMES: " + frames)
			return True
		else:
			return False
	else:
		return False

def GIStarted (job, sName):
	sSettings = RepositoryUtils.GetSlaveSettings(sName, True) # Get the slave settings
	sInfo = RepositoryUtils.GetSlaveInfo(sName, True) # Get the slave info
	
	# Set Slave to GI Render Group 
	sGroups = sSettings.SlaveGroups	
	for i in range(len(sGroups)):
		if sGroups[i] == "gifree":
			sGroups[i] = "girender"
			sSettings.SetSlaveGroups(sGroups)
			RepositoryUtils.SaveSlaveSettings(sSettings)
 
	# Set Job to GI Render Group
	job.JobGroup = 'girender'
	RepositoryUtils.SaveJob(job) # Change the Job's Group
	
	# Add Slave to Job Whitelist
	RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, sName) #add slave to whitelist
	RepositoryUtils.SetMachineLimitWhiteListFlag(job.JobId, True) #set limit to whitelist in case its on blacklist
	
def GIStopped (job, sName):
	sSettings = RepositoryUtils.GetSlaveSettings(sName, True) # Get the slave settings
	sInfo = RepositoryUtils.GetSlaveInfo(sName, True) # Get the slave info
	
	# Set Slave to GI Free Group
	sGroups = sSettings.SlaveGroups
	for i in range(len(sGroups)):
		if sGroups[i] == "girender":
			sGroups[i] = "gifree"
			sSettings.SetSlaveGroups(sGroups)
			RepositoryUtils.SaveSlaveSettings(sSettings)
	
	# Set Job to GI Free Group
	job.JobGroup = 'gifree'
	RepositoryUtils.SaveJob(job) # Change the Job's Group
	
	# Clear Job Whitelist
	RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, None) # Clear whitelist

###############################################################
# The event listener class.
###############################################################

class GISlaveManagerListener (DeadlineEventListener):
	def __init__(self):
		self.OnSlaveStartingJobCallback += self.OnSlaveStartingJob
		self.OnJobRequeuedCallback += self.OnJobRequeued
		self.OnJobFinishedCallback += self.OnJobFinished
		self.OnJobFailedCallback += self.OnJobFailed
		self.OnJobSuspendedCallback += self.OnJobSuspended
		
	def Cleanup(self):
		del self.OnSlaveStartingJobCallback
		del self.OnJobRequeuedCallback
		del self.OnJobFinishedCallback
		del self.OnJobFailedCallback
		del self.OnJobSuspendedCallback

	def OnSlaveStartingJob(self, sName, job):
		isGIJob = AnimGIJobCheck(job) #Check if it's a GI Job
		if isGIJob == True:
			if job.JobCompletedTasks < 1: # Check to see if this is the first task
				self.LogInfo("GI Slave Manager - SLAVE STARTING JOB")
				GIStarted(job, sName) # Run the GIStarted function

	def OnJobRequeued( self, job ):
		isGIJob = AnimGIJobCheck(job) #Check if it's a GI Job
		if isGIJob == True:
			self.LogInfo("GI Slave Manager - JOB REQUEUED")
			WLSlaves = job.JobListedSlaves # Need to get the name of the last used slave from the whitelist
			if len(WLSlaves) > 0: # Check to see if job has any whitelisted slaves first (ie. was it already suspended)
				WLSlave = WLSlaves[0] # Get the first item in the Whitelist
				GIStopped(job, WLSlave) # Run the GIStopped function

	def OnJobFinished( self, job ):
		isGIJob = AnimGIJobCheck(job) #Check if it's a GI Job
		if isGIJob == True:
			self.LogInfo("GI Slave Manager - JOB FINISHED")
			WLSlaves = job.JobListedSlaves # Need to get the name of the last used slave from the whitelist
			if len(WLSlaves) > 0: # Check to see if job has any whitelisted slaves first (ie. was it already suspended)
				WLSlave = WLSlaves[0] # Get the first item in the Whitelist
				GIStopped(job, WLSlave) # Run the GIStopped function
		
	def OnJobFailed( self, job ):
		isGIJob = AnimGIJobCheck(job) #Check if it's a GI Job
		if isGIJob == True:
			self.LogInfo("GI Slave Manager - JOB FAILED")
			WLSlaves = job.JobListedSlaves # Need to get the name of the last used slave from the whitelist
			if len(WLSlaves) > 0: # Check to see if job has any whitelisted slaves first (ie. was it already suspended)
				WLSlave = WLSlaves[0] # Get the first item in the Whitelist
				GIStopped(job, WLSlave) # Run the GIStopped function

	def OnJobSuspended( self, job ):
		isGIJob = AnimGIJobCheck(job) #Check if it's a GI Job
		if isGIJob == True:
			self.LogInfo("GI Slave Manager - JOB SUSPENDED")	
			WLSlaves = job.JobListedSlaves # Need to get the name of the last used slave from the whitelist
			if len(WLSlaves) > 0: # Check to see if job has any whitelisted slaves first (ie. was it already suspended)
				WLSlave = WLSlaves[0] # Get the first item in the Whitelist
				GIStopped(job, WLSlave) # Run the GIStopped function