import sys
import os
import traceback

import Deadline.Events


def GetDeadlineEventListener():
	return EventScriptListener()


def CleanupDeadlineEventListener(eventListener):
	eventListener.Cleanup()


class EventScriptListener(Deadline.Events.DeadlineEventListener):

	def __init__(self):
		self.OnSlaveStartingJobCallback += self.OnSlaveStartingJob
		self.OnJobStartedCallback += self.OnJobStarted
		self.OnJobFinishedCallback += self.OnJobFinished
		self.OnJobFailedCallback += self.OnJobFailed
		self.OnJobSuspendedCallback += self.OnJobSuspended

	def Cleanup(self):
		del self.OnSlaveStartingJobCallback
		del self.OnJobStartedCallback
		del self.OnJobFinishedCallback
		del self.OnJobFailedCallback
		del self.OnJobSuspendedCallback

	def OnSlaveStartingJob(self, slaveName, job):
		self.LogInfo( "SLAVE STARTING JOB" )
			
	def OnJobStarted(self, job):
		self.LogInfo( "JOB STARTED" )
		
	def OnJobFinished(self, job):
		self.LogInfo( "JOB FINISHED" )		
		
	def OnJobFailed(self, job):
		self.LogInfo( "JOB FAILED" )		
		
	def OnJobSuspended(self, job):
		self.LogInfo( "JOB SUSPENDED" )		