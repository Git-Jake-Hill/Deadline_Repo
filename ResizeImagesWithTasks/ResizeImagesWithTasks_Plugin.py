#!/usr/bin/env python3
from Deadline.Plugins import *

def GetDeadlinePlugin():
	"""This is the function that Deadline calls to get an instance of the
	main DeadlinePlugin class.
	"""
	return MyPlugin()

def CleanupDeadlinePlugin(deadlinePlugin):
	"""This is the function that Deadline calls when the plugin is no
	longer in use so that it can get cleaned up.
	"""
	deadlinePlugin.Cleanup()

class MyPlugin(DeadlinePlugin):
	"""This is the main DeadlinePlugin class for MyPlugin."""
	Process = None  # Variable to hold the Managed Process object.

	def __init__(self):
		"""Hook up the callbacks in the constructor."""
		self.InitializeProcessCallback += self.InitializeProcess
		self.StartJobCallback += self.StartJob
		self.RenderTasksCallback += self.RenderTasks
		self.EndJobCallback += self.EndJob

	def Cleanup(self):
		"""Clean up the plugin."""
		del self.InitializeProcessCallback
		del self.StartJobCallback
		del self.RenderTasksCallback
		del self.EndJobCallback

		# Clean up the managed process object.
		if self.Process:
			self.Process.Cleanup()
			del self.Process

	def InitializeProcess(self):
		"""Called by Deadline to initialize the process."""
		# Set the plugin specific settings.
		self.SingleFramesOnly = False
		self.PluginType = PluginType.Advanced

	def StartJob(self):
		"""Called by Deadline when the job starts."""
		myProcess = MyPluginProcess()
		StartMonitoredManagedProcess("My Process", myProcess)
		self.RenderTasks()

	def RenderTasks(self):
		"""Called by Deadline for each task the Worker renders."""
		# Do something to interact with the running process.
		self.LogInfo( "   *****ALERT: RENDER TASK ADDED*****" )

	def EndJob(self):
		"""Called by Deadline when the job ends."""
		ShutdownMonitoredManagedProcess("My Process")

class MyPluginProcess(ManagedProcess):
	"""This is the ManagedProcess class that is launched above."""
	def __init__(self, deadlinePlugin):
		"""Hook up the callbacks in the constructor."""
		self.deadlinePlugin = deadlinePlugin

		self.InitializeProcessCallback += self.InitializeProcess
		self.RenderExecutableCallback += self.RenderExecutable
		self.RenderArgumentCallback += self.RenderArgument

	def Cleanup(self):
		"""Clean up the managed process."""
		# Clean up stdout handler callbacks.
		for stdoutHandler in self.StdoutHandlers:
			del stdoutHandler.HandleCallback

		del self.InitializeProcessCallback
		del self.RenderExecutableCallback
		del self.RenderArgumentCallback

	def InitializeProcess(self):
		"""Called by Deadline to initialize the process."""
		# Set the ManagedProcess specific settings.
		self.SingleFramesOnly = True
		self.PluginType = PluginType.Advanced

	def HandleStdoutWarning(self):
		"""Callback for when a line of stdout contains a WARNING message."""
		self.deadlinePlugin.LogWarning(self.GetRegexMatch(0))

	def HandleStdoutError(self):
		"""Callback for when a line of stdout contains an ERROR message."""
		self.deadlinePlugin.FailRender("Detected an error: " + self.GetRegexMatch(1))

	def RenderExecutable(self):
		"""Callback to get the executable used for rendering."""
		return self.deadlinePlugin.GetConfigEntry("MyPluginRenderExecutable")

	def RenderArgument(self):
		"""Callback to get the arguments that will be passed to the executable."""
		arguments = ' -verbose ' + self.deadlinePlugin.GetPluginInfoEntry('Verbose')
		arguments += ' -scene "{}"'.format(self.deadlinePlugin.GetDataFilename())
		return arguments