import sys
import os
import traceback

from Deadline.Events import *


def GetDeadlineEventListener():
	return EventScriptListener()


def CleanupDeadlineEventListener(deadlinePlugin):
	deadlinePlugin.Cleanup()


class EventScriptListener(DeadlineEventListener):

	def __init__(self):
		self.OnJobSubmittedCallback += self.OnJobSubmitted
		self.OnSlaveStartingJobCallback += self.OnSlaveStartingJob
		self.OnJobStartedCallback += self.OnJobStarted
		self.OnJobFinishedCallback += self.OnJobFinished
		self.OnJobFailedCallback += self.OnJobFailed
		self.OnJobSuspendedCallback += self.OnJobSuspended

	def Cleanup(self):
		del self.OnJobSubmittedCallback
		del self.OnSlaveStartingJobCallback
		del self.OnJobStartedCallback
		del self.OnJobFinishedCallback
		del self.OnJobFailedCallback
		del self.OnJobSuspendedCallback

	def OnJobSubmitted( self, job):
		self.LogInfo( "@@@ JOB SUBMITTED @@@")

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