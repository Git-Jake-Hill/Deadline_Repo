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

##################################################################################################
# This is the function called by Deadline to get an instance of the Draft event listener.
##################################################################################################
def GetDeadlineEventListener():
	return eventTest()


def CleanupDeadlineEventListener(eventListener):
	eventListener.Cleanup()


###############################################################
# The event listener class.
###############################################################
class eventTest (DeadlineEventListener):
	def __init__(self):
		self.OnJobFinishedCallback += self.OnJobFinished
	
	def Cleanup(self):
		del self.OnJobFinishedCallback

	def OnJobFinished(self, job):
		self.LogInfo("Checking for - DENOISE + LENS EFFECT [MAXSCRIPT]")
		# print("ExtractEXR")
		self.LogInfo(job.JobName)

		if job.JobName.endswith("DENOISE + LENS EFFECT [MAXSCRIPT]"):
			values = job.GetJobExtraInfoKeyValue("REToDenoise") # additional render elements to extract
			self.LogInfo("Job Found")
			self.LogInfo(values)