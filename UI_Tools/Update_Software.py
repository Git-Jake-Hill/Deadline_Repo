"""Install software on the selected machines."""
from __future__ import absolute_import
from Deadline.Scripting import MonitorUtils, SlaveUtils
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

# import SoftwareList


scriptDialog = DeadlineScriptDialog()
softwareCommands = {}

def __main__():
    # type: () -> None
    global scriptDialog
    global softwareCommands

    
    with open("//SCHARPFp3/DeadlineRepository10/custom/scripts/Slaves/SoftwareList.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            k , v = line.split(":")
            k = k.strip()
            softwareCommands[k] = v
    
    print(softwareCommands)
    
    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetSize( 400, 100 )
    scriptDialog.AllowResizingDialog( True )
    scriptDialog.SetTitle( "Install Software" )
    
    scriptDialog.AddGrid()
    # select software from dropdown menu
    scriptDialog.AddControlToGrid( "ComboLabel", "LabelControl", "Select An Item", 1, 0, expand=False )
    scriptDialog.AddComboControlToGrid( "SoftwareSelect", "ComboControl", "", ( "3DS MAX", "AFTER EFFECT", "ANIMA", "RAILCLONE", "FOREST", "V-RAY", "PHOENIX", "GROW FX" ), 1, 1 )
    
    scriptDialog.EndGrid()
    
    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel1", 0, 0 )
    scriptDialog.EndGrid()
    

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel2", 0, 0 )
    startButton = scriptDialog.AddControlToGrid( "StartButton", "ButtonControl", "Install", 0, 1, expand=False )
    startButton.ValueModified.connect(InstallButtonPressed)

    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 3, expand=False )
    closeButton.ValueModified.connect(CloseButtonPressed)
    scriptDialog.EndGrid()

    scriptDialog.ShowDialog( True )

def InstallButtonPressed():
    # type: () -> None
    global scriptDialog
    global softwareCommands
    

    softwareTag = scriptDialog.GetValue( "SoftwareSelect" ).strip()

    if softwareTag == "":
        scriptDialog.ShowMessageBox( "Please specify software to install.", "Error" )
        return

    run = False

    print("Installing:", softwareTag)
    try:
        output_string = softwareCommands[softwareTag]  
        print(output_string)
    except:
        print("error accessing dictonary")
        
    if run:
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
