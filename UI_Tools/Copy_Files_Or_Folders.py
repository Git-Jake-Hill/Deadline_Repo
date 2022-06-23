"""Copies files or folders from the server onto the selected machines."""
from __future__ import absolute_import
from Deadline.Scripting import MonitorUtils, SlaveUtils
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

scriptDialog = DeadlineScriptDialog()


def __main__():
    # type: () -> None
    global scriptDialog
    
    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetSize( 600, 100 )
    scriptDialog.AllowResizingDialog( True )
    scriptDialog.SetTitle( "Copy Files/Folders" )
    
    scriptDialog.AddGrid()

    # copy file
    scriptDialog.AddControlToGrid( "FileSourceLable", "LabelControl", "Copy File", 1, 0, expand=False )
    scriptDialog.AddSelectionControlToGrid( "FileBox", "FileBrowserControl", "", "Text Files (*.txt);;All Files (*.*)", 1, 1 )

    # copy folder
    scriptDialog.AddControlToGrid( "FolderSourceLable", "LabelControl", "Copy Folder", 2, 0, expand=False )
    scriptDialog.AddSelectionControlToGrid( "FolderBox", "FolderBrowserControl", "", "", 2, 1 )

    scriptDialog.EndGrid()
    
    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel1", 0, 0 )
    scriptDialog.EndGrid()
    
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "FolderDestinationLabel", "LabelControl", "Paste File/Folder", 1, 0, expand=False )
    scriptDialog.AddSelectionControlToGrid( "FolderDestinationBox", "FolderBrowserControl", "", "", 1, 1 )

    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel1", 0, 0 )
    startButton = scriptDialog.AddControlToGrid( "StartButton", "ButtonControl", "Copy File/Folder", 0, 1, expand=False )
    startButton.ValueModified.connect(CopyButtonPressed)

    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 3, expand=False )
    closeButton.ValueModified.connect(CloseButtonPressed)
    scriptDialog.EndGrid()

    scriptDialog.ShowDialog( True )

def CopyButtonPressed():
    # type: () -> None
    global scriptDialog
    
    sourceFilePath = scriptDialog.GetValue( "FileBox" ).strip()
    sourceFolderPath = scriptDialog.GetValue( "FolderBox" ).strip()
    destinationFolderPath = scriptDialog.GetValue( "FolderDestinationBox" ).strip()

    if sourceFilePath == "" and sourceFolderPath == "":
        scriptDialog.ShowMessageBox( "Please specify a source File or Folder.", "Error" )
        return
    
    if sourceFilePath != "" and sourceFolderPath != "":
        scriptDialog.ShowMessageBox( "Please specify only one source File or Folder, not both.", "Error" )
        return

    if destinationFolderPath == "":
        scriptDialog.ShowMessageBox( "Please specify a destination Folder.", "Error" )
        return

    # copy files
    if sourceFilePath != "":
        print("Copy Files")
        output_string = f"Execute cmd /C copy {sourceFilePath} {destinationFolderPath}"
    else:
        print("Copy Folders")
        output_string = f"Execute cmd /C Robocopy /S /E {sourceFolderPath} {destinationFolderPath}"
        
    print(output_string)
    
    selectedSlaveInfoSettings = MonitorUtils.GetSelectedSlaveInfoSettings()
    # Get the list of selected machine names from the Worker info settings.
    machineNames = SlaveUtils.GetMachineNameOrIPAddresses(selectedSlaveInfoSettings)
    for machineName in machineNames:
        try:
            SlaveUtils.SendRemoteCommand( machineName, output_string )
        except Exception as e:
            print(e)


def CloseButtonPressed():
    # type: () -> None
    global scriptDialog
    scriptDialog.CloseDialog()
