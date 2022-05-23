###############################################################
# Imports
###############################################################
from Deadline.Events import *
from Deadline.Scripting import *
from Deadline.Jobs import *


def GetDeadlineEventListener():
	return SetJobInterruptiblePercentageListener()


def CleanupDeadlineEventListener(eventListener):
	eventListener.Cleanup()


###############################################################
# The event listener class.
###############################################################
class SetJobInterruptiblePercentageListener (DeadlineEventListener):
	def __init__(self):
		self.OnJobSubmittedCallback += self.OnJobSubmitted
		
	def Cleanup(self):
		del self.OnJobSubmittedCallback

	def OnJobSubmitted(self, job):

		interruptiblePercentage = self.GetIntegerConfigEntryWithDefault("InterruptiblePercentage", 1)	# get percentage set in param file
		job.JobInterruptiblePercentage = interruptiblePercentage	# set percentage for job
		self.LogInfo("+Job Interruptible Percentage set to: %s" % interruptiblePercentage)
		
		RepositoryUtils.SaveJob(job)	#save it back to repository