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

def GIJobCheck(jobName):
	GIPattern = '~ GI'
	if re.search(GIPattern, jobName):
		return True
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
		self.OnJobFinishedCallback += self.OnJobFinished
		self.OnJobFailedCallback += self.OnJobFailed
		self.OnJobSuspendedCallback += self.OnJobSuspended
		
	def Cleanup(self):
		del self.OnSlaveStartingJobCallback
		del self.OnJobFinishedCallback
		del self.OnJobFailedCallback
		del self.OnJobSuspendedCallback

	def OnSlaveStartingJob(self, sName, job):
		self.LogInfo("GI Slave Manager - SLAVE STARTING JOB")
		
		isGIJob = GIJobCheck(job.JobName) #Check if it's a GI Job
		if isGIJob == True:
			GIStarted(job, sName)

		
#			sSettings = RepositoryUtils.GetSlaveSettings(sName, True) # Get the slave settings
#			sInfo = RepositoryUtils.GetSlaveInfo(sName, True) # Get the slave info
#			
#			sGroups = sSettings.SlaveGroups
#			for g in sGroups:
#				self.LogInfo("Current Slave Groups: %s" % g)
#				
#			for i in range(len(sGroups)):
#				if sGroups[i] == "gifree":
#					sGroups[i] = "girender"
#					sSettings.SetSlaveGroups(sGroups)
#					RepositoryUtils.SaveSlaveSettings(sSettings)
#
#			job.JobGroup = 'girender'
#			RepositoryUtils.SaveJob(job) # Change the Job's Group
#			self.LogInfo( "Job has been set to girender group" )
#
#			
#			RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, sName) #add slave to whitelist

#			##### Not working properly, I think it's running this code before the task has been assigned
#			taskIDs = slaveInfo.SlaveCurrentTaskIds # get the task ID to see if it's the first task
#			for ID in taskIDs:
#				self.LogInfo("Current Task ID: %s" % ID)
#
			
	def OnJobFinished( self, job ):
		self.LogInfo("GI Slave Manager - JOB FINISHED!")
		
		isGIJob = GIJobCheck(job.JobName) #Check if it's a GI Job
		if isGIJob == True:
			job.JobGroup = 'gifree'
			RepositoryUtils.SaveJob(job) # Change the Job's Group
			self.LogInfo( "Job has been set to gifree group" )

			RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, None) #empty out whitelist group			
			
	def OnJobFailed( self, job ):
		self.LogInfo("GI Slave Manager - JOB FAILED!")
		
		isGIJob = GIJobCheck(job.JobName) #Check if it's a GI Job
		if isGIJob == True:
			job.JobGroup = 'gifree'
			RepositoryUtils.SaveJob(job)  # Change the Job's Group
			self.LogInfo( "Job has been set to gifree group" )
			
			RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, None) #empty out whitelist group

	def OnJobSuspended( self, job ):
		self.LogInfo("GI Slave Manager - JOB SUSPENDED!")	
		
		isGIJob = GIJobCheck(job.JobName) #Check if it's a GI Job
		if isGIJob == True:
			job.JobGroup = 'gifree'
			RepositoryUtils.SaveJob(job)  # Change the Job's Group
			self.LogInfo( "Job has been set to gifree group" )
			
			RepositoryUtils.SetMachineLimitListedSlaves(job.JobId, None) #empty out whitelist group
	