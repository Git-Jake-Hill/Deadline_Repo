###############################################################
# Imports
###############################################################
import os
import re
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
        		
		self.LogInfo("Render Log - check for tile assembley.")
		tile_assembley = "Draft Assembler Dependent Job Submission from 3ds Max"
		
		job_keys = job.GetJobInfoKeys()

		# for i in job_keys:
		# 	print(i, job.GetJobInfoKeyValue(i))
		# print(job.GetJobInfoKeyValue("Comment"))

		if job.GetJobInfoKeyValue("Comment") == tile_assembley:
			print("Tile assembley job found")
			
			outputDirectories = job.OutputDirectories
			outputFilenames = job.OutputFileNames
			jobName = job.JobName
			user_name = job.JobUserName
			paddingRegex = re.compile("[^\\?#]*([\\?#]+).*")
			print(jobName)
			print(user_name)
			
			outputDirectory = outputDirectories[0]
			outputFilename = outputFilenames[0]

			log_file_path = "G:/Temp/JH/Scripts/Photoshop_Render_List/" + user_name
			if not os.path.isdir(log_file_path):
				os.makedirs(log_file_path)

			
			outputPath = Path.Combine(outputDirectory,outputFilename)
			outputPath = outputPath.replace("//","/")


			# deadlinePlugin.LogInfo("Output file: " + outputPath)
			textFile = open(log_file_path + "/" + jobName + ".txt", "w")
			textFile.writelines(outputPath)
			textFile.close()

		else:
			self.LogInfo("Render Log - not tile assembley job.")
