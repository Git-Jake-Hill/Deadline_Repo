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
        		
		self.LogInfo("Auto Cleanup Alt Frames Started")
		folders = []
		dialogString = ""
		altRe = Regex( r"\.?_alt_[0-9]+" )
		
		#for job in MonitorUtils.GetSelectedJobs():		
		for outputDir in job.JobOutputDirectories:
			if outputDir != "":
				if(folders.count(outputDir) == 0):
					folders.append( outputDir )
					dialogString += outputDir + "\n"
		
		dialogString = ""
		altFiles = 0
		overwriteAll = 1
		skipAll = 0
			
		for folder in folders:
			
			files = Directory.GetFiles( folder )
			
			for file in files:
				newFileName = altRe.Replace( file, "" )
				
				if newFileName != file:
					
					if File.Exists (newFileName):
					
						File.Delete (newFileName)
						
					
					dialogString =  dialogString + file + "\n"
					altFiles += 1
					
					File.Move(file, newFileName)
					
		self.LogInfo( "%d alt files were found and renamed!" % altFiles)