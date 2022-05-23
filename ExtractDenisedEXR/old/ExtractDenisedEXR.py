from Deadline.Events import *
from Deadline.Scripting import *

def GetDeadlineEventListener():
    """This is the function that Deadline calls to get an instance of the
    main DeadlineEventListener class.
    """
    return MyEvent()

def CleanupDeadlineEventListener(deadlinePlugin):
    """This is the function that Deadline calls when the event plugin is
    no longer in use so that it can get cleaned up.
    """
    deadlinePlugin.Cleanup()

class MyEvent(DeadlineEventListener):
    """This is the main DeadlineEventListener class for MyEvent"""
    def __init__(self):
        # Set up the event callbacks here
        # self.OnJobSubmittedCallback += self.OnJobSubmitted
        self.OnJobFinishedCallback += self.OnJobFinished

    def Cleanup(self):
        
        del self.OnJobFinishedCallback

    def OnJobSubmitted(self, job):
        # TODO: Connect to pipeline site to notify it that a job has been submitted
        # for a particular shot or task.
        pass

    def OnJobFinished(self, job):
        # TODO: Connect to pipeline site to notify it that the job for a particular
        # shot or task is complete.
        print("JOB FINSIHED")
        self.LogInfo("Checking for - DENOISE + LENS EFFECT [MAXSCRIPT]")
        self.LogInfo(job.JobName)
        if job.JobName.endswith("DENOISE + LENS EFFECT [MAXSCRIPT]"):
            values = job.GetJobExtraInfoKeyValue("REToDenoise")
            self.LogInfo("Job Found")
            self.LogInfo(values)

