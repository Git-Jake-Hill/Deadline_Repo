'''
    QueryDeadlineInjectData.py - Capture and record custom job statistics
    Puesdo-code:
    Check every active job in the queue:
    IF job is currently active (rendering/queued) THEN
        Return job object & tasks and calculate job stats object
        Query & inject average frame render time into column "ExtraInfo2" for each job
        Query & inject peak ram usage into column "ExtraInfo3" for each job
    Notes:
    1. It is assumed a studio will rename the "ExtraInfo2" column used to something more meaningful such as "Average Frame Render Time" via repo options
    2. It is assumed a studio will rename the "ExtraInfo3" column used to something more meaningful such as "Peak RAM Usage" via repo options
    2. It is assumed we are only checking currently "Active" & "Queued" jobs only
    3. It is assumed we are running this python script on a machine that has the Deadline client software already installed
'''

from System import TimeSpan
import datetime
import time
from time import time

from Deadline.Scripting import *
from Deadline.Jobs import *
from Deadline.Events import *

def GetDeadlineEventListener():
	return HouseCleaningEvent()

def CleanupDeadlineEventListener( eventListener ):
	eventListener.Cleanup()

def convertTimeToSecs(hours,mins,secs):
	totalSecs = (hours*3600)
	totalSecs += (mins*60)
	totalSecs += secs
	return totalSecs

def convertSecsToTime(secs):
	m, s = divmod(secs, 60)
	h, m = divmod(m, 60)
	return "%d:%02d:%02d" % (h, m, s)	
	
class HouseCleaningEvent (DeadlineEventListener):
	def __init__( self ):
		self.OnHouseCleaningCallback += self.OnHouseCleaning

	def Cleanup( self ):
		del self.OnHouseCleaningCallback

	def OnHouseCleaning( self ):
		MIN_COMPLETED_TASKS = 1  # Min - Number of Completed Tasks BEFORE the job is queried. Change as applicable

		for job in RepositoryUtils.GetJobs(True):
			# Filter out non-"Active" jobs
			if job.JobStatus != "Active":
				continue

			jobName = job.JobName
			jobId = job.JobId
			JobTaskCount = job.JobTaskCount
			jobCompletedChunks = job.CompletedChunks
			jobNumQueuedTasks = job.JobQueuedTasks
			jobNumRenderingTasks = job.JobRenderingTasks		
			job = RepositoryUtils.GetJob(jobId, True)
			tasks = RepositoryUtils.GetJobTasks(job, True)
			stats = JobUtils.CalculateJobStatistics(job, tasks)
			jobAverageFrameRenderTime = stats.AverageFrameRenderTime
			

		# Split the estimated time remaining into 2 parts
		#	The first is the estimated task time of the rendering tasks
		#	The secong is the estimated task time of the queued tasks
			
			addedTaskPercent = 0.0
			avgCompletedTaskTimeSecs = 0
			for task in tasks:
				# Find the average percentage for tasks that are rendering
				if task.TaskStatus == "Rendering":			
					# Get the average task percentage
					# Have to first convert the string to a float and strip the percent char
					floatTaskPecent = float(task.TaskProgress.strip('%')) / 100.0
					addedTaskPercent += floatTaskPecent
				# I don't trust the inbuilt average time here, it never seems accurate
				# so I'm going to create my own.
				elif task.TaskStatus == "Completed":
					splitHours,splitMins,splitSecs = str(task.TaskRenderTime).split(":")
					splitSecs = splitSecs.split(".")[0]
					avgCompletedTaskTimeSecs += convertTimeToSecs(int(splitHours),int(splitMins),int(splitSecs))

			if jobCompletedChunks != 0: # Check to see if there's previous times to go against
				myAverageTimeSecs = avgCompletedTaskTimeSecs/jobCompletedChunks
			
				# Get the average task percentage for jobs that have current rendering tasks
				if jobNumRenderingTasks > 0:
					averageTaskPercent = addedTaskPercent/jobNumRenderingTasks
					
			# Find the estimated time remaining
				
					# Take the average time and split it into hours, mins, secs
					splitHours,splitMins,splitSecs = str(jobAverageFrameRenderTime).split(":")
					#Remove the . value from the end of secs
					splitSecs = splitSecs.split(".")[0]
					avgTimeSecs = convertTimeToSecs(int(splitHours),int(splitMins),int(splitSecs))
					renderingTimeRemainingSecs = (myAverageTimeSecs*(1-averageTaskPercent))
					convertSecsToTime(renderingTimeRemainingSecs)

					# Now to get the estimated time remaining for tasks that are Queued
						# Number of Jobs Queued * Average Frame Time / Number of slaves available
					queuedTimeRemainingSecs = ((jobNumQueuedTasks * myAverageTimeSecs)/jobNumRenderingTasks)

					# Add the estimated time remaining on rendering tasks to the queued tasks
					totalTimeRemainingSecs = (renderingTimeRemainingSecs+queuedTimeRemainingSecs)

					totalTimeRemaining = convertSecsToTime(totalTimeRemainingSecs)
					
					job.ExtraInfo0 = str(totalTimeRemaining)

					RepositoryUtils.SaveJob(job)
				else:
					job.ExtraInfo0 = str("NOT AVAILABLE")
			else:
				job.ExtraInfo0 = str("NOT AVAILABLE")	